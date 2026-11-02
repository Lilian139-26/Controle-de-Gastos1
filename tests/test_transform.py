import pandas as pd
from src.transform import normalize_transactions, monthly_personal_summary


def test_normalize_transactions_types_month_amount_and_recurring():
    data = pd.DataFrame({
        "month": ["2026-01"], "amount": ["1200,00"], "is_recurring": ["true"]
    })
    data["amount"] = data["amount"].str.replace(",", ".").astype(float)
    out = normalize_transactions(data)
    assert out.loc[0, "month"] == "2026-01"
    assert out.loc[0, "amount"] == 1200.0
    assert bool(out.loc[0, "is_recurring"]) is True


def test_monthly_summary_calculates_personal_balance():
    data = pd.DataFrame([
        {"month": "2026-01", "expense_type": "expense", "amount": 1200, "is_recurring": False},
        {"month": "2026-01", "expense_type": "expense", "amount": 300, "is_recurring": False},
        {"month": "2026-01", "expense_type": "income", "amount": 4500, "is_recurring": False},
    ])
    out = monthly_personal_summary(data)
    assert out.loc[0, "expenses"] == 1500
    assert out.loc[0, "income"] == 4500
    assert out.loc[0, "balance"] == 3000
