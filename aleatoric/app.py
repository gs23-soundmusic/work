'''
Background
Aleatoric MusicLinks to an external site.: is music that is "procedurally generated" using random numbers. An arbitrary random collection of sounds or notes is not going to be so usable; good aleatoric music generates some song structure to guide generation.
A computer program is a convenient way to generate aleatoric music. The computer has a random number generator and facilities for making sound.

Building a song
Song Structure: It is common to use repeated phrases or melodies in music. For starters, we will randomly pick one of the following song structures: "AABB/CC", "ABAB/CD", "AB/CDDD". Here each letter represents a line_structure_choice(a four chord loop in our case), with each letter being a repetition of that line_structure_choice The slash / separates the "verse" from the "chorus"; for now we will ignore this distinction.
line_structure_choiceStructure: Each "line" of our song will be a four-chord loop (one chord per measure). For starters, for a given line_structure_choicestructure (letter) we will choose randomly one of the following chord loops:

I-IV-ii-V
I-vi-ii-V
I-iii-IV-iv
I-V-ii-V
I-vi-IV-V
IV-I-vi-IV
I-V-vi-I
I-IV-iv-I
IV-V-I-I
vi-IV-I-V

No two labels in the song structure should correspond to the same loop.
Key: Pick a random key (base scale note) in the range A3-A4 inclusive.
Tempo: Pick a tempo between 80 and 160 beats per minute. The song will be in "common time" — four beats per measure, so 16 beats per line_structure_choice
Melody: For starters, the melody will just be eighth notes (8 notes per measure). Pick a note from the current chord with probability 0.8, else another note from the major scale. All notes should be in the first octave of the song's key (major scale).
Performance: The program should perform the melody using sawtooth waves. By default, it should play on the computer directly. When invoked with --output FILENAME.wav it should instead write the performance to FILENAME.wav as a WAV file: mono 48000sps 16-bit.

Assignment
Write the program described above. Submit the program, together with a sample output ALEATORIC.wav, a 48000sps mono 16-bit WAV file.

Hints
For Python, still recommend scipy.io.wavfile for WAV writing and sounddevice for playing on the speaker.
If you're having trouble generating a sawtooth wave, Wikipedia's explanationLinks to an external site. is pretty good.
If you are going to do the bonus stuff, you will probably want to be set up from the beginning to be able to do several notes at once: use a list of lists per eighth-note, or use a heap or other event structure.
For MIDI in Python, recommend using mido with python-rtmidi.
'''

import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import sys
import getopt
import random



SAMPLE_RATE = 48000
MINUTE = 60             #Seconds in a minute
EIGTH_NOTE = 0.5        #Half a beat

random.seed(0)

#Song Structure: For starters, we will randomly pick one of the following song structures:
SONG_STRUCTURES = ["1122/33", "1212/34", "12/3444"]
song_structure_choice = random.choice(SONG_STRUCTURES)


#Line Structure: Each "line" of our song will be a four-chord loop (one chord per measure):
LINE_STRUCTURES = ["1425", "1625", "1344", "1525", "1645", "4164", "1561", "1441", "4511", "6415"]
line_structure_choice= random.sample(LINE_STRUCTURES, len(set(song_structure_choice.replace("/", ""))))

#Key: Pick a random key (base scale note) in the range A3-A4 inclusive in frequency.
#Major scale of A is A3(220 Hz), B3(246.94 Hz), C#4(277.18 Hz), D4(293.66 Hz), E4(329.63 Hz), F#4(369.99 Hz), and G#4(415.30 Hz). Major chord of A is A3(220 Hz), C#4(277.18 Hz), and E4(329.63 Hz).
#Major scale of A#3 is A#3(233.08 Hz), C4(261.63 Hz), D#4(311.13 Hz), F4(349.23 Hz), F#4(369.99 Hz), and G#4(415.30 Hz). Major chord of A#3 is A#3(233.08 Hz), D#4(311.13 Hz), and F#4(369.99 Hz).
KEYS =            ["A3","A#3",  "B3",   "C4",   "C#4",  "D4",   "D#4",  "E4",   "F4",   "F#4",  "G4",   "G#4",  "A4",   "A#4",  "B4",   "C5",   "C#5",  "D5",   "D#5",  "E5",   "F5",   "F#5",  "G5",   "G#5"]
KEYS_FREQUENCIES = [220, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61]
valid_starting_key = [0, 2, 3, 5, 7, 8, 10, 12]
major_scale = [0, 2, 4, 5, 7, 9, 11]
major_chord = [0, 4, 7]
starting_key = random.choice(valid_starting_key)

#Tempo: Pick a tempo between 80 and 160 beats per minute. The song will be in "common time" — four beats per measure, so 16 beats per line
tempo = 160


#Melody: Pick a note from the current chord with probability 0.8, else another note from the major scale.
def pick_melody_note(key, scale):
    index = KEYS_FREQUENCIES.index(key)
    octave = KEYS_FREQUENCIES[index:index+13]


    index = major_scale[scale - 1]
    #print(index)

    if random.random() < 0.8:
        #return major chord
        #return KEYS_FREQUENCIES[index + random.choice(major_chord)]
        return octave[0]
    else:
        #return major scale
        return octave[random.choice(major_scale) % len(octave)]


#Performance: The program should perform the melody using sawtooth waves. By default, it should play on the computer directly. When invoked with --output FILENAME.wav it should instead write the performance to FILENAME.wav as a WAV file: mono 48000sps 16-bit.
def sawtooth_wave(frequency):
    duration = MINUTE / tempo * EIGTH_NOTE
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return 0.5 * (t * frequency - np.floor(0.5 + t * frequency))

song = None
print(song_structure_choice, line_structure_choice)
print("starting key:", KEYS[starting_key])
for chord in song_structure_choice.replace("/", ""):
    l = line_structure_choice[int(chord) - 1]
    for c in l:
        note = pick_melody_note(KEYS_FREQUENCIES[starting_key], int(c))

        print(c, note, end=", ")
        if song is None:
            song = sawtooth_wave(note)
        else:
            song = np.concatenate((song, sawtooth_wave(note)))
    print()

print(song)

    

output = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "o:", ["output="])
    for opt, arg in opts:
        if opt in ("-o", "--output"):
            if '.' in arg:
                output = '.'.split(arg)[0]
            else:
                output = arg
            wavfile.write(f'{output}.wav', SAMPLE_RATE, song)

except getopt.GetoptError as err:
    print(err)
    print("Usage: app.py -o <file> -v")
    sys.exit(2)