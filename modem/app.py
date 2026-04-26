#This a decoder for text messages encoded as audio using the Bell 103 modem protocol.

import numpy as np
from scipy.io import wavfile



BIT_SIZE = 160
BYTE_SIZE = 1600
SAMPLE_RATE = 48_000



def tone_power(samples, frequency):
    '''Single tone detector with correlation method.'''
    I = 0.0
    Q = 0.0
    for n in range(BIT_SIZE):
        I += np.dot(samples[n], np.cos(2 * np.pi * frequency * n / SAMPLE_RATE))
        Q += np.dot(samples[n], np.sin(2 * np.pi * frequency * n / SAMPLE_RATE))
    return I**2 + Q**2



def bit_extractor(samples, frequency1, frequency2):
    '''Extracts a bit from the given samples.'''
    power1 = tone_power(samples, frequency1)
    power2 = tone_power(samples, frequency2)
    if power1 > power2:
        return 0
    else:
        return 1



def byte_extractor(samples, frequency1, frequency2):
    '''Extracts a byte from the given samples. The byte is constructed from 8 bits, 
    and the start and stop bits are extracted and ignored.'''
    bits = []
    for i in range(0, BYTE_SIZE, BIT_SIZE):
        bit = bit_extractor(samples[i:i+BIT_SIZE], frequency1, frequency2)
        bits.append(bit)

    bits = bits[1:-1]
    byte = 0
    for i in range(8):
        byte |= (bits[i] << i)
    return byte



file = 'message.wav'
wave = wavfile.read(file)
text = []
for i in range(0, wave[1].shape[0], BYTE_SIZE):
    bytes = byte_extractor(wave[1][i:i+BYTE_SIZE], 2025, 2225)
    text.append(chr(bytes))

message_output = ''.join(text)
with open(file.split('.')[0] + '.txt', 'w') as f:
    f.write(message_output)