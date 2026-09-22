# Soft, warm music bed: slow I-vi-IV-V pad (F major) of detuned triangle+sine voices, gentle low-pass,
# sparse music-box melody, -18 dBFS RMS, 1.5 s fade-in, 4 s fade-out, exact length.
import numpy as np, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR=44100; DUR=float(sys.argv[1]); N=int(SR*DUR); t=np.arange(N)/SR
rng=np.random.default_rng(7)
def f(midi): return 440*2**((midi-69)/12)
# chords (midi): F3 A3 C4 F4 | D3 F3 A3 D4 | Bb2 D3 F3 Bb3 | C3 E3 G3 C4
chords=[[53,57,60,65],[50,53,57,62],[46,50,53,58],[48,52,55,60]]
CH=6.0  # seconds per chord
def tri(ph): return 2*np.abs(2*(ph%1)-1)-1
pad=np.zeros(N)
for ci in range(int(np.ceil(DUR/CH))):
    notes=chords[ci%4]; s0=ci*CH; s1=min(DUR,s0+CH)
    i0=int(s0*SR); i1=min(N,int((s1+1.6)*SR))  # overlap into next chord (release)
    seg=t[i0:i1]-s0; L=seg.size
    env=np.ones(L); a=int(1.4*SR); r=int(1.6*SR)
    env[:a]=np.linspace(0,1,a)**2
    if L>r: env[-r:]*=np.linspace(1,0,r)**1.5
    voice=np.zeros(L)
    for m in notes:
        for det,amp in ((-5,.5),(0,.7),(4,.5)):
            fr=f(m)*2**(det/1200); ph=fr*seg+rng.random()
            voice+=amp*(0.55*tri(ph)+0.45*np.sin(2*np.pi*ph))
        # soft octave-up shimmer
        voice+=0.12*np.sin(2*np.pi*f(m+12)*seg)
    pad[i0:i1]+=voice*env
# gentle low-pass + slow filter "breathing" via two stages
sos=butter(2,1500,'low',fs=SR,output='sos'); pad=sosfilt(sos,pad)
lfo=0.85+0.15*np.sin(2*np.pi*t/9.0); pad*=lfo
# music-box melody: pentatonic plucks every ~1.5 s, quiet, decaying sines
mel=np.zeros(N); pent=[77,79,81,84,86,89]  # F5 G5 A5 C6 D6 F6
k=0; tt=2.0
while tt<DUR-5:
    m=pent[(k*3+ (k//2))%len(pent)] if k%4 else 77
    i0=int(tt*SR); L=min(N-i0,int(2.2*SR)); seg=np.arange(L)/SR
    note=np.sin(2*np.pi*f(m)*seg)*np.exp(-seg*2.2)+0.25*np.sin(2*np.pi*f(m)*2*seg)*np.exp(-seg*4)
    mel[i0:i0+L]+=note*0.7
    tt+=1.5 if k%3 else 3.0; k+=1
mix=pad*1.0+mel*0.9
# stereo: slight detune widening via short delay on one side
d=int(0.012*SR); left=mix.copy(); right=np.concatenate([np.zeros(d),mix[:-d]])
st=np.stack([left,right],1)
# fades
fi=int(1.5*SR); fo=int(4.0*SR)
st[:fi]*=np.linspace(0,1,fi)[:,None]; st[-fo:]*=np.linspace(1,0,fo)[:,None]**1.2
# normalise to -18 dBFS RMS, keep peak under -1 dBFS
rms=np.sqrt(np.mean(st**2)); st*= (10**(-18/20))/rms
peak=np.abs(st).max()
if peak>10**(-1/20): st*= (10**(-1/20))/peak
print('rms dBFS',20*np.log10(np.sqrt(np.mean(st**2))),'peak dBFS',20*np.log10(np.abs(st).max()),'len',st.shape[0]/SR)
wavfile.write(sys.argv[2],SR,(st*32767).astype(np.int16))
