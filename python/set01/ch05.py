import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto

PLAINTEXT = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
KEY = b"ICE"
EXPECTED = (
    "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c"
    "2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b"
    "2027630c692b20283165286326302e27282f"
)


def solve() -> str:
    return crypto.bytes_to_hex(crypto.repeating_key_xor(PLAINTEXT.encode(), KEY))


def main() -> None:
    result = solve()
    print(result)
    assert result == EXPECTED, f"expected {EXPECTED}"
    print("OK")


if __name__ == "__main__":
    main()
