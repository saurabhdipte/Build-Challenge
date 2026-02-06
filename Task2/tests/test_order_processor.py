from pathlib import Path
from decimal import Decimal
import pytest

from order_processor import (
    OrderLine,
    parse_orders,
    summarize_by_customer,
    format_report,
)


def write_tmp_file(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def test_orderline_discount_threshold_not_applied_when_equal_500():
    ol = OrderLine(
        order_id="ORDX",
        customer="Test",
        product="X",
        quantity=1,
        unit_price=Decimal("500.00"),
        order_date=__import__("datetime").datetime(2024, 1, 1),
    )
    assert ol.line_total == Decimal("500.00")
    assert ol.discount == Decimal("0.00")
    assert ol.net_total == Decimal("500.00")


def test_orderline_discount_applied_when_over_500():
    ol = OrderLine(
        order_id="ORDY",
        customer="Test",
        product="Y",
        quantity=1,
        unit_price=Decimal("500.01"),
        order_date=__import__("datetime").datetime(2024, 1, 1),
    )
    assert ol.line_total == Decimal("500.01")
    assert ol.discount == Decimal("50.00")  # 10% of 500.01 = 50.001 -> rounds to 50.00
    assert ol.net_total == Decimal("450.01")


def test_parse_orders_skips_comments_and_blank_lines(tmp_path: Path):
    content = """
# comment
     
ORD001|John Smith|Laptop|1|999.99|2024-03-15
"""
    inp = write_tmp_file(tmp_path, "in.txt", content)
    err = tmp_path / "err.txt"

    orders = parse_orders(inp, err)
    assert len(orders) == 1
    assert orders[0].order_id == "ORD001"
    assert err.read_text(encoding="utf-8").strip() == ""


def test_parse_orders_logs_malformed_field_count(tmp_path: Path):
    content = "ORD001|John Smith|Laptop|1|999.99\n"
    inp = write_tmp_file(tmp_path, "in.txt", content)
    err = tmp_path / "err.txt"

    orders = parse_orders(inp, err)
    assert len(orders) == 0
    e = err.read_text(encoding="utf-8")
    assert "wrong field count" in e


@pytest.mark.parametrize(
    "bad_line, expected_phrase",
    [
        ("ORD001|John Smith|Laptop|-1|999.99|2024-03-15", "invalid quantity"),
        ("ORD001|John Smith|Laptop|0|999.99|2024-03-15", "invalid quantity"),
        ("ORD001|John Smith|Laptop|1|abc|2024-03-15", "invalid unit price"),
        ("ORD001|John Smith|Laptop|1|999.99|not-a-date", "invalid date"),
        ("ORD001||Laptop|1|999.99|2024-03-15", "empty OrderID/CustomerName/ProductName"),
        ("ORD001|John Smith|Laptop|1|-1.00|2024-03-15", "invalid unit price"),
    ],
)
def test_parse_orders_logs_invalid_values(tmp_path: Path, bad_line: str, expected_phrase: str):
    inp = write_tmp_file(tmp_path, "in.txt", bad_line + "\n")
    err = tmp_path / "err.txt"

    orders = parse_orders(inp, err)
    assert orders == []
    assert expected_phrase in err.read_text(encoding="utf-8")


def test_summarize_by_customer_aggregates_correctly():
    dt = __import__("datetime").datetime(2024, 1, 1)
    lines = [
        OrderLine("A1", "Alice", "Item1", 2, Decimal("10.00"), dt),  # gross 20
        OrderLine("A2", "Alice", "Item2", 1, Decimal("600.00"), dt), # gross 600 discount 60
        OrderLine("B1", "Bob", "Item3", 3, Decimal("5.00"), dt),     # gross 15
    ]

    s = summarize_by_customer(lines)
    assert set(s.keys()) == {"Alice", "Bob"}

    alice = s["Alice"]
    assert alice.num_orders == 2
    assert alice.total_items == 3
    assert alice.gross_total == Decimal("620.00")
    assert alice.discount_total == Decimal("60.00")
    assert alice.net_total == Decimal("560.00")

    bob = s["Bob"]
    assert bob.num_orders == 1
    assert bob.total_items == 3
    assert bob.gross_total == Decimal("15.00")
    assert bob.discount_total == Decimal("0.00")
    assert bob.net_total == Decimal("15.00")


def test_format_report_contains_grand_total_row():
    dt = __import__("datetime").datetime(2024, 1, 1)
    lines = [
        OrderLine("A1", "Alice", "Item1", 1, Decimal("100.00"), dt),
        OrderLine("B1", "Bob", "Item2", 1, Decimal("200.00"), dt),
    ]
    summaries = summarize_by_customer(lines)
    report = format_report(summaries)

    assert "GRAND TOTAL" in report
    assert "Alice" in report
    assert "Bob" in report


def test_parse_orders_empty_file(tmp_path: Path):
    inp = write_tmp_file(tmp_path, "in.txt", "")
    err = tmp_path / "err.txt"
    orders = parse_orders(inp, err)
    assert orders == []
    assert err.read_text(encoding="utf-8") == ""
