This tool decodes text messages embedded in audio using the Bell 103 modem FSK protocol. It analyzes each bit by comparing tone power at 2025 Hz and 2225 Hz, reconstructs bytes from 160‑sample bit windows, and outputs the recovered message as plain text.

The script reads message.wav, extracts all bytes, and writes the decoded text to message.txt.

Dependencies: numpy, scipy

Run with Python 3.12+.