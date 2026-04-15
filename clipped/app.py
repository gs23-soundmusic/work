import numpy as np
from scipy.io import wavfile
import sounddevice as sd

NSECS = 1
SAMPLE_RATE = 48_000
NSAMPLES = NSECS * SAMPLE_RATE
FREQUENCY = 440
MAX_AMP = 32767
HALF_AMP = MAX_AMP // 2
QUARTER_AMP = MAX_AMP // 4

t = np.linspace(0, NSECS, num=NSAMPLES, endpoint=False, dtype=np.float32)

sine_wave = np.sin(2 * np.pi * FREQUENCY * t) * QUARTER_AMP
sine_wave = sine_wave.astype(np.int16)
wavfile.write('sine.wav', SAMPLE_RATE, sine_wave)

clipped_wave = HALF_AMP * np.sin(2 * np.pi * FREQUENCY * t)
clipped_wave = np.clip(clipped_wave, -QUARTER_AMP, QUARTER_AMP)
clipped_wave = clipped_wave.astype(np.int16)
wavfile.write('clipped.wav', SAMPLE_RATE, clipped_wave)

sd.play(clipped_wave, SAMPLE_RATE)
sd.wait()