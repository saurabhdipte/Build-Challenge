# Library Book Checkout System (Task 1)

## Overview
This project implements a **library book checkout system** using Python and object-oriented design principles.

The system manages:
- Books
- Library members
- Book checkouts and returns
- Due dates and overdue fines

It enforces the following business rules:

1. A member can borrow **at most 3 books** at a time  
2. Books are due **14 days** from the checkout date  
3. Overdue books incur a fine of **$0.50 per day**  
4. Members with **unpaid fines over $10** cannot borrow new books  

The project includes:
- Core domain models (`Book`, `Member`, `Library`)
- Proper exception handling
- A demo program showing all operations
- Unit tests covering core functionality and edge cases

---

## Project Structure

```
Task1/
├─ readme.md
├─ requirements.txt
├─ conftest.py
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

The demo program demonstrates:
- Adding books and members
- Successful and failed checkouts
- Overdue fine calculation
- Book return with fine charging
- Borrowing history tracking

Run the demo with:

```bash
python -m src.library_system
```

---

## Running Unit Tests

All core methods and rule violations are covered by unit tests.

Run tests using:

```bash
pytest -q
```

---

## Design Notes & Assumptions

- The system uses **object-oriented design**:
  - `Book` represents a library book
  - `Member` encapsulates borrower state and history
  - `Library` acts as the service layer enforcing business rules
- Overdue fines are **charged at the time of return**
- `calculateFine()` reports **currently accrued overdue fines** for active loans but does not mutate `fineBalance`
- Custom exceptions are used to signal invalid operations (e.g., rule violations, missing entities)
- All date handling is done using Python’s `datetime.date`

---

## Sample Output (Demo)

```
--- Available books initially ---
['Clean Code', 'Design Patterns', 'The Pragmatic Programmer', 'Effective Python']

--- Checkout 3 books for M1 ---
--- Try 4th checkout (should fail) ---
Expected error: Member cannot borrow more than 3 books at a time.

--- Accrued fine as of 2026-02-21 ---
3.0

--- Return one late book ---
Fine charged: 3.0
```

---

