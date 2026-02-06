# Library Management System (Task 1)

This project implements a simple **Library Management System** using Python and object-oriented design.

It supports adding books, registering members, checking out and returning books, enforcing borrowing rules, calculating fines, and tracking borrowing history.

---

## Features

- Add books to the library  
- Register library members  
- Check out books  
- Return books  
- Enforce borrowing rules  
- Calculate overdue fines  
- View member borrowing history  
- Unit tests for core functionality  

---

## Business Rules

- A book can only be checked out if it is **available**
- A member can borrow **at most 3 books** at a time
- A member **cannot borrow books if their outstanding fine exceeds $10**
- Each book can be borrowed for **14 days**
- Overdue fine is **$1 per day**
- Every checkout and return is recorded in the member’s borrowing history

---

## Fine Handling (Important Assumption)

### Assumption

This system assumes that **any fine for a book is paid at the time the book is returned**.

### How it works

- `fineBalance` represents the **current outstanding fine for books that are still borrowed and overdue**
- Fines are calculated dynamically based on overdue days
- When a late book is returned:
  - The fine for that book is considered **paid immediately**
  - That fine is no longer included in `fineBalance`

Because of this:
- Returning overdue books can reduce the outstanding fine
- A member may regain borrowing eligibility after returning books, as long as the remaining fine is **$10 or less**

This assumption is applied consistently across the code and tests.

---

## Project Structure

```
Task1/
├── src/
│   └── library_system/
│       ├── models/
│       │   ├── book.py
│       │   ├── member.py
│       │   ├── borrow_record.py
│       │   └── library.py
├── demo.py
├── tests/
│   └── test_library.py
├── requirements.txt
└── README.md
```

---

## How to Run

### Create and activate virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows
pip install -r requirements.txt
```

---

### Run the demo

```bash
python demo.py
```

---

## How to Run Tests

Unit tests are written using **pytest**.

Run from the `Task1/` directory:

```bash
pytest
```

---

## Error Handling

The system raises clear errors for invalid operations, including:

- Book not found
- Member not found
- Book already checked out
- Borrow limit exceeded
- Outstanding fine exceeds allowed limit
- Invalid return operations

---

## Notes

- The system is in-memory and does not use a database
- Dates can be passed explicitly for deterministic testing
- The design prioritizes clarity, correctness, and testability
