from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Dict, List, Set


#Constants 
MONEY_Q = Decimal("0.01")
DISCOUNT_RATE = Decimal("0.10")            
DISCOUNT_THRESHOLD = Decimal("500.00")     


@dataclass(frozen=True)
class OrderLine:
    """Represents a single parsed order line."""
    order_id: str
    customer: str
    product: str
    quantity: int
    unit_price: Decimal
    order_date: datetime

    @property
    def line_total(self) -> Decimal:
        """Quantity * unit_price, rounded to 2 decimal places."""
        return (Decimal(self.quantity) * self.unit_price).quantize(MONEY_Q, rounding=ROUND_HALF_UP)

    @property
    def discount(self) -> Decimal:
        """10% discount applied only when line_total > $500."""
        lt = self.line_total
        if lt > DISCOUNT_THRESHOLD:
            return (lt * DISCOUNT_RATE).quantize(MONEY_Q, rounding=ROUND_HALF_UP)
        return Decimal("0.00")

    @property
    def net_total(self) -> Decimal:
        """Gross line total minus discount."""
        return (self.line_total - self.discount).quantize(MONEY_Q, rounding=ROUND_HALF_UP)


@dataclass
class CustomerSummary:
    """Aggregated customer metrics for the summary report."""
    customer: str
    order_ids: Set[str]
    total_items: int
    gross_total: Decimal
    discount_total: Decimal

    @property
    def num_orders(self) -> int:
        """Number of distinct OrderIDs for this customer."""
        return len(self.order_ids)

    @property
    def net_total(self) -> Decimal:
        """Gross minus discount."""
        return (self.gross_total - self.discount_total).quantize(MONEY_Q, rounding=ROUND_HALF_UP)


def _parse_date(date_str: str) -> datetime:
    """Parse strict ISO date YYYY-MM-DD. Raises ValueError if invalid."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def _parse_money(value: str) -> Decimal:
    """Parse a money-like string into Decimal (2 dp). Raises InvalidOperation for non-numeric inputs."""
    d = Decimal(value)
    return d.quantize(MONEY_Q, rounding=ROUND_HALF_UP)


def parse_orders(input_path: Path, error_path: Path) -> List[OrderLine]:
    """
    Read order records from input_path and return a list of valid OrderLine objects.

    Malformed/invalid records are NOT fatal:
    - they are logged to error_path with a reason + original line
    - processing continues

    Skips:
    - empty lines
    - comment lines starting with '#'
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    valid: List[OrderLine] = []
    errors: List[str] = []

    for line_no, raw_line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 6:
            errors.append(f"Line {line_no}: wrong field count ({len(parts)}), expected 6 | {raw_line}")
            continue

        order_id, customer, product, qty_s, price_s, date_s = parts

        # Required string fields
        if not order_id or not customer or not product:
            errors.append(f"Line {line_no}: empty OrderID/CustomerName/ProductName | {raw_line}")
            continue

        # Quantity must be positive integer
        try:
            qty = int(qty_s)
            if qty <= 0:
                raise ValueError("quantity must be positive")
        except Exception as e:
            errors.append(f"Line {line_no}: invalid quantity ({qty_s}) - {e} | {raw_line}")
            continue

        # Unit price must be valid number and non-negative
        try:
            unit_price = _parse_money(price_s)
            if unit_price < 0:
                raise ValueError("unit price cannot be negative")
        except (InvalidOperation, ValueError) as e:
            errors.append(f"Line {line_no}: invalid unit price ({price_s}) - {e} | {raw_line}")
            continue

        # Date must match YYYY-MM-DD
        try:
            order_date = _parse_date(date_s)
        except Exception as e:
            errors.append(f"Line {line_no}: invalid date ({date_s}) - {e} | {raw_line}")
            continue

        valid.append(
            OrderLine(
                order_id=order_id,
                customer=customer,
                product=product,
                quantity=qty,
                unit_price=unit_price,
                order_date=order_date,
            )
        )

    # Always write error file (empty file is ok)
    error_path.write_text("\n".join(errors) + ("\n" if errors else ""), encoding="utf-8")
    return valid


def summarize_by_customer(lines: List[OrderLine]) -> Dict[str, CustomerSummary]:
    """
    Group valid order lines by customer and aggregate metrics:
    - distinct order count
    - total items
    - gross total
    - discount total
    - net total (derived)
    """
    summaries: Dict[str, CustomerSummary] = {}

    for ol in lines:
        if ol.customer not in summaries:
            summaries[ol.customer] = CustomerSummary(
                customer=ol.customer,
                order_ids=set(),
                total_items=0,
                gross_total=Decimal("0.00"),
                discount_total=Decimal("0.00"),
            )

        s = summaries[ol.customer]
        s.order_ids.add(ol.order_id)
        s.total_items += ol.quantity
        s.gross_total = (s.gross_total + ol.line_total).quantize(MONEY_Q, rounding=ROUND_HALF_UP)
        s.discount_total = (s.discount_total + ol.discount).quantize(MONEY_Q, rounding=ROUND_HALF_UP)

    return summaries


def format_report(summaries: Dict[str, CustomerSummary]) -> str:
    """
    Produce a fixed-width report with a grand total row.
    Customers are sorted alphabetically (case-insensitive).
    """
    headers = [
        ("Customer", 22),
        ("#Orders", 8),
        ("Items", 8),
        ("GrossTotal", 14),
        ("Discount", 14),
        ("NetTotal", 14),
    ]

    def money(d: Decimal) -> str:
        return f"{d.quantize(MONEY_Q, rounding=ROUND_HALF_UP):,.2f}"

    rows = sorted(summaries.values(), key=lambda x: x.customer.lower())

    # Grand totals
    grand_orders = 0
    grand_items = 0
    grand_gross = Decimal("0.00")
    grand_discount = Decimal("0.00")

    out: List[str] = []

    # Header
    header_line = "".join(name.ljust(width) for name, width in headers).rstrip()
    out.append(header_line)
    out.append("-" * sum(width for _, width in headers))

    # Rows
    for s in rows:
        grand_orders += s.num_orders
        grand_items += s.total_items
        grand_gross = (grand_gross + s.gross_total).quantize(MONEY_Q, rounding=ROUND_HALF_UP)
        grand_discount = (grand_discount + s.discount_total).quantize(MONEY_Q, rounding=ROUND_HALF_UP)

        out.append(
            s.customer.ljust(22)
            + str(s.num_orders).rjust(8)
            + str(s.total_items).rjust(8)
            + money(s.gross_total).rjust(14)
            + money(s.discount_total).rjust(14)
            + money(s.net_total).rjust(14)
        )

    out.append("-" * sum(width for _, width in headers))

    grand_net = (grand_gross - grand_discount).quantize(MONEY_Q, rounding=ROUND_HALF_UP)
    out.append(
        "GRAND TOTAL".ljust(22)
        + str(grand_orders).rjust(8)
        + str(grand_items).rjust(8)
        + money(grand_gross).rjust(14)
        + money(grand_discount).rjust(14)
        + money(grand_net).rjust(14)
    )

    return "\n".join(out) + "\n"


def generate_invoice_summary(input_file: str, output_file: str, error_file: str) -> None:
    """
    Main orchestration function:
    - parse
    - summarize
    - format
    - write outputs
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    error_path = Path(error_file)

    orders = parse_orders(input_path, error_path)

    if not orders:
        # Empty file or all invalid -> still generate a helpful report.
        output_path.write_text(
            "No valid orders found.\n"
            "If you expected data, check the error log for malformed records.\n",
            encoding="utf-8",
        )
        return

    summaries = summarize_by_customer(orders)
    output_path.write_text(format_report(summaries), encoding="utf-8")


if __name__ == "__main__":
    generate_invoice_summary("orders.txt", "summary_report.txt", "error_log.txt")
    print("Done. Generated summary_report.txt and error_log.txt")
