# Synth

A simple synthesizer that generates sound using sawtooth waves by Gabriel Santana Soto.

Generates sound using sawtooth waves with adjustable volume and waveform type (sawtooth, sine, triangle, or square). Driven by MIDI files to play notes and control volume based on velocity.

Usage:

- `python app.py`

To specify a different waveform type, use the flag of the desired waveform name (e.g., `sine`, `square`, or `triangle`). The program will use `sawtooth` by default:

- `python app.py --square`

Dependencies: numpy, sounddevice, mido