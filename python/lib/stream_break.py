"""Piecemeal breaking of fixed-nonce CTR ciphertexts (ch19/ch20).

Fixed-nonce CTR is repeating-key XOR with a key as long as the message, so
the ciphertexts are broken column by column. Shared machinery:

- letter-frequency column breaking (case-insensitive),
- bigram/trigram context scoring against recovered neighbours,
- capitalization priors (sentence starts favor uppercase),
- common-word completion constraints (resolve columns that frequency alone
  leaves ambiguous, e.g. line-start capitals).
"""

from .crypto import ENGLISH_FREQ, xor_bytes

# Common English bigrams/trigrams (relative weights from published frequency
# tables), used to validate letter guesses against their neighbours.
BIGRAMS = {
    "th": 105, "he": 66, "in": 55, "er": 47, "an": 45, "re": 45, "on": 44,
    "at": 37, "en": 37, "nd": 35, "ti": 30, "es": 30, "or": 30, "te": 30,
    "of": 29, "ed": 28, "is": 28, "it": 27, "al": 27, "ar": 26, "st": 25,
    "to": 25, "nt": 22, "ng": 22, "se": 20, "ha": 20, "as": 20, "ou": 20,
    "io": 16, "le": 16, "ve": 16, "co": 16, "me": 16, "de": 15, "hi": 12,
    "ri": 12, "ro": 12, "ic": 12, "ne": 11, "ea": 11, "ra": 11, "ce": 11,
    "li": 11, "ch": 11, "ll": 11, "be": 11, "ma": 11, "si": 10, "om": 9,
    "ur": 9, "el": 9, "la": 8, "cc": 8, "et": 8, "ai": 8, "oo": 8, "ts": 8,
    "ee": 8, "fo": 8, "ss": 8, "ad": 8, "ge": 6, "tu": 6, "wo": 5,
}

TRIGRAMS = {
    "the": 49, "and": 34, "ing": 30, "ion": 27, "tio": 22, "her": 19,
    "ent": 18, "ere": 17, "for": 16, "ate": 16, "ith": 14, "ter": 13,
    "tha": 13, "hat": 13, "his": 12, "she": 12, "was": 10, "all": 10,
    "ver": 9, "you": 9, "not": 8, "but": 8, "had": 8, "one": 8, "out": 8,
    "who": 8, "him": 8, "say": 7, "see": 7, "way": 7, "old": 7, "own": 7,
    "new": 7, "may": 7, "how": 7, "tur": 6, "urn": 6, "ead": 6,
}

# Common English words, used to resolve positions where letter frequency
# alone is underdetermined (the "catch common English" step).
WORDS = {
    "about", "above", "after", "again", "all", "also", "among", "and",
    "another", "any", "around", "are", "because", "been", "before", "being",
    "between", "both", "but", "came", "can", "could", "day", "did", "do",
    "does", "done", "down", "during", "each", "even", "ever", "every",
    "face", "fact", "far", "feel", "few", "first", "fire", "find", "five",
    "for", "found", "four", "from", "get", "give", "go", "good", "got",
    "great", "had", "happen", "has", "have", "head", "hear", "her", "here",
    "high", "him", "his", "hold", "home", "hot", "house", "houses", "how",
    "idea", "if", "into", "is", "job", "just", "kept", "know", "lady",
    "large", "last", "late", "left", "let", "life", "light", "like", "line",
    "little", "live", "long", "look", "made", "make", "man", "many", "may",
    "me", "member", "men", "might", "mind", "miss", "moment", "more",
    "most", "much", "must", "name", "near", "new", "next", "no", "not",
    "nothing", "now", "number", "often", "of", "off", "on", "once", "one",
    "only", "open", "or", "other", "our", "out", "over", "own", "part",
    "people", "place", "point", "put", "question", "read", "right", "room",
    "said", "same", "say", "school", "see", "seem", "set", "she", "short",
    "show", "side", "sign", "small", "so", "some", "something", "still",
    "story", "such", "sure", "take", "talk", "tell", "than", "that", "the",
    "their", "them", "then", "there", "these", "they", "thing", "think",
    "this", "those", "three", "time", "to", "together", "today", "too",
    "took", "try", "turn", "two", "under", "until", "up", "us", "use",
    "very", "want", "war", "way", "we", "week", "well", "went", "were",
    "what", "when", "where", "which", "while", "who", "why", "wide", "will",
    "wind", "with", "within", "without", "woman", "women", "word", "work",
    "world", "would", "year", "yes", "yet", "you", "young", "your",
    "beauty", "born", "changed", "close", "days", "desk", "dreamed", "fame",
    "faces", "force", "grew", "grey", "heart", "hers", "helper", "ignorant",
    "lived", "lout", "motley", "nature", "nights", "nod", "passed",
    "please", "polite", "seemed", "sensitive", "shrill", "sun", "sweet",
    "terrible", "utterly", "vain", "voices", "worn",
    "death", "wish", "hysterical", "apocalypse", "clue", "warned", "warning",
    "paranoid", "alcoholic", "tremble", "muscles", "tighten", "suddenly",
    "horror", "flick", "murderer", "bass", "peace", "step", "attack",
    "lightning", "frightenin", "afraid", "dark", "park", "scared", "trouble",
}


def letter_score(b: int) -> float:
    if 0x41 <= b <= 0x5A:
        b += 0x20
    return ENGLISH_FREQ.get(b, -1.0)


def column_letter_score(column: bytes, g: int) -> float:
    """Letter-frequency score of a ciphertext column XOR'd with candidate g."""
    return sum(letter_score(b ^ g) for b in column)


def case_score(row: bytes, i: int, g: int, ks: bytes) -> float:
    """Capitalization prior: line starts and post-sentence positions favor
    uppercase; mid-word positions favor lowercase."""
    b = row[i] ^ g
    if not (0x41 <= b <= 0x5A or 0x61 <= b <= 0x7A):
        return 0.0
    upper = 2.0 if b < 0x60 else -1.0
    if i == 0:
        return upper
    prev = row[i - 1] ^ ks[i - 1]
    if 0x41 <= prev <= 0x5A or 0x61 <= prev <= 0x7A:
        return -1.0 if b < 0x60 else 0.0
    if i >= 2:
        prev2 = row[i - 2] ^ ks[i - 2]
        if prev == 0x20 and prev2 in b".!?":
            return upper
    return 0.0


def context_score(row: bytes, i: int, g: int, ks: bytes) -> float:
    """Bigram/trigram score of the byte at i against its recovered neighbours."""
    b = row[i] ^ g
    if not (0x20 <= b < 0x7F):
        return 0.0
    score = 0.0
    left = row[i - 1] ^ ks[i - 1] if i > 0 else None
    right1 = row[i + 1] ^ ks[i + 1] if i + 1 < len(row) else None
    if left is not None:
        score += BIGRAMS.get(bytes([left, b]).lower().decode("latin-1"), 0)
    if right1 is not None:
        score += BIGRAMS.get(bytes([b, right1]).lower().decode("latin-1"), 0)
    if left is not None and right1 is not None:
        score += TRIGRAMS.get(bytes([left, b, right1]).lower().decode("latin-1"), 0)
    return score


def build_word_constraints(plain: bytes, words: set[str]) -> list[dict[int, int]]:
    """For each position i, map candidate byte -> total length of words the
    byte would complete at i (the row matches the word everywhere except
    possibly at i; both letter cases count)."""
    low = plain.lower()
    n = len(plain)
    constraints = [dict() for _ in range(n)]
    for w in words:
        wl = w.lower().encode()
        if len(wl) > n:
            continue
        for start in range(0, n - len(wl) + 1):
            mismatches = 0
            mismatch = -1
            for o in range(len(wl)):
                if low[start + o] != wl[o]:
                    mismatches += 1
                    if mismatches > 1:
                        break
                    mismatch = start + o
            if mismatches != 1:
                continue
            c = wl[mismatch - start]
            candidates = (c, c ^ 0x20) if 0x61 <= c <= 0x7A else (c,)
            for cand in candidates:
                constraints[mismatch][cand] = constraints[mismatch].get(cand, 0) + len(wl)
    return constraints


def refine_keystream(ciphertexts: list[bytes], ks: bytearray, words: set[str] = WORDS, passes: int = 6) -> None:
    """Re-guess every keystream byte, scoring candidates by the column's
    letter frequency, bigram/trigram context from the recovered neighbours,
    capitalization priors, and common-word completion."""
    for _pass in range(passes):
        rows = [xor_bytes(ct, ks[: len(ct)]) for ct in ciphertexts]
        constraints = [build_word_constraints(row, words) for row in rows]
        for i in range(len(ks)):
            best_g, best_score = ks[i], float("-inf")
            for g in range(256):
                score = 0.0
                for r, ct in enumerate(ciphertexts):
                    if len(ct) > i:
                        score += letter_score(ct[i] ^ g)
                        score += context_score(ct, i, g, ks)
                        score += case_score(ct, i, g, ks)
                        score += constraints[r][i].get(ct[i] ^ g, 0)
                if score > best_score:
                    best_g, best_score = g, score
            ks[i] = best_g


def break_fixed_nonce_ctr(ciphertexts: list[bytes]) -> bytes:
    """Recover the shared keystream of fixed-nonce CTR ciphertexts.

    Pass 1 breaks each column by letter frequency (the repeating-key XOR
    transposition); refinement passes add context, case, and word knowledge.
    """
    max_len = max(len(ct) for ct in ciphertexts)
    ks = bytearray(max_len)
    for i in range(max_len):
        column = bytes(ct[i] for ct in ciphertexts if len(ct) > i)
        ks[i] = max(range(256), key=lambda g: column_letter_score(column, g))
    refine_keystream(ciphertexts, ks)
    return bytes(ks)
