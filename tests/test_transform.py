import pandas as pd
from src.transform import normalize_orders, build_order_spend


def test_normalize_orders_creates_month_without_database():
    orders = pd.DataFrame({"order_id": ["a"], "order_purchase_timestamp": ["2024-01-15 10:00:00"]})
    out = normalize_orders(orders)
    assert out.loc[0, "order_month"] == "2024-01"
    assert str(out.loc[0, "order_purchase_timestamp"].date()) == "2024-01-15"


def test_build_order_spend_aggregates_multiple_payment_rows():
    orders = pd.DataFrame({"order_id": ["a", "b"], "customer_id": ["c1", "c2"], "order_purchase_timestamp": ["2024-01-01", "2024-01-02"]})
    payments = pd.DataFrame({"order_id": ["a", "a", "b"], "payment_value": [10.0, 5.0, 20.0], "payment_installments": [1, 2, 1]})
    out = build_order_spend(orders, payments).sort_values("order_id")
    assert out["order_paid_value"].tolist() == [15.0, 20.0]
    assert out["payment_installments"].tolist() == [2, 1]


def test_summarize_monthly_spend_identifies_monthly_total():
    from src.transform import summarize_monthly_spend
    orders = pd.DataFrame({
        "order_id": ["a", "b", "c"],
        "order_month": ["2024-01", "2024-01", "2024-02"],
        "order_paid_value": [10.0, 20.0, 50.0],
    })
    out = summarize_monthly_spend(orders)
    peak = out.loc[out["total_paid"].idxmax()]
    assert peak["order_month"] == "2024-02"
    assert peak["total_paid"] == 50.0
