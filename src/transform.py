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
