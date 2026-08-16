import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto

A = "1c0111001f010100061a024b53535009181c"
B = "686974207468652062756c6c277320657965"
EXPECTED = "746865206b696420646f6e277420706c6179"


def solve() -> str:
    return crypto.bytes_to_hex(crypto.xor_bytes(crypto.hex_to_bytes(A), crypto.hex_to_bytes(B)))


def main() -> None:
    result = solve()
    print(result)
    assert result == EXPECTED, f"expected {EXPECTED}"
    print("OK")


if __name__ == "__main__":
    main()
