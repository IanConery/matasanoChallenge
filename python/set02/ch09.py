"""Challenge 9: Implement PKCS#7 padding

A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of
plaintext into ciphertext. But we almost never want to transform a single
block; we encrypt irregularly-sized messages.

One way we account for irregularly-sized messages is by padding, creating a
plaintext that is an even multiple of the blocksize. The most popular
padding scheme is called PKCS#7.

So: pad any block to a specific block length, by appending the number of
bytes of padding to the end of the block. For instance,

    "YELLOW SUBMARINE"
    ... padded to 20 bytes would be:
    "YELLOW SUBMARINE\\x04\\x04\\x04\\x04"

https://cryptopals.com/sets/2/challenges/9
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto


def main() -> None:
    data = b"YELLOW SUBMARINE"

    padded = crypto.pkcs7_pad(data, block_size=20)
    print(padded)
    assert padded == b"YELLOW SUBMARINE" + b"\x04" * 4

    for block_size in (8, 16):
        padded = crypto.pkcs7_pad(data, block_size)
        assert len(padded) % block_size == 0
        assert crypto.pkcs7_unpad(padded, block_size) == data
        print(f"block size {block_size}: {padded!r}")

    print("OK")


if __name__ == "__main__":
    main()
