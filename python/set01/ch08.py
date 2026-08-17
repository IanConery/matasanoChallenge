"""Challenge 8: Detect AES in ECB mode

In the data/set01/challenge_08.txt file are a bunch of hex-encoded
ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and
deterministic; the same 16 byte plaintext block will always produce the
same 16 byte ciphertext.

https://cryptopals.com/sets/1/challenges/8
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto

DATA = Path(__file__).resolve().parents[2] / "data" / "set01" / "challenge_08.txt"


def solve() -> list[int]:
    lines = [ln for ln in DATA.read_text().splitlines() if ln.strip()]
    return [i for i, line in enumerate(lines) if crypto.detect_ecb(crypto.hex_to_bytes(line))]


def main() -> None:
    hits = solve()
    for i in hits:
        print(f"line {i}: ECB")
    assert len(hits) == 1
    print("OK")


if __name__ == "__main__":
    main()
