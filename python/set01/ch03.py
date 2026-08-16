import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto

HEX = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
EXPECTED = "Cooking MC's like a pound of bacon"


def solve() -> tuple[int, bytes]:
    data = crypto.hex_to_bytes(HEX)
    best_key, best_score = 0, float("-inf")
    for key in range(256):
        plaintext = crypto.single_byte_xor(data, key)
        score = crypto.score_english(plaintext)
        if score > best_score:
            best_key, best_score = key, score
    return best_key, crypto.single_byte_xor(data, best_key)


def main() -> None:
    key, plaintext = solve()
    print(f"key: 0x{key:02x}")
    print(plaintext.decode())
    assert plaintext.decode() == EXPECTED, f"expected {EXPECTED}"
    print("OK")


if __name__ == "__main__":
    main()
