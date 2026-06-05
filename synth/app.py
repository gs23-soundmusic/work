import numpy as np
import sounddevice as sd
from mido import MidiFile
import time
import getopt
import sys



SAMPLE_RATE = 48000
WAVE_SCALE = 0.708
DURATION = 0.01



#We will use the now-familiar sawtooth wave as our synthesizer sound. Run it at -3dBFS: about 0.708 of full scale.
def waveforms(note, duration, type):
    frequency = 440 * (2 ** ((note - 69) / 12))
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    
    if type == 'sawtooth':
        return WAVE_SCALE * (2 * (t % (1 / frequency)) - 1)
    elif type == 'sine':
        return WAVE_SCALE * np.sin(t * (2 * np.pi * frequency))
    elif type == 'triangle':
        return WAVE_SCALE * np.abs(np.sin(t * (2 * np.pi * frequency)))
    elif type == 'square':
        return WAVE_SCALE * np.sign(np.sin(t * (2 * np.pi * frequency)))


#Put a fixed attack-release volume envelope on the sawtooth. Start a note by ramping up linearly in amplitude from zero to full scale over 10 milliseconds. End the note by ramping down to zero over 10 milliseconds.
def ar_envelope(wave, attack=DURATION, release=DURATION):
    envelope = np.ones_like(wave, dtype=float)
    envelope[:int(attack * SAMPLE_RATE)] = np.linspace(0, 1, int(SAMPLE_RATE * attack))
    envelope[int(-release * SAMPLE_RATE):] = np.linspace(1, 0, int(SAMPLE_RATE * release))
    return envelope * wave



#Drive the synthesizer with a MIDI file. Send the sound to your system's default output as usual.
def midi_events(in_midi, wave_type):
    for msg in in_midi:
        if msg.time > 0:
            print(msg)
        if msg.type == 'note_off' and msg.time > 0:
            wave = waveforms(msg.note, msg.time, wave_type)
            envelope = ar_envelope(wave)
            sd.play(wave * envelope, SAMPLE_RATE)
            time.sleep(msg.time)

        elif msg.type == 'note_on' and msg.time > 0:
            time.sleep(msg.time)
    
        elif msg.type == 'note_on' or msg.type == 'note_off' and msg.velocity == 0:
            pass



try:
    opts, args = getopt.getopt(sys.argv[1:], 'wst', ['sine', 'square', 'triangle'])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

wave_type = 'sawtooth'
for opt, arg in opts:
    if opt in ['-w', '--sine']:
        wave_type = 'sine'
    elif opt in ['-s', '--square']:
        wave_type = 'square'
    elif opt in ['-t', '--triangle']:
        wave_type = 'triangle'

input_midi = MidiFile('input.mid')
midi_events(input_midi, wave_type)