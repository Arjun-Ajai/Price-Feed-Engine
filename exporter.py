class Exporter:
    def __init__(self, ticker: str, quantity: float = 100.0):
        self.ticker = ticker
        self.quantity = quantity

    def to_csv(self, signals: list[dict], path: str):
        with open(path, "w") as f:
            for s in signals:
                f.write(f"{self.ticker}|{s['side']}|{self.quantity}|{s['price']}|{s['date']}\n")
        print(f"Wrote {len(signals)} signals to {path}")
