class SignalGenerator:
    def __init__(self, rsi_oversold=30, rsi_overbought=70):
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.prev_bar = None

    def evaluate(self, bar: dict) -> dict | None:
        signal = None
        sma20 = bar.get("sma_20")
        sma50 = bar.get("sma_50")
        rsi   = bar.get("rsi_14")

        if sma20 and sma50 and self.prev_bar:
            prev_sma20 = self.prev_bar.get("sma_20")
            prev_sma50 = self.prev_bar.get("sma_50")
            if prev_sma20 and prev_sma50:
                if prev_sma20 <= prev_sma50 and sma20 > sma50:
                    signal = {"side": "BUY", "reason": "SMA_CROSS_UP", "price": bar["close"]}
                elif prev_sma20 >= prev_sma50 and sma20 < sma50:
                    signal = {"side": "SELL", "reason": "SMA_CROSS_DOWN", "price": bar["close"]}

        if rsi and not signal:
            if rsi < self.rsi_oversold:
                signal = {"side": "BUY", "reason": "RSI_OVERSOLD", "price": bar["close"]}
            elif rsi > self.rsi_overbought:
                signal = {"side": "SELL", "reason": "RSI_OVERBOUGHT", "price": bar["close"]}

        self.prev_bar = bar
        return signal
