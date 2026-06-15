import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="트레이딩 서비스", layout="wide")

st.title("📊 실전 트레이딩 대시보드")

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

latest = data["assets"][-1]["total"]
first = data["assets"][0]["total"]

profit = latest - first
rate = (profit / first) * 100

st.metric(
    "💰 총 자산",
    f"{latest:,.0f} 원",
    f"{rate:.2f}%"
)

st.subheader("📈 자산 그래프")
df = pd.DataFrame(data["assets"])
st.line_chart(df.set_index("time")["total"])

st.subheader("📒 거래 내역")

trades = pd.DataFrame(data["trades"])

if not trades.empty:
    st.dataframe(trades.tail(20))

    st.subheader("🔥 최근 거래")
    st.write(trades.tail(5))