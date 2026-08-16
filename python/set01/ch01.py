"""Challenge 1: Convert hex to base64

The string:
49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

Should produce:
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

So go ahead and make that happen. You'll need to use this code for the rest
of the exercises.

Cryptopals Rule
Always operate on raw bytes, never on encoded strings. Only use hex and
base64 for pretty-printing.

https://cryptopals.com/sets/1/challenges/1
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto

HEX = (
    "49276d206b696c6c696e6720796f757220627261696e206c696b6520"
    "6120706f69736f6e6f7573206d757368726f6f6d"
)
EXPECTED = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"


def solve() -> str:
    return crypto.b64_encode(crypto.hex_to_bytes(HEX))


def main() -> None:
    result = solve()
    print(result)
    assert result == EXPECTED, f"expected {EXPECTED}"
    print("OK")


if __name__ == "__main__":
    main()
