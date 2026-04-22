# work
Contains the work done for 516, the class Computers, Sound, and Music. 

## Clipped
This python project will generate two wav files, `sine.wav` and `clipped.wav`, as well as play clipped.wav through `sounddevice`. `sine.wav` is a 1 second, 440 Hz sine wave, sampled at 48 kHz, mono audio, 16-bit PCM, and with an amplitude limited to a quarter of the 16-bit range. `clipped.wav` is a similar sine wav with half the amplitude of the 16-bit range, but hard-clipped to +-8192. 

## Modem
This tool decodes text messages embedded in audio using the Bell 103 modem FSK protocol. It analyzes each bit by comparing tone power at 2025 Hz and 2225 Hz, reconstructs bytes from 160‑sample bit windows, and outputs the recovered message as plain text. The script reads message.wav, extracts all bytes, and writes the decoded text to message.txt.