import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Crypto.Cipher import AES
from lib import crypto

DATA = Path(__file__).resolve().parents[2] / "data" / "set01" / "challenge_07.txt"
KEY = b"YELLOW SUBMARINE"


def solve() -> str:
    ciphertext = crypto.b64_decode(DATA.read_text())
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.decrypt(ciphertext).decode()


def main() -> None:
    plaintext = solve()
    print(plaintext)
    assert "Play that funky music" in plaintext and "Vanilla Ice" in plaintext
    print("OK")


if __name__ == "__main__":
    main()
