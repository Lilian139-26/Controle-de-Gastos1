import pandas as pd


def normalize_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    out = transactions.copy()
    out["month"] = pd.to_datetime(out["month"], format="%Y-%m").dt.to_period("M").astype("string")
    out["amount"] = pd.to_numeric(out["amount"], errors="raise")
    out["is_recurring"] = out["is_recurring"].astype(str).str.lower().eq("true")
    return out


def monthly_personal_summary(transactions: pd.DataFrame) -> pd.DataFrame:
    out = normalize_transactions(transactions)
    expenses = out.loc[out["expense_type"].eq("expense")].groupby("month")["amount"].sum()
    income = out.loc[out["expense_type"].eq("income")].groupby("month")["amount"].sum()
    count = out.groupby("month").size().rename("launches")
    result = pd.concat([expenses.rename("expenses"), income.rename("income"), count], axis=1).fillna(0).reset_index()
    result["balance"] = result["income"] - result["expenses"]
    return result.sort_values("month").reset_index(drop=True)
