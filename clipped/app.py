import numpy as np
from scipy.io import wavfile
import sounddevice as sd

NSECS = 3
SAMPLE_RATE = 48_000
NSAMPLES = NSECS * SAMPLE_RATE
F = 440

t = np.linspace(0, NSECS, num=NSAMPLES, endpoint=False, dtype=np.float32)
f = np.sin(2 * np.pi * F * t) * t / NSECS
wavfile.write('sine.wav', SAMPLE_RATE, f)