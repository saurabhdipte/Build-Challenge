# Intuit Build Challenge

This repository contains my submission for the **Intuit Build Challenge**, consisting of two independent tasks implemented in Python.

Both tasks focus on writing clean, readable, and testable code while clearly documenting assumptions and handling edge cases.

---

## Repository Structure

```
.
├── Task1/
│   ├── src/
│   │   └── library_system/
│   ├── tests/
│   ├── demo.py
│   ├── requirements.txt
│   └── README.md
│
├── Task2/
│   ├── order_processor.py
│   ├── orders.txt
│   ├── summary_report.txt
│   ├── error_log.txt
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
└── README.md   ← (this file)
```

---

## Task 1 – Library Management System

A simple object-oriented library system that supports:

- Adding books and registering members
- Checking out and returning books
- Enforcing borrowing limits and fine rules
- Calculating overdue fines
- Tracking borrowing history
- Unit testing core functionality

📄 **Details:** See `Task1/README.md` for full documentation, assumptions, and usage instructions.

---

## Task 2 – Order Invoice Summary

A file-processing application that:

- Parses pipe-delimited order records from a text file
- Applies business rules and discounts
- Aggregates data by customer
- Generates a formatted invoice summary report
- Logs malformed or invalid records
- Includes unit tests for validation and edge cases

📄 **Details:** See `Task2/README.md` for full documentation, assumptions, and usage instructions.

---

## Setup

Each task is self-contained and includes its own `requirements.txt`.

To run a task:
1. Navigate to the task directory
2. Create and activate a virtual environment
3. Install dependencies
4. Run the program or tests as described in the task README

---

## Testing

Both tasks use **pytest** for unit testing.

Tests are designed to:
- Cover core functionality
- Validate business rules
- Handle edge cases and invalid inputs
- Ensure deterministic behavior

---

## Notes

- Both tasks are intentionally kept simple and in-memory
- No external databases or services are used
- All design assumptions are explicitly documented in the respective task README files
- Code prioritizes clarity, correctness, and maintainability

---

Thank you for reviewing my submission.
