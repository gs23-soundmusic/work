Contains work done by Gabriel Santana Soto for the modem assignment.

This tool decodes text messages embedded in audio using the Bell 103 modem FSK protocol. It analyzes each bit by comparing tone power at 2025 Hz and 2225 Hz, reconstructs bytes from 160‑sample bit windows, and outputs the recovered message as plain text. In addition, it checks for mono or stereo audio, before attempting message extraction.

The script reads `message.wav`, extracts all bytes, and writes the decoded text to `message.txt`.

The file `300bps.txt`, contains a partially decoded message from "300bps N, 8, 1/Terminal Mode or ASCII Download". This portion was not fully completed. The issue arises from a bit error in the wav file, so further santization is required for a full message capture.

Dependencies: numpy, scipy

Run with Python 3.12+.