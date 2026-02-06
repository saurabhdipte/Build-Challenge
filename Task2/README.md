# Order Invoice Summary (Assignment 2)

Processes pipe-delimited order records from a text file and generates a customer-level invoice summary report.

This assignment demonstrates file I/O, string parsing, data aggregation, formatted output generation, error handling, and unit testing using Python best practices.

---

## Input format

Each input line is:

`OrderID|CustomerName|ProductName|Quantity|UnitPrice|OrderDate`

Example:

`ORD001|John Smith|Laptop|2|999.99|2024-03-15`

Notes:
- Lines beginning with `#` are treated as comments and skipped
- Empty lines are ignored
- Each record represents one product line item

---

## Business rules

- Line total = `quantity * unit_price`
- Discount:
  - 10% discount applies when **line total > $500.00**
- Summary grouped by customer includes:
  - customer name
  - number of distinct orders
  - total items purchased
  - gross total
  - discount amount
  - net total
- Output includes a **GRAND TOTAL** row at the bottom

---

## Error handling

Malformed or invalid records are logged to `error_log.txt` and processing continues.

Handled cases:
- wrong number of fields
- empty required fields (OrderID, CustomerName, ProductName)
- non-integer, zero, or negative quantity
- invalid or negative unit price
- invalid date format (must be YYYY-MM-DD)

---

## Project structure

Task2/
  order_processor.py
  orders.txt
  summary_report.txt
  error_log.txt
  requirements.txt
  README.md
  tests/
    test_order_processor.py

---

## Setup

### Create and activate virtual environment

### Windows (PowerShell / Git Bash)

python -m venv .venv  
source .venv/Scripts/activate  
python -m pip install --upgrade pip  
pip install -r requirements.txt  

### macOS / Linux

python3 -m venv .venv  
source .venv/bin/activate  
python -m pip install --upgrade pip  
pip install -r requirements.txt  

---

## How to run the code

From the project root directory (`Task2/`), run:

python order_processor.py

This generates:
- `summary_report.txt` – formatted customer invoice summary
- `error_log.txt` – malformed or invalid input records

The input file used is `orders.txt`.

---

## How to run unit tests

Unit tests are written using **pytest** and cover all core functionality.

Run from the project root directory:

python -m pytest -q

---

## Sample output (excerpt)

Customer              #Orders   Items    GrossTotal      Discount        NetTotal
------------------------------------------------------------------------------
Aisha Khan                 7      26      2,345.98        234.60        2,111.38
John Smith                 6      11      3,454.96        345.50        3,109.46
------------------------------------------------------------------------------
GRAND TOTAL               25      94      9,876.54        876.23        9,000.31

---

## Assumptions

- Each record represents one purchased product (line item)
- Order count is based on **distinct Order IDs**
- Currency values are rounded to **2 decimal places (half-up rounding)**
- Discount is applied **per line item**, not per customer total
- Lines starting with `#` are comments
- Empty or fully invalid input files still produce a valid output message

---

## Technologies used

- Python 3
- pytest
- Python standard library only (datetime, decimal, pathlib, dataclasses)

---

