"""Challenge 17: The CBC padding oracle

This is the best-known attack on modern block-cipher cryptography.

Combine your padding code and your CBC code to write two functions.

The first function should select at random one of the following 10 strings:

    MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
    MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
    MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
    MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
    MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
    MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
    MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
    MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
    MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
    MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93

... generate a random AES key (which it should save for all future
encryptions), pad the string out to the 16-byte AES block size and
CBC-encrypt it under that key, providing the caller the ciphertext and IV.

The second function should consume the ciphertext produced by the first
function, decrypt it, check its padding, and return true or false depending
on whether the padding is valid.

What you're doing here.
This pair of functions approximates AES-CBC encryption as its deployed
serverside in web applications; the second function models the server's
consumption of an encrypted session token, as if it was a cookie.

It turns out that it's possible to decrypt the ciphertexts provided by the
first function.

The decryption here depends on a side-channel leak by the decryption
function. The leak is the error message that the padding is valid or not.

You can find 100 web pages on how this attack works, so I won't re-explain
it. What I'll say is this:

The fundamental insight behind this attack is that the byte 01h is valid
padding, and occur in 1/256 trials of "randomized" plaintexts produced by
decrypting a tampered ciphertext.

02h in isolation is not valid padding.

02h 02h is valid padding, but is much less likely to occur randomly than
01h.

03h 03h 03h is even less likely.

So you can assume that if you corrupt a decryption AND it had valid padding,
you know what that padding byte is.

It is easy to get tripped up on the fact that CBC plaintexts are "padded".
Padding oracles have nothing to do with the actual padding on a CBC
plaintext. It's an attack that targets a specific bit of code that handles
decryption. You can mount a padding oracle on any CBC block, whether it's
padded or not.

https://cryptopals.com/sets/3/challenges/17
"""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import aes, crypto

STRINGS = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]


class PaddingOracle:
    """The challenge's pair of functions as a local server.

    The key is generated once and saved for all future encryptions, per the
    spec. `plaintext` is kept only so main() can verify the attack.
    """

    def __init__(self) -> None:
        self.key: bytes | None = None
        self.plaintext: bytes | None = None

    def generate(self) -> tuple[bytes, bytes]:
        if self.key is None:
            self.key = os.urandom(16)
        self.plaintext = crypto.b64_decode(random.choice(STRINGS))
        iv = os.urandom(16)
        ciphertext = aes.aes_cbc_encrypt(self.key, iv, crypto.pkcs7_pad(self.plaintext))
        return iv, ciphertext

    def is_valid(self, ciphertext: bytes) -> bool:
        """Decrypt (first 16 bytes = IV) and report whether padding is valid."""
        if self.key is None or len(ciphertext) < 32 or len(ciphertext) % 16:
            return False
        try:
            crypto.pkcs7_unpad(aes.aes_cbc_decrypt(self.key, ciphertext[:16], ciphertext[16:]))
            return True
        except ValueError:
            return False


def _recover_first_byte(oracle: PaddingOracle, prev: bytes, target: bytes) -> int:
    """Recover the rightmost byte of the block (padding length k = 1).

    At k = 1 no byte is forced to the right of the target, so a wrong guess
    is also accepted when the real plaintext's own tail happens to be a valid
    longer padding (always true for the final block of a message). The true
    byte is the only guess under which the fake plaintext ends in exactly one
    padding byte, i.e. the oracle accepts every value of the byte to the
    left; any other accepted guess accepts at most one such value.
    """
    candidates = []
    for g in range(256):
        forged = bytearray(prev)
        forged[15] = g ^ prev[15] ^ 1
        if oracle.is_valid(bytes(forged) + target):
            candidates.append(g)
    assert candidates, "padding oracle never accepted the rightmost byte"

    confirmed = []
    for g in candidates:
        accepts = 0
        for left in range(256):
            forged = bytearray(prev)
            forged[15] = g ^ prev[15] ^ 1
            forged[14] = left ^ prev[14] ^ 2
            if oracle.is_valid(bytes(forged) + target):
                accepts += 1
        if accepts == 256:
            confirmed.append(g)
    assert len(confirmed) == 1, f"ambiguous rightmost byte: {confirmed}"
    return confirmed[0]


def padding_oracle_attack(oracle: PaddingOracle, iv: bytes, ciphertext: bytes) -> bytes:
    """Recover the plaintext block by block, byte by byte, right to left.

    For the byte at position p (padding length k = 16 - p), forge a previous
    block so the decrypted fake plaintext's last k bytes must equal k
    repeated: the already-recovered bytes are forced to k directly, and the
    target byte is forced to k only when the guess equals the real byte.
    For k >= 2 the forced tail makes the answer unique; the k = 1 byte is
    handled by _recover_first_byte.
    """
    plaintext = b""
    prev = iv
    for i in range(0, len(ciphertext), 16):
        target = ciphertext[i : i + 16]
        block = bytearray(16)
        block[15] = _recover_first_byte(oracle, prev, target)
        for p in range(14, -1, -1):
            k = 16 - p
            for g in range(256):
                forged = bytearray(prev)
                for q in range(p + 1, 16):
                    forged[q] = block[q] ^ prev[q] ^ k
                forged[p] = g ^ prev[p] ^ k
                if oracle.is_valid(bytes(forged) + target):
                    block[p] = g
                    break
            else:
                raise AssertionError(f"padding oracle never accepted position {p}")
        plaintext += bytes(block)
        prev = target
    return crypto.pkcs7_unpad(plaintext)


def main() -> None:
    oracle = PaddingOracle()
    iv, ciphertext = oracle.generate()
    plaintext = padding_oracle_attack(oracle, iv, ciphertext)
    print(plaintext.decode())
    assert plaintext == oracle.plaintext
    assert plaintext in [crypto.b64_decode(s) for s in STRINGS]
    print("OK")


if __name__ == "__main__":
    main()
