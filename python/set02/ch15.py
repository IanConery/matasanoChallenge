"""Challenge 15: PKCS#7 padding validation

Write a function that takes a plaintext, determines if it has valid PKCS#7
padding, and strips the padding off.

The string:

    "ICE ICE BABY\\x04\\x04\\x04\\x04"

... has valid padding, and produces the result "ICE ICE BABY".

The string:

    "ICE ICE BABY\\x05\\x05\\x05\\x05"

... does not have valid padding, nor does:

    "ICE ICE BABY\\x01\\x02\\x03\\x04"

If you are writing in a language with exceptions, like Python or Ruby, make
your function throw an exception on bad padding.

Crypto nerds know where we're going with this. Bear with us.

https://cryptopals.com/sets/2/challenges/15
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto


def main() -> None:
    # Valid padding.
    assert crypto.pkcs7_unpad(b"ICE ICE BABY" + b"\x04" * 4) == b"ICE ICE BABY"
    print("ICE ICE BABY\\x04\\x04\\x04\\x04 -> ICE ICE BABY")

    # Invalid padding: wrong pad length, mixed pad bytes, no padding,
    # pad length exceeds the block, not block-aligned.
    invalid = [
        b"ICE ICE BABY" + b"\x05" * 4,
        b"ICE ICE BABY" + b"\x01\x02\x03\x04",
        b"ICE ICE BABY",
        b"\x00",
        b"\x11" * 15,
        b"A" * 17,
    ]
    for data in invalid:
        try:
            crypto.pkcs7_unpad(data)
        except ValueError:
            print(f"{data!r} -> rejected")
        else:
            raise SystemExit(f"should have raised: {data!r}")

    print("OK")


if __name__ == "__main__":
    main()
