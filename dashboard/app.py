from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Controle de Gastos", layout="wide")
st.title("Controle de Gastos — visão pessoal")
st.caption("Indicadores calculados pelo pipeline; esta tela não faz cálculos de negócio.")
monthly = pd.read_csv(ROOT / "data/marts/monthly_personal_spending.csv")
categories = pd.read_csv(ROOT / "data/marts/category_spend_summary.csv")
peak = monthly.loc[monthly["expenses"].idxmax()]
col1, col2, col3 = st.columns(3)
col1.metric("Mês de maior gasto", peak["month"], f"R$ {peak['expenses']:,.2f}")
col2.metric("Ganhos no período", f"R$ {monthly['income'].sum():,.2f}")
col3.metric("Saldo no período", f"R$ {monthly['balance'].sum():,.2f}")
left, right = st.columns(2)
with left:
    st.subheader("Evolução mensal")
    st.line_chart(monthly.set_index("month")[["expenses", "income", "balance"]])
with right:
    st.subheader("Gastos por grupo")
    st.dataframe(categories, use_container_width=True, hide_index=True)
st.subheader("Resumo mensal")
st.dataframe(monthly, use_container_width=True, hide_index=True)
