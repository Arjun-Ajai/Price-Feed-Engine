import sqlite3

class Database:
    def __init__(self, path: str = "pricefeed.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.init_schema()

    def init_schema(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS symbols (
                id INTEGER PRIMARY KEY,
                ticker TEXT UNIQUE NOT NULL,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS ohlcv_bars (
                id INTEGER PRIMARY KEY,
                symbol_id INTEGER NOT NULL REFERENCES symbols(id),
                date DATE NOT NULL,
                open REAL, high REAL, low REAL, close REAL, volume INTEGER,
                UNIQUE(symbol_id, date)
            );
            CREATE TABLE IF NOT EXISTS indicators (
                id INTEGER PRIMARY KEY,
                bar_id INTEGER NOT NULL REFERENCES ohlcv_bars(id),
                sma_20 REAL, sma_50 REAL, rsi_14 REAL
            );
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY,
                symbol_id INTEGER NOT NULL REFERENCES symbols(id),
                date DATE, side TEXT, reason TEXT, price REAL
            );
        """)
        self.conn.commit()

    def save_symbol(self, ticker: str) -> int:
        self.conn.execute(
            "INSERT OR IGNORE INTO symbols (ticker) VALUES (?)", (ticker,))
        self.conn.commit()
        return self.get_symbol_id(ticker)

    def get_symbol_id(self, ticker: str) -> int | None:
        row = self.conn.execute(
            "SELECT id FROM symbols WHERE ticker = ?", (ticker,)).fetchone()
        return row["id"] if row else None

    def save_bars(self, symbol_id: int, bars: list[dict]) -> None:
        self.conn.executemany("""
            INSERT OR IGNORE INTO ohlcv_bars
            (symbol_id, date, open, high, low, close, volume)
            VALUES (:symbol_id, :date, :open, :high, :low, :close, :volume)
        """, [{"symbol_id": symbol_id, **b} for b in bars])
        self.conn.commit()

    def save_indicators(self, bar_id: int, sma_20, sma_50, rsi_14):
        self.conn.execute("""
            INSERT OR REPLACE INTO indicators (bar_id, sma_20, sma_50, rsi_14)
            VALUES (?, ?, ?, ?)
        """, (bar_id, sma_20, sma_50, rsi_14))
        self.conn.commit()

    def get_bars_with_ids(self, symbol_id: int) -> list[dict]:
        rows = self.conn.execute("""
            SELECT id, date, open, high, low, close, volume
            FROM ohlcv_bars WHERE symbol_id = ? ORDER BY date ASC
        """, (symbol_id,)).fetchall()
        return [dict(r) for r in rows]

    def list_symbols(self) -> list[dict]:
        rows = self.conn.execute("""
                                 SELECT s.ticker,
                                        COUNT(b.id) as bar_count,
                                        MIN(b.date) as from_date,
                                        MAX(b.date) as to_date
                                 FROM symbols s
                                          JOIN ohlcv_bars b ON b.symbol_id = s.id
                                 GROUP BY s.id
                                 """).fetchall()
        return [dict(r) for r in rows]