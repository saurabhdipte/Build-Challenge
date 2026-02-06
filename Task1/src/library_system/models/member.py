from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional


@dataclass
class BorrowRecord:
    isbn: str
    checkoutDate: date
    dueDate: date
    returnDate: Optional[date] = None
    fineCharged: float = 0.0


@dataclass
class Member:
    memberId: str
    name: str

    # Active loans: isbn -> checkoutDate
    borrowedBooks: Dict[str, date] = field(default_factory=dict)

    # Completed + open history
    borrowingHistory: List[BorrowRecord] = field(default_factory=list)

    # Unpaid fines already charged (charged on return)
    fineBalance: float = 0.0

    def __str__(self) -> str:
        return f"Member {self.memberId}: {self.name} (Fine: ${self.fineBalance:.2f})"
