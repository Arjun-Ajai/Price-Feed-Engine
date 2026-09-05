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
