import pandas as pd
import numpy as np

def calculate_risk_and_return(price_df):
    returns = price_df.pct_change().dropna()

    metrics = pd.DataFrame({
        "Ticker": returns.columns,
        "Daily Volatility": returns.std().values,
        "Expected Annual Return": (returns.mean() * 252).values,
        "Risk Score (1–10)": (returns.std() * 100).clip(1, 10).round(1).values
    })

    return metrics
