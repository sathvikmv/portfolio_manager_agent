import yfinance as yf
import pandas as pd

def fetch_price_history(tickers):
    """
    Fetch daily closing prices for multiple tickers.
    Works for both stocks and crypto.
    Returns a DataFrame with columns: Date, Ticker, Close.
    """
    all_data = []

    for t in tickers:
        try:
            # Try stock directly
            data = yf.Ticker(t).history(period="1y")
            if data.empty:
                raise Exception("Not a stock")
        except:
            # If not stock → assume crypto (BTC → BTC-USD)
            data = yf.Ticker(t + "-USD").history(period="1y")

        df_temp = pd.DataFrame({
            "Date": data.index,
            "Ticker": t,
            "Close": data["Close"].values
        })

        all_data.append(df_temp)

    return pd.concat(all_data, ignore_index=True)



# ---------------------------------------------------------
# ADD THIS FUNCTION BELOW (FIXES LIVE PRICE ISSUE)
# ---------------------------------------------------------

def fetch_live_price(symbol):
    """
    Fetch live price in INR for stocks and crypto.
    Crypto price is fetched in USD then converted to INR.
    """
    # ----- Try stock (INR brokers on Yahoo) -----
    try:
        data = yf.Ticker(symbol).history(period="1d")
        if not data.empty:
            return round(float(data["Close"].iloc[-1]), 2)
    except:
        pass

    # ----- Try crypto (BTC -> BTC-USD) -----
    try:
        data = yf.Ticker(symbol + "-USD").history(period="1d")
        usd_price = float(data["Close"].iloc[-1])

        # USD → INR conversion
        fx = yf.Ticker("USDINR=X").history(period="1d")
        usd_inr = float(fx["Close"].iloc[-1])

        return round(usd_price * usd_inr, 2)
    except:
        return 0.0
