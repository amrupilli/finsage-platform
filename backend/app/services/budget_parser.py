import re


def extract_budget_amount(budget_text: str) -> float:
    if not budget_text or not budget_text.strip():
        raise ValueError("Budget text is empty.")

    normalised_text = budget_text.replace(",", "").strip()

    matches = re.findall(r"\d+(?:\.\d+)?", normalised_text)

    if not matches:
        raise ValueError("Could not extract a numeric budget amount.")

    amount = float(matches[0])

    if amount <= 0:
        raise ValueError("Budget amount must be greater than zero.")

    if amount > 1_000_000:
        raise ValueError("Budget amount is unrealistically large for this educational prototype.")

    return round(amount, 2)