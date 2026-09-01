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

## Deeper-layer search (creator-confirmed: plaintext = only a hint)

After the layer-1 solve was confirmed to be "just a hint", every remaining carrier
was probed to exhaustion. Summary of negative results (all reproducible; scripts
in `work/`):

**Containers — clean.**
- Repo: 3 commits, all blobs checked (`Initial commit` README differs only by the
  zip-pointer line); no releases/tags/other branches/issues/PR comments.
- `Sacred_numbers.zip`: exactly 2 entries; local/central headers tight, zero
  inter-entry gaps, no comments/extra fields; both deflate streams have
  `unused_data = 0` (no stream-tail stego). The zip being 1369 B "larger" than the
  PNG is ordinary deflate-inflation on incompressible noise.
- PNG: IHDR/48×IDAT/IEND only — no tEXt/iTXt, no trailing bytes, 8-bit RGB
  (no bit-depth headroom). Scanline filter bytes are normal libpng heuristics
  (1184×AVG, 66×PAETH, 7×SUB, 2×UP).
- LSB stego: every bit plane (shifts 0,1,2,6,7) × 3 channels × row/col-major ×
  forward/reverse — zero printable runs ≥16 bytes. Equalized/brightened/
  R−G/B−G views: no structure beyond the visible art.

**Image content — fully accounted for.**
- Number ring verified glyph-by-glyph at 4×: exactly 41,43,47,53,59,61,67,71,73,
  79,83,91, all upright, no marks/dots/rotations.
- Dark-line chord extraction: figure = 12 spokes (6 diameters) + concentric circles
  + petals. No polygon chords; center is pure glow.
- Starfield: 1114 clusters; angular distribution vs the 12 spokes is consistent
  with chance (18 near-spoke stars vs ~17 expected).
- The one true anomaly is the ring itself: **91 is not prime (7·13); the 24th
  prime is 89** — the "sacred number" ring is the consecutive primes 41..89 with
  the last slot faked. As an nth-prime↔letter cipher the ring decodes to
  M,N,O,P,Q,R,S,T,U,V,W,(X): a running alphabet — the ring is a teaching device.

**Crypto — closed.**
- Uniform autokey family: crib forces lag ∈ {6,17}; fixed-seed sweep over all lags
  2..47 × {vigenère,beaufort,var} and per-chain seed optimization for all
  prime/square lags (2,3,4,5,6,7,9,11,13,16,17,19,23,25,29,31,36,37,41,43,47):
  only lag 6 + seed "primes" yields English (cov 93/95; everything else ≤52).
- Second layer keyed by ring numbers (mod 26, digits, prime gaps, diameter
  sums/diffs) × 3 modes on BOTH ciphertext and plaintext: all garbage (≤52/95).
- Plaintext meta keys (word initials/lasts/lengths) on ciphertext: garbage.

**Positional readings — all negative.**
Ring-number indices (0/1-based, n, n², mod L), prime/square positions, word
initial/last acrostics, gap walks (91-ring, 89-ring, standard prime gaps; both
directions; all starts), the FULL affine-stride space pt[(a·i+b) mod 95] (all 72
units × 95 offsets — only trivial rotations of the message itself score), rail
fence (6/7 rails), 10×10 spiral/columnar, 16×6 grid flips: nothing beyond
chance-wording.

## Interpretation (strongest candidate for the "deeper" step)

The README's phrase "Given in the puzzle hint 2" + the decrypted text's structure
show the plaintext IS a numbered hint-list:
  hint 1 = "primes are important" (→ the seed/ring),
  hint 2 = "squares are important",
  hint 3 = "the strides we take … reveal the meaning" (→ the autokey LAG itself:
  the message explains its own decryption).
Under "dont overthink", every *data* layer is empty; what the hints teach is the
mechanism of the cipher. Consistent with "This is a test for the one I want to
make" and "That's the STARTING puzzle file", the real (test-)puzzle content the
hints prepare for is not shipped in this repo — the follow-up exists only with
the creator (Discord; cf. Cipher-478's "Solve this discord cipher posted"). If a
one-line answer is demanded for 475 itself, the defensible deliverable is:

> **The sacred ring is faked: 91 ≠ prime (7·13); the 12th sacred number must be 89.**
> ("Primes are important." — and the oracle's autokey stride is 6, seeded by the theme.)

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
