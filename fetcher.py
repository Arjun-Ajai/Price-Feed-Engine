import yfinance as yf
import pandas as pd

class Fetcher:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()

    def fetch(self, period: str = "1y") -> list[dict]:
        df = yf.download(self.ticker, period=period, interval="1d", progress=False)
        if df.empty:
            raise ValueError(f"No data returned for {self.ticker}")
        df = df.reset_index()
        df.columns = [c.lower() for c in df.columns]
        return df[["date", "open", "high", "low", "close", "volume"]].to_dict(orient="records")
