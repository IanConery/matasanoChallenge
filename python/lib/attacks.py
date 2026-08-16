"""ECB byte-at-a-time decryption (challenges 12 and 14).

Oracle shape: oracle(x) = ECB(prefix || x || hidden), with a fixed unknown
prefix (possibly empty) and a consistent unknown key.

Mechanics, for the j-th hidden byte (j = 0, 1, 2, ...):

  real = oracle(A^k)
  fake_c = oracle(A^k + recovered + c)

with k = (15 - (offset + j)) mod 16 and `offset` a candidate for
len(prefix) mod 16. In `real` the byte at position len(prefix)+k+j is
hidden[j]; in `fake_c` it is c. When the offset is the true one, that
position falls on a block boundary (last byte of a block), so:

  - a wrong c corrupts exactly that block -> first differing block = B
  - the right c leaves that block identical and only the *following*
    blocks can differ -> first differing block >= B+1

Hence the correct byte is the c whose first-differing block index is
maximal. A wrong offset never lands the candidate on a block end, so every
c corrupts the same block and the recovery degenerates to a constant
(all-zero) stream; callers discriminate by keeping the non-constant
result.
"""


def _first_differing_block_index(a: bytes, b: bytes) -> int:
    """Index of the first differing 16-byte block.

    If all common blocks are equal, returns the number of common blocks
    (a sentinel larger than any real difference index).
    """
    n = min(len(a), len(b))
    full = n - (n % 16)
    for i in range(0, full, 16):
        if a[i : i + 16] != b[i : i + 16]:
            return i // 16
    return n // 16


def ecb_byte_at_a_time(
    oracle,
    num_bytes: int,
    prefix_offsets: tuple = (0,),
    block_size: int = 16,
) -> dict:
    """Recover the hidden suffix byte by byte.

    Tries every candidate value of len(prefix) mod 16. Returns
    {prefix_offset: recovered_bytes}; only the true offset yields a
    non-constant (i.e. the actual hidden data) result.
    """
    results = {}
    for offset in prefix_offsets:
        recovered = b""
        for j in range(num_bytes):
            k = (block_size - 1 - (offset + j)) % block_size
            base = oracle(b"A" * k)
            best_c, best_d = None, -1
            for c in range(256):
                fake = oracle(b"A" * k + recovered + bytes([c]))
                d = _first_differing_block_index(base, fake)
                if d > best_d:
                    best_c, best_d = c, d
            recovered += bytes([best_c])
        results[offset] = recovered
    return results
