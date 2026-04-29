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
    and the start and stop bits are extracted and ignored. '''
    bits = []
    for i in range(0, BYTE_SIZE, BIT_SIZE):
        bit = bit_extractor(samples[i:i+BIT_SIZE], frequency1, frequency2)
        bits.append(bit)

    bits = bits[1:-1]
    byte = 0
    for i in range(8):
        byte |= (bits[i] << i)
    return byte



def find_start_bit(samples, frequency1, frequency2):
    '''Finds the start bit of the given samples, returns index where start bit is found.'''
    start_found = 1
    index = 0
    while start_found < 9:
        start_bit = bit_extractor(samples[index:index + BIT_SIZE], frequency1, frequency2)
        stop_bit = bit_extractor(samples[index + BIT_SIZE * 9:index + BIT_SIZE * 10], frequency1, frequency2)

        if start_bit == 0 and stop_bit == 1:
            for n in range(1, 9):
                start_bit = bit_extractor(samples[index + BYTE_SIZE * n:index + BIT_SIZE + BYTE_SIZE * n], frequency1, frequency2)
                stop_bit = bit_extractor(samples[index + BYTE_SIZE * n + BIT_SIZE * 9:index + BYTE_SIZE * n + BIT_SIZE * 10], frequency1, frequency2)

                if start_bit == 0 and stop_bit == 1:
                    start_found += 1
                else:
                    start_found = 1
                    index += BIT_SIZE
                    break

        else:
            index += BIT_SIZE

    return index



file = "message.wav"
wave = wavfile.read(file)
text = []

if len(wave[1].shape) == 1:
    index = find_start_bit(wave[1], 2025, 2225)
    print("start bit at:", index)
    for i in range(index, wave[1].shape[0], BYTE_SIZE):
        bytes = byte_extractor(wave[1][i:i+BYTE_SIZE], 2025, 2225)
        text.append(chr(bytes))

    message_output = ''.join(text)
    with open(file.split('.')[0] + '.txt', 'w') as f:
        f.write(message_output)

if len(wave[1].shape) > 1 and wave[1].shape[1] == 2:
    left = wave[1][:, 0]
    right = wave[1][:, 1]
    wave = np.array([((left[n] + right[n]) // 2) for n in range(wave[1].shape[0])])

    try:
        index = find_start_bit(wave, 2025, 2225)
        print("start bit at:", index)
        for i in range(index, wave.shape[0], BYTE_SIZE):
            bytes = byte_extractor(wave[i:i+BYTE_SIZE], 2025, 2225)
            text.append(chr(bytes))
    except:
        print("ERROR")

    message_output = ''.join(text)
    with open(file.split('.')[0] + '.txt', 'w') as f:
        f.write(message_output)