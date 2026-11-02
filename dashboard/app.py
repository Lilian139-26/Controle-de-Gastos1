from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Controle de Gastos", layout="wide")
st.title("Controle de Gastos — indicadores Olist")
st.caption("Visualização dos marts produzidos pelo pipeline; nenhum cálculo de negócio é feito nesta tela.")
monthly = pd.read_csv(ROOT / "data/marts/monthly_spend_by_state.csv")
payment = pd.read_csv(ROOT / "data/marts/payment_method_mix.csv")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Valor pago por mês")
    chart = monthly.groupby("order_month", as_index=False)["total_paid"].sum().set_index("order_month")
    st.line_chart(chart)
with col2:
    st.subheader("Mix de pagamento")
    st.dataframe(payment, use_container_width=True, hide_index=True)
st.subheader("Gasto mensal por estado")
st.dataframe(monthly, use_container_width=True, hide_index=True)
