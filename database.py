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
        
