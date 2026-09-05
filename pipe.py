import subprocess

class CppPipe:
    def __init__(self, binary_path: str):
        self.process = subprocess.Popen(
            [binary_path, "--stream"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        print(f"C++ engine started: {binary_path}")

    def send_signal(self, ticker: str, side: str, qty: float, price: float) -> str:
        line = f"{ticker}|{side}|{qty}|{price}\n"
        self.process.stdin.write(line)
        self.process.stdin.flush()
        fill = self.process.stdout.readline().strip()
        return fill

    def close(self):
        self.process.stdin.write("quit\n")
        self.process.stdin.flush()
        self.process.wait()
