'''
Synth
Bart Massey

Let's write a personal MIDI synthesizer.
A MIDI soft synthesizer accepts MIDI key events via a system interface, and plays software-generatged audio on a system interface.
Of the several popular modern styles of synth, the easiest is probably straight waveform-based. Let's do sawtooth wave monophonic synthesis to start, with a fixed AR envelope.

MIDI Events
Opening a MIDI interface will give you access to KEY ON and KEY OFF events with velocities sent by a controller. We will mostly ignore the velocities for now. Exception: some MIDI controllers will not send KEY OFF events, but instead KEY ON events with 0 velocity. Treat a zero-velocity KEY ON as a KEY OFF.
For now, ignore all other MIDI messages.
Make your synth listen for a MIDI controller connection in the standard way for your system.

Waveform Synthesis
We will use the now-familiar sawtooth wave as our synthesizer sound. Run it at -3dBFS: about 0.708 of full scale.

AR Envelope
Put a fixed attack-release volume envelope on the sawtooth. Start a note by ramping up linearly in amplitude from zero to full scale over 10 milliseconds. End the note by ramping down to zero over 10 milliseconds.

Playing
Drive the synthesizer in such a way that key events are only processed between sample outputs. Try to keep the synth latency reasonably small: under 10ms is a good target. Send the sound to your system's default output as usual.

Assignment
Write the program described above. Submit the code, together with a 5 second video (no longer) SYNTH.mp4 (or other portable video format) with audio showing you playing notes on the MIDI synth.



Hints
In the likely case that you have no MIDI controller to try your synth with, several options:
Wire up your aleatoric music generator as a MIDI controller.
Find a MIDI file player and some MIDI files to send to your synth. Note that the MIDI files should be monotonic.
Grab vmpk or some other virtual MIDI keyboard.
For Python, still recommend sounddevice for playing on the speaker. Probably use mido with python-rtmidi for MIDI.
'''
import numpy as np
import sounddevice as sd
from mido import MidiFile
import time



SAMPLE_RATE = 48000
WAVE_SCALE = 0.708
DURATION = 0.01



def sawtooth_wave(note, duration):
    frequency = 440 * (2 ** ((note - 69) / 12))
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    return WAVE_SCALE * (2 * (t % (1 / frequency)) - 1)



def ar_envelope(wave, attack, release):
    envelope = np.ones_like(wave, dtype=float)
    envelope[:int(attack * SAMPLE_RATE)] = np.linspace(0, 1, int(SAMPLE_RATE * attack))
    envelope[int(-release * SAMPLE_RATE):] = np.linspace(1, 0, int(SAMPLE_RATE * release))
    return envelope * wave



def midi_events(in_midi):
    for msg in in_midi:
        if msg.time > 0:
            print(msg)
        if msg.type == 'note_off' and msg.time > 0:
            wave = sawtooth_wave(msg.note, msg.time)
            envelope = ar_envelope(wave, 0.01, 0.01)
            sd.play(wave * envelope, SAMPLE_RATE)
            time.sleep(msg.time)

        elif msg.type == 'note_on' and msg.time > 0:
            time.sleep(msg.time)
            sd.stop()
    
        elif msg.type == 'note_on' or msg.type == 'note_off' and msg.velocity == 0:
            sd.stop()
        


input_midi = MidiFile('input.mid')
midi_events(input_midi)