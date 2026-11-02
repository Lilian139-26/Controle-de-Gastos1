import pandas as pd

from src.app_contract import app_state_to_transactions, summarize_app_month


def test_app_state_maps_expenses_and_income_to_rows():
    state = {
        "cartoes": [{"nome": "Cartão exemplo", "meses": {"2026-01": 100.0}}],
        "contasFixas": [{"nome": "Aluguel exemplo", "meses": {"2026-01": 800.0}}],
        "contasAdicionais": [],
        "ganhos": {"2026-01": 2000.0},
    }
    out = app_state_to_transactions(state)
    assert len(out) == 3
    assert set(out["expense_type"]) == {"cartao", "conta_fixa", "income"}


def test_app_summary_calculates_balance_from_normalized_rows():
    rows = pd.DataFrame([
        {"month": "2026-01", "expense_type": "cartao", "amount": 100.0},
        {"month": "2026-01", "expense_type": "conta_fixa", "amount": 800.0},
        {"month": "2026-01", "expense_type": "income", "amount": 2000.0},
    ])
    out = summarize_app_month(rows)
    assert out.loc[0, "expenses"] == 900.0
    assert out.loc[0, "income"] == 2000.0
    assert out.loc[0, "balance"] == 1100.0
