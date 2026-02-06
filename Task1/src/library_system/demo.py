"""
demo.py
Demonstrates all core operations of the Library Book Checkout System.
"""

from datetime import date

from .models import Book, Member, Library
from .exceptions import LibraryError


def run_demo():
    print("\n========== LIBRARY SYSTEM DEMO ==========\n")

    library = Library()

    # Add sample books
    library.addBook(Book("111", "Clean Code", "Robert C. Martin"))
    library.addBook(Book("222", "Design Patterns", "GoF"))
    library.addBook(Book("333", "The Pragmatic Programmer", "Hunt & Thomas"))
    library.addBook(Book("444", "Effective Python", "Brett Slatkin"))

    # Register members
    library.registerMember(Member("M1", "Saurabh"))
    library.registerMember(Member("M2", "Alex"))

    print("Available books initially:")
    print([book.title for book in library.getAvailableBooks()])

    # Checkout 3 books for M1 on Feb 1
    checkout_date = date(2026, 2, 1)
    print("\nCheckout 3 books for member M1 on 2026-02-01")
    library.checkoutBook("M1", "111", checkoutDate=checkout_date)
    library.checkoutBook("M1", "222", checkoutDate=checkout_date)
    library.checkoutBook("M1", "333", checkoutDate=checkout_date)

    # Rule: Max 3 books
    print("\nAttempting 4th checkout (should fail)")
    try:
        library.checkoutBook("M1", "444", checkoutDate=checkout_date)
    except LibraryError as e:
        print("Expected error:", e)

    # Accrued fine as of Feb 21 (all 3 overdue by 6 days => 9.0)
    as_of_date = date(2026, 2, 21)
    print(f"\nTotal overdue fine for M1 as of {as_of_date}:")
    print(library.calculateFine("M1", as_of=as_of_date))

    # Return ONE book late on Feb 21
    # LIVE fineBalance should drop from 9.0 to 6.0 because 2 overdue books remain.
    print("\nReturning book 111 late on 2026-02-21")
    fine_for_returned_book = library.returnBook("M1", "111", returnDate=as_of_date)
    print("Fine attributable to returned book:", fine_for_returned_book)
    print("Member live fineBalance now (remaining overdue):", library.members["M1"].fineBalance)
    print("Total overdue fine as of 2026-02-21 (should now be 6.0):", library.calculateFine("M1", as_of=as_of_date))

    # Rule: Block checkout if LIVE fineBalance > $10 (natural scenario)
    print("\nDemonstrating fine-block rule (natural scenario: overdue > $10)")
    try:
        # By March 10, the remaining 2 books are very overdue => fine > $10
        library.checkoutBook("M1", "444", checkoutDate=date(2026, 3, 10))
    except LibraryError as e:
        print("Expected fine-block error:", e)

    print("\nAvailable books after return:")
    print([book.title for book in library.getAvailableBooks()])

    print("\nBorrowing history for M1:")
    for rec in library.getMemberBorrowingHistory("M1"):
        print(rec)

    print("\n========== DEMO COMPLETE ==========\n")


if __name__ == "__main__":
    run_demo()
