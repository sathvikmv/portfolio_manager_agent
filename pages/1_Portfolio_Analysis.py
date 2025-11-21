import streamlit as st
import pandas as pd

from market_data import fetch_live_price, fetch_price_history
from analytics import calculate_risk_and_return
from ai_engine import investment_recommendation

st.title("📈 Portfolio Analysis")

# --------------------------
# STEP 1 — ENTER TICKERS
# --------------------------
st.subheader("Step 1: Enter Assets")

tickers_input = st.text_input(
    "Enter ticker symbols (comma separated):",
    value="AAPL, MSFT, TSLA",
)

if tickers_input.strip() == "":
    st.info("Enter at least one ticker to continue.")
    st.stop()

tickers = [t.strip().upper() for t in tickers_input.split(",")]

# --------------------------
# STEP 2 — ENTER AMOUNTS
# --------------------------
st.subheader("Step 2: Enter Investment Amount per Asset")

amounts = {}
for t in tickers:
    amounts[t] = st.number_input(
        f"Amount invested in {t} (₹)",
        min_value=0,
        value=0,
    )

# --------------------------
# ANALYZE BUTTON
# --------------------------
if st.button("🔍 Analyze Portfolio"):

    # ---- LIVE PRICES & UNITS ----
    st.subheader("📌 Live Prices & Units")

    prices = {t: fetch_live_price(t) for t in tickers}

    df_units = pd.DataFrame({
        "Ticker": tickers,
        "Invested (₹)": [amounts[t] for t in tickers],
        "Live Price (₹)": [prices[t] for t in tickers],
    })

    df_units["Units Owned"] = (
        df_units["Invested (₹)"] / df_units["Live Price (₹)"]
    ).round(6)

    st.dataframe(df_units)

    # ---- RISK & RETURN ----
    st.subheader("📌 Risk & Return Metrics")

    # 1️⃣ Fetch raw history
    price_history = fetch_price_history(tickers)

    # 2️⃣ Pivot to wide format
    price_pivot = price_history.pivot(
        index="Date",
        columns="Ticker",
        values="Close"
    )

    # 3️⃣ Calculate risk & return
    df_risk = calculate_risk_and_return(price_pivot)

    st.dataframe(df_risk)

    # ---- AI RECOMMENDATION ----
    st.subheader("🤖 AI Recommendation")

    advice = investment_recommendation(df_units, df_risk)
    st.write(advice)

else:
    st.warning("Click **Analyze Portfolio** after entering all data.")
