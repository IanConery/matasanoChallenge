import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import crypto

DATA = Path(__file__).resolve().parents[2] / "data" / "set01" / "challenge_06.txt"


def decrypt_with_key_size(ciphertext: bytes, key_size: int) -> tuple[bytes, bytes]:
    key = b""
    for i in range(key_size):
        column = ciphertext[i :: key_size]
        best = max(range(256), key=lambda k: crypto.score_english(crypto.single_byte_xor(column, k)))
        key += bytes([best])
    return key, crypto.repeating_key_xor(ciphertext, key)


def score_plaintext(plaintext: bytes) -> float:
    words = (b" the ", b" and ", b" that ", b" you ", b" this ", b" with ", b" for ")
    word_hits = sum(plaintext.count(w) for w in words)
    return crypto.score_english(plaintext) * 100 + word_hits


def solve() -> tuple[int, bytes, str]:
    ciphertext = crypto.b64_decode(DATA.read_text())

    assert crypto.hamming_distance(b"this is a test", b"wokka wokka!!!") == 37

    # The normalized Hamming distance heuristic picks a good starting range,
    # but on this data the true size is not the smallest, so verify every
    # candidate by fully decrypting and scoring the plaintext.
    best_key_size, best_key, best_plaintext, best_score = 0, b"", b"", float("-inf")
    for key_size in range(2, 41):
        key, plaintext = decrypt_with_key_size(ciphertext, key_size)
        score = score_plaintext(plaintext)
        if score > best_score:
            best_key_size, best_key, best_plaintext, best_score = key_size, key, plaintext, score

    return best_key_size, best_key, best_plaintext.decode()


def main() -> None:
    key_size, key, plaintext = solve()
    print(f"key size: {key_size}")
    print(f"key: {key!r}")
    print()
    print(plaintext)
    assert key_size == 29 and key == b"Terminator X: Bring the noise"
    print("OK")


if __name__ == "__main__":
    main()
