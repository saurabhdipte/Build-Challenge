from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, List, Optional

from ..exceptions import BookNotFoundError, MemberNotFoundError, CheckoutRuleViolation
from .book import Book
from .member import Member, BorrowRecord


class Library:
    MAX_BORROWED = 3
    LOAN_DAYS = 14
    FINE_PER_DAY = 0.50
    FINE_BLOCK_THRESHOLD = 10.0

    # Initialize the library with empty book and member collections
    def __init__(self) -> None:
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}

    # Fetch a member by ID or raise an error if not found
    def _get_member(self, memberId: str) -> Member:
        if memberId not in self.members:
            raise MemberNotFoundError(f"Member not found: {memberId}")
        return self.members[memberId]

    # Fetch a book by ISBN or raise an error if not found
    def _get_book(self, isbn: str) -> Book:
        if isbn not in self.books:
            raise BookNotFoundError(f"Book not found: {isbn}")
        return self.books[isbn]

    # Compute the due date for a checkout based on loan duration
    def _due_date(self, checkout_date: date) -> date:
        return checkout_date + timedelta(days=self.LOAN_DAYS)

    # Calculate overdue fine for a single loan as of a given date
    def _fine_for_loan(self, checkout_date: date, as_of: date) -> float:
        due = self._due_date(checkout_date)
        if as_of <= due:
            return 0.0
        overdue_days = (as_of - due).days
        return round(overdue_days * self.FINE_PER_DAY, 2)

    # Add a new book to the library collection
    def addBook(self, book: Book) -> None:
        if book is None or not isinstance(book, Book):
            raise TypeError("book must be a Book instance.")
        if book.isbn in self.books:
            raise ValueError(f"Book with ISBN {book.isbn} already exists.")
        self.books[book.isbn] = book

    # Register a new member in the library
    def registerMember(self, member: Member) -> None:
        if member is None or not isinstance(member, Member):
            raise TypeError("member must be a Member instance.")
        if member.memberId in self.members:
            raise ValueError(f"Member with ID {member.memberId} already exists.")
        self.members[member.memberId] = member

    # Checkout a book to a member while enforcing borrowing and fine rules
    def checkoutBook(self, memberId: str, isbn: str, checkoutDate: Optional[date] = None) -> None:
        member = self._get_member(memberId)
        book = self._get_book(isbn)
        checkoutDate = checkoutDate or date.today()

        member.fineBalance = self.calculateFine(memberId, as_of=checkoutDate)
        if member.fineBalance > self.FINE_BLOCK_THRESHOLD:
            raise CheckoutRuleViolation("Member has unpaid fines over $10 and cannot borrow new books.")

        if not book.isAvailable:
            raise CheckoutRuleViolation("Book is not available.")

        if len(member.borrowedBooks) >= self.MAX_BORROWED:
            raise CheckoutRuleViolation("Member cannot borrow more than 3 books at a time.")

        if isbn in member.borrowedBooks:
            raise CheckoutRuleViolation("Member already has this book checked out.")

        member.borrowedBooks[isbn] = checkoutDate
        book.isAvailable = False

        member.borrowingHistory.append(
            BorrowRecord(
                isbn=isbn,
                checkoutDate=checkoutDate,
                dueDate=self._due_date(checkoutDate),
            )
        )

        member.fineBalance = self.calculateFine(memberId, as_of=checkoutDate)

    # Return a borrowed book and update fines and borrowing history
    def returnBook(self, memberId: str, isbn: str, returnDate: Optional[date] = None) -> float:
        member = self._get_member(memberId)
        book = self._get_book(isbn)
        returnDate = returnDate or date.today()

        if isbn not in member.borrowedBooks:
            raise CheckoutRuleViolation("This member did not borrow this book.")

        checkoutDate = member.borrowedBooks[isbn]
        if returnDate < checkoutDate:
            raise CheckoutRuleViolation("Return date cannot be before checkout date.")

        fine_for_this_book = self._fine_for_loan(checkoutDate, returnDate)

        for rec in reversed(member.borrowingHistory):
            if rec.isbn == isbn and rec.returnDate is None:
                rec.returnDate = returnDate
                rec.fineCharged = fine_for_this_book
                break

        del member.borrowedBooks[isbn]
        book.isAvailable = True

        member.fineBalance = self.calculateFine(memberId, as_of=returnDate)

        return fine_for_this_book

    # Calculate the current overdue fine for all active borrowed books
    def calculateFine(self, memberId: str, as_of: Optional[date] = None) -> float:
        member = self._get_member(memberId)
        as_of = as_of or date.today()

        total = 0.0
        for _, checkoutDate in member.borrowedBooks.items():
            total += self._fine_for_loan(checkoutDate, as_of)

        return round(total, 2)

    # Retrieve all books that are currently available for checkout
    def getAvailableBooks(self) -> List[Book]:
        return [b for b in self.books.values() if b.isAvailable]

    # Return the complete borrowing history for a member
    def getMemberBorrowingHistory(self, memberId: str):
        member = self._get_member(memberId)
        return list(member.borrowingHistory)
