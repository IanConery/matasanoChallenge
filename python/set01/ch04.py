import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto

DATA = Path(__file__).resolve().parents[2] / "data" / "set01" / "challenge_04.txt"


def solve() -> tuple[int, int, bytes]:
    lines = [ln for ln in DATA.read_text().splitlines() if ln.strip()]
    best_key, best_score, best_plaintext = 0, float("-inf"), b""
    for line in lines:
        data = crypto.hex_to_bytes(line)
        for key in range(256):
            plaintext = crypto.single_byte_xor(data, key)
            score = crypto.score_english(plaintext)
            if score > best_score:
                best_key, best_score, best_plaintext = key, score, plaintext
    return best_key, best_score, best_plaintext


def main() -> None:
    key, score, plaintext = solve()
    print(f"key: 0x{key:02x}  score: {score:.3f}")
    print(plaintext.decode())
    assert plaintext.rstrip() == b"Now that the party is jumping"
    print("OK")


if __name__ == "__main__":
    main()
