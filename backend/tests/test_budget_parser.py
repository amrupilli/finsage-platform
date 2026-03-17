import pytest

from app.services.budget_parser import extract_budget_amount


def test_extract_budget_amount_simple() -> None:
    assert extract_budget_amount("100 pounds") == 100.0


def test_extract_budget_amount_with_comma() -> None:
    assert extract_budget_amount("1,250 pounds") == 1250.0


def test_extract_budget_amount_raises_for_empty_text() -> None:
    with pytest.raises(ValueError, match="Budget text is empty"):
        extract_budget_amount("")


def test_extract_budget_amount_raises_for_missing_number() -> None:
    with pytest.raises(ValueError, match="Could not extract a numeric budget amount"):
        extract_budget_amount("a small amount")


def test_extract_budget_amount_raises_for_large_value() -> None:
    with pytest.raises(ValueError, match="unrealistically large"):
        extract_budget_amount("1000001 pounds")