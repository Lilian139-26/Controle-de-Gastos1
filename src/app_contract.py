"""Adaptador entre o formato salvo pelo app e uma tabela analítica.

O app salva anos com as coleções cartoes, contasFixas, contasAdicionais e ganhos.
Este módulo não contém dados pessoais: ele só define como um export sanitizado
pode entrar na camada raw/refined do pipeline.
"""
from __future__ import annotations

from typing import Any
import pandas as pd


COLLECTIONS = {
    "cartoes": "cartao",
    "contasFixas": "conta_fixa",
    "contasAdicionais": "conta_adicional",
}


def app_state_to_transactions(state: dict[str, Any]) -> pd.DataFrame:
    """Converte um export de um ano do app em linhas mensais normalizadas."""
    rows: list[dict[str, Any]] = []
    for collection, expense_type in COLLECTIONS.items():
        for item in state.get(collection, []) or []:
            name = str(item.get("nome", "")).strip()
            for month, value in (item.get("meses", {}) or {}).items():
                rows.append({
                    "source": "controle_de_gastos",
                    "expense_type": expense_type,
                    "item_name": name,
                    "month": str(month),
                    "amount": float(value or 0),
                })
    for month, value in (state.get("ganhos", {}) or {}).items():
        rows.append({
            "source": "controle_de_gastos",
            "expense_type": "income",
            "item_name": "ganhos",
            "month": str(month),
            "amount": float(value or 0),
        })
    return pd.DataFrame(rows, columns=["source", "expense_type", "item_name", "month", "amount"])


def summarize_app_month(transactions: pd.DataFrame) -> pd.DataFrame:
    """Cria indicadores do app sem depender de banco ou de dados pessoais."""
    if transactions.empty:
        return pd.DataFrame(columns=["month", "expenses", "income", "balance"])
    expenses = transactions[transactions["expense_type"] != "income"].groupby("month")["amount"].sum()
    income = transactions[transactions["expense_type"] == "income"].groupby("month")["amount"].sum()
    out = pd.concat([expenses.rename("expenses"), income.rename("income")], axis=1).fillna(0).reset_index()
    out["balance"] = out["income"] - out["expenses"]
    return out.sort_values("month").reset_index(drop=True)
