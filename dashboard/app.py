from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Controle de Gastos", layout="wide")
st.title("Controle de Gastos — indicadores Olist")
st.caption("O painel lê somente a camada de indicadores; os cálculos são feitos no pipeline SQL.")
monthly = pd.read_csv(ROOT / "data/marts/monthly_spend_summary.csv")
payment = pd.read_csv(ROOT / "data/marts/payment_method_mix.csv")

peak = monthly.loc[monthly["total_paid"].idxmax()]
col1, col2, col3 = st.columns(3)
col1.metric("Mês de maior gasto", peak["order_month"], f"R$ {peak['total_paid']:,.2f}")
col2.metric("Pedidos no mês", f"{int(peak['orders']):,}")
col3.metric("Ticket médio", f"R$ {peak['avg_ticket']:,.2f}")

left, right = st.columns(2)
with left:
    st.subheader("Evolução do gasto por mês")
    st.line_chart(monthly.set_index("order_month")["total_paid"])
with right:
    st.subheader("Formas de pagamento")
    st.dataframe(payment, use_container_width=True, hide_index=True)

st.subheader("Indicadores mensais")
st.dataframe(monthly, use_container_width=True, hide_index=True)
