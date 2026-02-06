class LibraryError(Exception):
    """Base exception for the library system."""


class BookNotFoundError(LibraryError):
    pass


class MemberNotFoundError(LibraryError):
    pass


class CheckoutRuleViolation(LibraryError):
    pass
