# aleatoric

Simple aleatoric music generator by Gabriel Santana Soto.

This script randomly selects a song structure, a four-chord line progression, and a starting key in the range A3–A4. It generates a melody of eighth notes where each note has an 80% chance of coming from the current chord and a 20% chance of coming from the major scale.

The melody is synthesized using sawtooth waves and can either play directly through the speaker or write a WAV file.

Usage:

- `python app.py` — play the generated song live
- `python app.py --output filename` — write the performance to `filename.wav`

Dependencies: numpy, scipy, sounddevice
