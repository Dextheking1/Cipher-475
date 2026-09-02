import numpy as np, re, zipfile, sys

# ============ independent re-proof of the uniqueness claim ============
# Different implementation path (numpy-batched, trigram first-stage,
# greedy-DP second-stage) than the round-1/2 scans that are cited in
# SOLUTION.md. If lag-6/'primes' is really the UNIQUE solution, this
# must find it as the only candidate above the intelligibility bar.

z=zipfile.ZipFile('Sacred_numbers.zip')
raw=z.read('Sacred_numbers/Sacred_numbers_Oracle').decode()
ct=re.sub('[^A-Za-z]','',raw).lower()
C=np.array([ord(c)-97 for c in ct]); N=len(ct); assert N==95

from english_words import get_english_words_set
words=sorted({w for w in get_english_words_set(['web2'],lower=True)
              if w.isalpha() and 2<=len(w)<=12})
wset=set(words)

# English trigram codes ('^'=26), as sorted set for np.isin
codes=[]
for w in words:
    x='^'+w+'^'
    for i in range(len(x)-2):
        a,b,c=(26 if ch=='^' else ord(ch)-97 for ch in x[i:i+3])
        codes.append(a*676+b*26+c)
tri=np.unique(np.array(codes))

def score(P):  # P (S,N) int -> frac of trigrams in English set, vectorized
    S=P.shape[0]
    A=np.empty((S,N+2),dtype=np.int64); A[:,0]=26; A[:,N+1]=26
    A[:,1:N+1]=P
    co=A[:,:-2]*676+A[:,1:-1]*26+A[:,2:]
    return np.isin(co,tri).mean(axis=1)

def wordcov(s):
    i=c=0;ws=[]
    while i<N:
        for L in range(12,2,-1):
            if s[i:i+L] in wset: c+=L;ws.append(s[i:i+L]);i+=L;break
        else:i+=1
    return c,' '.join(ws)

byL={}
for w in words: byL.setdefault(len(w),[]).append(w)

CANDS=[]  # (trigscore, kind, mode, L, seedlist, Prows)
for L in range(2,13):
    if L not in byL: continue
    wl=byL[L]
    K=np.array([[ord(ch)-97 for ch in w] for w in wl],dtype=np.int64)
    for kind in ('auto','fixed'):
        for mode in (0,1,2):
            P=np.empty((K.shape[0],N),dtype=np.int64)
            for i in range(N):
                kb = K[:,i] if (kind=='auto' and i<L) else (P[:,i-L] if kind=='auto' else K[:,i%L])
                v = (C[i]-kb) if mode==0 else ((C[i]+kb) if mode==1 else (kb-C[i]))
                P[:,i]=np.remainder(v,26)
            sc=score(P)
            top=np.argsort(-sc)[:30]
            if sc[top[0]]>0.55:
                CANDS.append((float(sc[top[0]]),kind,mode,L,[wl[t] for t in top],[P[t] for t in top]))
print(f"first-stage buckets with a >0.55 trigram leader: {len(CANDS)} (of 66)")

BEST=[]
for sc,kind,mode,L,seeds,rows in CANDS:
    for seed,row in zip(seeds,rows):
        s=''.join(chr(97+v) for v in row)
        cov,ws=wordcov(s)
        BEST.append((cov,kind,mode,seed,s,ws))
BEST.sort(key=lambda x:-x[0])
print("== top 5 by word-coverage (letters covered / 95) ==")
for cov,kind,mode,seed,s,ws in BEST[:5]:
    print(f"  {cov:3d}/95 {kind} m{mode} seed={seed!r}: {ws[:70]}")

# the known answer check, independent path:
P=np.empty(N,dtype=np.int64); K=[ord(c)-97 for c in 'primes']
for i in range(N):
    b=K[i] if i<6 else P[i-6]
    P[i]=(C[i]-b)%26
s=''.join(chr(97+v) for v in P)
cov,ws=wordcov(s)
print(f"known solution via audit path: {cov}/95 -> {ws}")
print("re-encrypt exact:", ''.join(chr(97+(P[i]+(K[i] if i<6 else P[i-6]))%26) for i in range(N))==ct)
above=[b for b in BEST if b[0]>=76]
print(f"UNIQUE@80%-coverage: {len(above)==1 and above[0][3]=='primes'} ({len(above)} candidates above 76/95)")
