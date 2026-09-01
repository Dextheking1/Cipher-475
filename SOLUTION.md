# Cipher-475 — Solution

## The answer

The Oracle decrypts to:

> **Primes are important. Squares are important. The strides we take often reveal the meaning of our life as we take them.**

(continuous form: `primesareimportantsquaresareimportantthestrideswetakeoftenrevealthemeaningofourlifeaswetakethem`)

## The cipher

**Autokey (plaintext-autokey), Vigenère subtraction, priming key = `primes`.**

For each ciphertext letter `c[i]` (letters only; spaces and periods carry no key material and are ignored):

```
p[i] = (c[i] − k[i]) mod 26
k[i] = "primes"[i]      for i < 6
k[i] = p[i − 6]         for i ≥ 6
```

The key stream is the 6-letter priming word `primes` followed by the plaintext itself
(classical autokey with period 6). Encryption is the inverse (`c = p + k`).

Check on the first word: `primes` + key `primes` = `Eiqyik` — the first word
encrypts with itself as the key (E = 2·P for the primer), which is exactly how the
primer `primes` can be recovered from `Eiqyik` alone once you notice the doubling:
no other priming reproduces the crib, and "sacred primes" / the prime-number ring in
the image point straight at it.

## Why it is "super shrimple"

- **The ciphertext must be taken verbatim from the file.** The oracle text is
  `Eiqyik pim uqhoixizi. Ghnaexk qle zqhoixizi. Hyx sgkbkik pv bdow kjmex vsaxey klz
  qelgprs sf bce rwks uj hm yekw plxm.` — note `Ghnaexk qle` (7+3, not 6+2) and
  `sgkbkik` / `rwks`. Misreading any letter derails the autokey recursion forever
  (each plaintext letter feeds the keystream, so one wrong letter corrupts all
  downstream words — which is why careless transcription makes this "hard").
- **The theme is the key.** `Sacred primes` + the ring of primes → priming word
  `primes`, then plain autokey. Nothing else.

## The image (`sacred_numbers.png`)

Supports the plaintext and doubles as a spot-the-error graphic:

- Gold number ring at 12 clock positions: 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
  83, **91** — the last is *not* prime (91 = 7·13; the true next prime is 89).
  "Primes are important."
- The gold chords connect clock nodes (h, h+3 mod 12), i.e. **four overlapping
  squares** rotated 30° apart. "Squares are important."
- LSB, chunk-walk, trailing bytes, metadata: no stego — the image is thematic,
  not a data carrier.

## Files

- `Sacred_numbers.zip` → `Sacred_numbers/Sacred_numbers_Oracle` (119 B, the
  ciphertext above) and `Sacred_numbers/sacred_numbers.png`.

## Reproduce

```python
ct = "eiqyikpimuqhoixizighnaexkqlezqhoixizihyxsgkbkikpvbdowkjmexvsaxeyklzqelgprssfbcerwksujhmyekwplxm"
C = [ord(c) - 97 for c in ct]
P, prime = [], "primes"
for i, v in enumerate(C):
    k = ord(prime[i]) - 97 if i < 6 else P[i - 6]
    P.append((v - k) % 26)
print("".join(chr(97 + p) for p in P))
# primesareimportantsquaresareimportantthestrideswetakeoftenrevealthemeaningofourlifeaswetakethem
```
