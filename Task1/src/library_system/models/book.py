class Book:
    def __init__(self, isbn: str, title: str, author: str, isAvailable: bool = True):
        self.isbn = str(isbn)
        self.title = str(title)
        self.author = str(author)
        self.isAvailable = bool(isAvailable)

    def __str__(self) -> str:
        status = "Available" if self.isAvailable else "Checked out"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {status}"
