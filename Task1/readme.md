# Library Book Checkout System (Task 1)

## Overview
This project implements a **library book checkout system** in Python using object-oriented design.
It was built as part of an interview build challenge and focuses on correctness, clarity, and
business rule enforcement rather than over-engineering.

The system manages:
- Books
- Library members
- Book checkouts and returns
- Due dates and overdue fines

---

## Business Rules Implemented

1. A member can borrow **at most 3 books** at a time  
2. Books are due **14 days** from the checkout date  
3. Overdue books incur a fine of **$0.50 per day per book**  
4. Members with **total overdue fines greater than $10** cannot borrow new books  

---

## Fine Accounting Model (Important)

- `fineBalance` represents a **LIVE overdue fine meter** for currently borrowed books.
- Fines accrue daily for overdue books.
- Returning a book removes that book from the overdue set, so the total fine decreases.

Example:
- 3 overdue books × $3 each = **$9**
- Return 1 overdue book → remaining fine = **$6**

This model reflects the *current overdue amount*, not historical debt.

---

## Project Structure

```
Task1/
├─ readme.md
├─ requirements.txt
├─ .gitignore
├─ src/
│  └─ library_system/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ demo.py
│     ├─ exceptions.py
│     └─ models/
│        ├─ __init__.py
│        ├─ book.py
│        ├─ member.py
│        └─ library.py
└─ tests/
   └─ test_library.py
```

---

## Setup Instructions

### Prerequisites
- Python 3.9+

### Install dependencies
From the `Task1/` directory:

```bash
pip install -r requirements.txt
```

---

## Running the Demo

Run the demo with:

```bash
python -m src.library_system
```

---

## Running Unit Tests

Run tests using:

```bash
pytest -q
```

---

## Design Notes

- `Book`, `Member`, and `Library` are modeled as separate classes.
- `Library` enforces all business rules.
- Custom exceptions signal invalid operations.
- Borrowing history records both active and completed loans.

---

## Sample Output

```
Total overdue fine for M1 as of 2026-02-21:
9.0

Returning book 111 late on 2026-02-21
Fine attributable to returned book: 3.0
Member live fineBalance now (remaining overdue): 6.0
```

---

## Notes
This project demonstrates clean Python design, rule enforcement, and testability.
