# JavaScript prototype v0.2

No dependencies. On a desktop with Node.js installed, run:

    node js/test.js
    node js/probe.js

The first command analyzes generated sine waves, not music recordings. The second inventories standard Linux audio metadata without opening audio devices. On Windows, Linux-specific fields will normally be empty.

The analyzer returns RMS, peak, dominant frequency and relative band power. Its simple DFT is a reference implementation, not optimized for real-time embedded use.

No live factory audio source has been verified. This is not an MGU Store package. Do not deploy to the vehicle yet. The Python prototype remains unchanged. No lighting, vehicle control, recording or system configuration changes are included.
