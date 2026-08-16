"""Challenge 13: ECB cut-and-paste

Write a k=v parsing routine, as if for a structured cookie. The routine
should take:

    foo=bar&baz=qux&zap=zazzle

... and produce:

    {
      foo: 'bar',
      baz: 'qux',
      zap: 'zazzle'
    }

(you know, the object; I don't care if you convert it to JSON).

Now write a function that encodes a user profile in that format, given an
email address. You should have something like:

    profile_for("foo@bar.com")

... and it should produce:

    {
      email: 'foo@bar.com',
      uid: 10,
      role: 'user'
    }

... encoded as:

    email=foo@bar.com&uid=10&role=user

Your "profile_for" function should not allow encoding metacharacters (& and
=). Eat them, quote them, whatever you want to do, but don't let people set
their email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

- Encrypt the encoded user profile under the key; "provide" that to the
  "attacker".
- Decrypt the encoded user profile and parse it.

Using only the user input to profile_for() (as an oracle to generate "valid"
ciphertexts) and the ciphertexts themselves, make a role=admin profile.

https://cryptopals.com/sets/2/challenges/13
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import aes, crypto

KEY = os.urandom(16)


def parse_profile(data: bytes) -> dict:
    profile = {}
    for pair in data.split(b"&"):
        if b"=" in pair:
            key, value = pair.split(b"=", 1)
            profile[key.decode()] = value.decode(errors="replace")
    return profile


def profile_for(email: str) -> bytes:
    safe = email.replace("&", "%26").replace("=", "%3D")
    return f"email={safe}&uid=10&role=user".encode()


def encrypt_profile(email: str) -> bytes:
    return aes.aes_ecb_encrypt(KEY, crypto.pkcs7_pad(profile_for(email)))


def decrypt_profile(ciphertext: bytes) -> dict:
    return parse_profile(aes.aes_ecb_decrypt(KEY, ciphertext))


def main() -> None:
    # The parser.
    assert parse_profile(b"foo=bar&baz=qux&zap=zazzle") == {
        "foo": "bar",
        "baz": "qux",
        "zap": "zazzle",
    }

    # Metacharacters are quoted, so user input alone can never set the role.
    assert b"&role=admin" not in profile_for("foo@bar.com&role=admin")

    # Cut-and-paste:
    #   email1 puts "admin" exactly at byte 16 of its profile (a block
    #   boundary), with 11 bytes of 0x0b after it;
    #   email2 makes its profile's first 32 bytes end exactly with "role=".
    # Splicing profile2's first two blocks with profile1's second block
    # yields "email=...&uid=10&role=admin" + 0x0b*11, which is also valid
    # PKCS#7 padding, so the forged ciphertext unpad cleanly.
    email1 = "foo@bar.co" + "admin" + "\x0b" * 11
    email2 = "foo@bar.commm"
    assert profile_for(email1)[16:21] == b"admin"
    assert profile_for(email2)[:32].endswith(b"role=")

    ct1 = encrypt_profile(email1)
    ct2 = encrypt_profile(email2)
    forged = ct2[:32] + ct1[16:32]

    plaintext = crypto.pkcs7_unpad(aes.aes_ecb_decrypt(KEY, forged))
    profile = parse_profile(plaintext)
    print(plaintext.decode())
    print(profile)
    assert profile["role"] == "admin"
    print("OK")


if __name__ == "__main__":
    main()
