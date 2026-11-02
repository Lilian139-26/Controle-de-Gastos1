import pandas as pd


def normalize_orders(orders: pd.DataFrame) -> pd.DataFrame:
    out = orders.copy()
    out["order_purchase_timestamp"] = pd.to_datetime(out["order_purchase_timestamp"], errors="coerce")
    out["order_month"] = out["order_purchase_timestamp"].dt.to_period("M").astype("string")
    return out


def build_order_spend(orders: pd.DataFrame, payments: pd.DataFrame) -> pd.DataFrame:
    p = payments.groupby("order_id", as_index=False).agg(
        order_paid_value=("payment_value", "sum"),
        payment_installments=("payment_installments", "max"),
    )
    out = normalize_orders(orders).merge(p, on="order_id", how="left")
    out["order_paid_value"] = out["order_paid_value"].fillna(0.0)
    out["payment_installments"] = out["payment_installments"].fillna(0).astype(int)
    return out

def summarize_monthly_spend(order_spend: pd.DataFrame) -> pd.DataFrame:
    """Agrega gastos por mês para responder qual mês concentrou mais valor."""
    out = order_spend.groupby("order_month", as_index=False).agg(
        orders=("order_id", "nunique"),
        total_paid=("order_paid_value", "sum"),
    )
    out["avg_ticket"] = out["total_paid"] / out["orders"]
    return out.sort_values("order_month").reset_index(drop=True)

