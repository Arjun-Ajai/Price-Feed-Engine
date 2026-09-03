import time

class Feed:
    def __init__(self, db, ticker: str, speed: float = 1.0):
        self.db = db
        self.ticker = ticker.upper()
        self.speed = speed  # bars per second

    def stream(self):
        symbol_id = self.db.get_symbol_id(self.ticker)
        if not symbol_id:
            raise ValueError(f"{self.ticker} not in database. Run fetch first.")

        rows = self.db.conn.execute("""
            SELECT b.date, b.open, b.high, b.low, b.close, b.volume,
                   i.sma_20, i.sma_50, i.rsi_14
            FROM ohlcv_bars b
            LEFT JOIN indicators i ON i.bar_id = b.id
            WHERE b.symbol_id = ?
            ORDER BY b.date ASC
        """, (symbol_id,)).fetchall()

        for row in rows:
            yield dict(row)
            if self.speed < float('inf'):
                time.sleep(1.0 / self.speed)
