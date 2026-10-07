import numpy as np
import wave

SR = 44100
DUR = 15.0
N = int(SR * DUR)
t = np.arange(N) / SR
buf = np.zeros(N)

def place(buf, sig, t0, amp=1.0):
    i0 = int(t0 * SR)
    if i0 >= N:
        return
    i1 = min(i0 + len(sig), N)
    buf[i0:i1] += sig[:i1 - i0] * amp

def kick(freq=55, decay=0.25):
    tt = np.arange(int(SR * decay)) / SR
    f = freq * np.exp(-tt * 22) + 32
    phase = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(phase) * np.exp(-tt * 15)

def hat(decay=0.06, seed=1):
    tt = np.arange(int(SR * decay)) / SR
    noise = np.random.RandomState(seed).uniform(-1, 1, len(tt))
    return noise * np.exp(-tt * 100)

def snare(decay=0.18, seed=2):
    tt = np.arange(int(SR * decay)) / SR
    noise = np.random.RandomState(seed).uniform(-1, 1, len(tt))
    body = np.sin(2 * np.pi * 185 * tt) * np.exp(-tt * 22)
    return (noise * 0.6 + body) * np.exp(-tt * 14)

BPM = 120
beat = 60 / BPM  # 0.5s

# kick on every beat
for b in np.arange(0.0, DUR - 0.1, beat):
    place(buf, kick(), b, 0.9)
# hats on off-beats
for b in np.arange(beat / 2, DUR - 0.1, beat):
    place(buf, hat(seed=int(b * 100) % 5 + 1), b, 0.32)
# snare on beats 2 & 4 (backbeat)
for b in np.arange(beat, DUR - 0.1, beat * 2):
    place(buf, snare(), b, 0.4)

# bass pulse on beats
for b in np.arange(0.0, DUR - 0.1, beat):
    tt = np.arange(int(SR * 0.45)) / SR
    place(buf, np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 4), b, 0.55)

# pad drone (A minor-ish)
freqs = [110.0, 164.81, 220.0, 277.18]
pad = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
env = np.full(N, 0.07)
env[:int(2 * SR)] = np.linspace(0.0, 0.07, int(2 * SR))
env[int(13 * SR):] = np.linspace(0.07, 0.0, N - int(13 * SR))
buf += pad * env

# riser: filtered noise sweep building 8s -> 12.5s
rng = np.random.RandomState(3)
noise = rng.uniform(-1, 1, N)
# crude rising tone via amplitude ramp
riser_env = np.zeros(N)
i8, i13 = int(7 * SR), int(10.5 * SR)
riser_env[i8:i13] = np.linspace(0.0, 0.28, i13 - i8)
riser_env[i13:] = 0.0
buf += noise * riser_env

# logo hit at 10.9s
place(buf, kick(70, 0.6), 10.9, 1.2)
place(buf, snare(seed=9), 10.9, 0.6)
crash = np.random.RandomState(4).uniform(-1, 1, int(SR * 0.9)) * np.exp(-np.arange(int(SR * 0.9)) / SR * 5)
place(buf, crash, 10.9, 0.5)

# gentle master: soft clip + normalize
buf = np.tanh(buf * 1.1)
buf = buf / np.max(np.abs(buf)) * 0.9

out = np.column_stack([buf, buf])
data = (out * 32767).astype(np.int16)
with wave.open('tornado_audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print('wrote tornado_audio.wav %.1fs' % (len(data) / SR))
