import pytest
from datetime import date

from library_system.models import Book, Member, Library
from library_system.exceptions import BookNotFoundError, MemberNotFoundError, CheckoutRuleViolation


@pytest.fixture()
def lib():
    l = Library()
    l.addBook(Book("111", "A", "Auth1"))
    l.addBook(Book("222", "B", "Auth2"))
    l.addBook(Book("333", "C", "Auth3"))
    l.addBook(Book("444", "D", "Auth4"))
    l.registerMember(Member("M1", "Saurabh"))
    return l


def test_member_not_found(lib):
    with pytest.raises(MemberNotFoundError):
        lib.checkoutBook("X", "111")


def test_book_not_found(lib):
    with pytest.raises(BookNotFoundError):
        lib.checkoutBook("M1", "999")


def test_checkout_unavailable(lib):
    lib.checkoutBook("M1", "111", checkoutDate=date(2026, 2, 1))
    with pytest.raises(CheckoutRuleViolation):
        lib.checkoutBook("M1", "111", checkoutDate=date(2026, 2, 1))


def test_checkout_max_3(lib):
    d = date(2026, 2, 1)
    lib.checkoutBook("M1", "111", checkoutDate=d)
    lib.checkoutBook("M1", "222", checkoutDate=d)
    lib.checkoutBook("M1", "333", checkoutDate=d)
    with pytest.raises(CheckoutRuleViolation):
        lib.checkoutBook("M1", "444", checkoutDate=d)


def test_calculateFine_overdue_three_books(lib):
    d = date(2026, 2, 1)
    lib.checkoutBook("M1", "111", checkoutDate=d)
    lib.checkoutBook("M1", "222", checkoutDate=d)
    lib.checkoutBook("M1", "333", checkoutDate=d)

    # Due Feb 15; as_of Feb 21 => 6 overdue days => $3.00 per book; 3 books => $9.00
    assert lib.calculateFine("M1", as_of=date(2026, 2, 21)) == 9.0


def test_returnBook_updates_live_fineBalance(lib):
    d = date(2026, 2, 1)
    lib.checkoutBook("M1", "111", checkoutDate=d)
    lib.checkoutBook("M1", "222", checkoutDate=d)
    lib.checkoutBook("M1", "333", checkoutDate=d)

    assert lib.calculateFine("M1", as_of=date(2026, 2, 21)) == 9.0

    fine = lib.returnBook("M1", "111", returnDate=date(2026, 2, 21))
    assert fine == 3.0

    # Remaining 2 books overdue => live fineBalance = 6.0
    assert lib.members["M1"].fineBalance == 6.0
    assert lib.calculateFine("M1", as_of=date(2026, 2, 21)) == 6.0

    assert lib.books["111"].isAvailable is True


def test_fine_block_rule_natural_overdue(lib):
    d = date(2026, 2, 1)
    lib.checkoutBook("M1", "111", checkoutDate=d)
    lib.checkoutBook("M1", "222", checkoutDate=d)
    lib.checkoutBook("M1", "333", checkoutDate=d)

    # Return one on Feb 21 so only 2 remain overdue
    lib.returnBook("M1", "111", returnDate=date(2026, 2, 21))

    # By March 10, the two remaining books are overdue enough that total fine > $10
    with pytest.raises(CheckoutRuleViolation):
        lib.checkoutBook("M1", "444", checkoutDate=date(2026, 3, 10))


def test_returnBook_not_borrowed_raises(lib):
    with pytest.raises(CheckoutRuleViolation):
        lib.returnBook("M1", "111", returnDate=date(2026, 2, 21))


def test_returnBook_return_before_checkout_raises(lib):
    d = date(2026, 2, 10)
    lib.checkoutBook("M1", "111", checkoutDate=d)
    with pytest.raises(CheckoutRuleViolation):
        lib.returnBook("M1", "111", returnDate=date(2026, 2, 9))
