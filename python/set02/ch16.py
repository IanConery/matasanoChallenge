"""Challenge 16: CBC bitflipping attacks

Generate a random AES key.

Combine your padding code and CBC code to write two functions.

The first function should take an arbitrary input string, prepend the string:

    "comment1=cooking%20MCs;userdata="

.. and append the string:

    ";comment2=%20like%20a%20pound%20of%20bacon"

The function should quote out the ";" and "=" characters.

The function should then pad out the input to the 16-byte AES block length
and encrypt it under the random AES key.

The second function should decrypt the string and look for the characters
";admin=true;" (or, equivalently, decrypt, split the string on ";", convert
each resulting string into 2-tuples, and look for the "admin" tuple).

Return true or false based on whether the string exists.

If you've written the first function properly, it should not be possible to
provide user input to it that will generate the string the second function is
looking for. We'll have to break the crypto to do that.

Instead, modify the ciphertext (without knowledge of the AES key) to
accomplish this.

You're relying on the fact that in CBC mode, a 1-bit error in a ciphertext
block:

- Completely scrambles the block the error occurs in
- Produces the identical 1-bit error in the next ciphertext block

Stop and think for a second.

Before you implement this attack, answer this question: why does CBC mode
have this property?

Because P_i = ECB_dec(C_i) XOR C_{i-1}: C_{i-1} is XORed into the next
plaintext block after decryption, so changing it changes exactly those bits
of P_i.

https://cryptopals.com/sets/2/challenges/16
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import aes, crypto

KEY = os.urandom(16)
IV = os.urandom(16)
PREFIX = b"comment1=cooking%20MCs;userdata="  # exactly 32 bytes
SUFFIX = b";comment2=%20like%20a%20pound%20of%20bacon"


def profile_for(userdata: str) -> bytes:
    safe = userdata.replace(";", "%3B").replace("=", "%3D")
    plaintext = PREFIX + safe.encode() + SUFFIX
    return aes.aes_cbc_encrypt(KEY, IV, crypto.pkcs7_pad(plaintext))


def profile_is_admin(ciphertext: bytes) -> bool:
    plaintext = aes.aes_cbc_decrypt(KEY, IV, ciphertext)
    return b";admin=true;" in plaintext


def main() -> None:
    # A proper profile_for cannot be talked into emitting ;admin=true;
    for attempt in (";admin=true;", "admin=true", "%3Badmin%3Dtrue%3B"):
        assert not profile_is_admin(profile_for(attempt)), attempt
    print("no user input can produce ;admin=true; directly")

    # Bitflip attack:
    # We prepend 16 dummy bytes so that our payload "?admin?true" begins
    # exactly at the boundary of block 3 (offset 48).
    # In CBC mode, P_3 = ECB_dec(C_3) XOR C_2. By modifying C_2[0] and C_2[6],
    # we flip '?' (0x3f) in P_3 into ';' (0x3b) and '=' (0x3d) upon decryption,
    # without any knowledge of the secret key.
    userdata = "A" * 16 + "?admin?true"
    ct = bytearray(profile_for(userdata))
    assert not profile_is_admin(bytes(ct))

    # C_2 is at bytes 32..48; flipping bytes in C_2 alters P_3 at bytes 48..64
    ct[32] ^= ord("?") ^ ord(";")
    ct[32 + 6] ^= ord("?") ^ ord("=")
    forged = bytes(ct)

    assert profile_is_admin(forged)
    print("forged profile is admin:", profile_is_admin(forged))
    print(aes.aes_cbc_decrypt(KEY, IV, forged).decode(errors="replace"))
    print("OK")


if __name__ == "__main__":
    main()
