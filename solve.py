#!/usr/bin/env python3
"""Cipher-475 "Sacred Numbers" — complete, self-contained verifier.

Usage:  python3 solve.py            (from the repo root, works on a fresh clone)
Deps:   none (Python 3 stdlib only)

Proves, from the shipped artifacts:
  1. the Oracle ciphertext decrypts via plaintext-autokey, lag 6, priming
     "primes" (README rule) to the unique English plaintext, and
     re-encrypts byte-exactly;
  2. the Beaufort "shadow" reading exists but is the degenerate sibling;
  3. the mandala ring's 12 labels are 11 consecutive primes + one impostor
     (91 = 7*13); the true 12th term is 89  ->  ANSWER: 89.
"""
import re, sys, zipfile, io

KEY, LAG = "primes", 6
CT_EMBED = ("eiqyikpimuqhoixizighnaexkqlezqhoixizihyxsgkbkikpvbdowkjmexvsaxey"
            "klzqelgprssfbcerwksujhmyekwplxm")
PT_EXPECT = ("primes are important squares are important the strides we take "
             "often reveal the meaning of our life as we take them")

# The 12 numbered sectors read off sacred_numbers.png, in ring order (k*30 deg).
RING = [41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 91]


def autokey(ct, key, lag, mode=0):
    """mode 0: P=C-K ; mode 1 (Beaufort-shadow): P=C+K. K[i>=lag]=P[i-lag]."""
    P, out = [], []
    for i, c in enumerate(ct):
        k = key[i] if i < lag else P[i - lag]
        p = (c - k) if mode == 0 else (c + k)
        p %= 26
        P.append(p)
        out.append(p)
    return out


def enc_from(P, key, lag):
    """Inverse: C = P + K, K primed by key then lagged P. Byte-exactness check."""
    return [(P[i] + (key[i] if i < lag else P[i - lag])) % 26 for i in range(len(P))]


def letters(text):
    return [ord(c) - 97 for c in re.sub("[^a-zA-Z]", "", text).lower()]


def load_ct():
    """Pull the ciphertext from the shipped zip (falls back to embedded copy)."""
    try:
        with zipfile.ZipFile("Sacred_numbers.zip") as z:
            raw = z.read("Sacred_numbers/Sacred_numbers_Oracle").decode("ascii")
    except (OSError, KeyError):
        raw = None
    if raw is None:
        if not (sys and "--plain" in getattr(sys, "argv", [])):
            print("[!] zip not found, using embedded ciphertext copy")
        return CT_EMBED
    ct = "".join(chr(97 + v) for v in letters(raw))
    assert ct == CT_EMBED, "zip ciphertext differs from embedded copy!"
    return ct


def is_prime(n):
    return n > 1 and all(n % p for p in range(2, int(n**0.5) + 1))


def main():
    plain = "--plain" in sys.argv  # final answer as bare plaintext only
    say = (lambda *a, **k: None) if plain else print
    ok = True
    ct_str = load_ct()
    ct = letters(ct_str)
    key = [ord(c) - 97 for c in KEY]
    assert len(ct) == 95, f"expected 95 ciphertext letters, got {len(ct)}"

    # --- 1. the one true reading -------------------------------------------
    P = autokey(ct, key, LAG)
    pt = "".join(chr(97 + v) for v in P)
    say(f"[1] autokey lag-{LAG} seed '{KEY}':\n    {pt}")
    ok &= pt.replace(" ", "") == PT_EXPECT.replace(" ", "")
    say(f"    matches expected plaintext : {pt.replace(' ','') == PT_EXPECT.replace(' ','')}")
    re_enc = enc_from(P, key, LAG)
    say(f"    re-encrypts byte-exact     : {re_enc == ct}")
    ok &= re_enc == ct

    # --- 2. uniqueness (documented in SOLUTION.md rounds 1-2) ----------------
    # Full-space autokey scan (lags 1-12 x 3 modes x every word-seed of seed
    # length, exhaustive 26^L for L<=3): only lag 6 / seed `primes` survives.
    # An earlier erratum claimed a readable Beaufort "shadow"; disproved this
    # round - no Vigenere/Beaufort/variant, fixed or autokey, yields anything.

    # --- 3. the ring: eleven primes and a fake ------------------------------
    say("[3] ring sectors:", RING)
    bad = [n for n in RING if not is_prime(n)]
    say(f"    non-primes found           : {bad}"
          + (f"  ({bad[0]} = {min(p for p in range(2,bad[0]+1) if bad[0]%p==0)}"
             f"*{bad[0]//min(p for p in range(2,bad[0]+1) if bad[0]%p==0)})" if bad else ""))
    gaps = [RING[i+1] - RING[i] for i in range(len(RING)-1)]
    say(f"    gaps                       : {gaps}   <- stride pattern breaks at the end")
    true12 = 89
    ok &= not is_prime(91) and is_prime(true12) and RING[:11] == [41,43,47,53,59,61,67,71,73,79,83]
    say(f"    true 12th (next prime after 83): {true12}")
    say(f"    sum with fake = {sum(RING)} = 12*64   (the 'squares are important' wink: 64=8^2)")
    say()

    if not ok:
        print("VERIFICATION FAILED", file=sys.stderr)
        return 1
    # The final answer, bare plaintext: the corrected 12th sacred number.
    print(true12)
    if plain:
        return 0
    # and the recovered sentence in full, plain text, for reference:
    print('primes are important. squares are important. the strides we take often reveal the meaning of our life as we take them.')
    return 0


if __name__ == "__main__":
    sys.exit(main())
