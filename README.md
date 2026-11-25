# MGU Audio Detector

Read-only diagnostic prototype for investigating whether BMW MGU exposes an audio capture or monitoring interface usable for music-synchronized ambient lighting.

## Status

**v0.1: audio-interface inventory only.** No audio capture, bass detection, playback-state detection, or compatibility with all factory audio sources has been confirmed. This is **not yet an installable MGU Store app**.

The initial script identifies accessible Linux audio-related devices and services. It does not record audio, modify audio configuration, write to vehicle buses, or control lights. Test only while safely parked.

## Run on a test Linux machine or an authorized MGU SSH session

```sh
python3 --version
python3 diagnostic/audio_probe.py
```

Results are printed and saved to a timestamped JSON file under `reports/`. If Python 3 is unavailable on the MGU, **do not install packages or modify the head unit merely for this test**. Let us adapt the detector to the available shell/runtime instead.

**Review reports before sharing them**: paths, device names and process metadata can be identifying. The reports folder is excluded from git.

## What the report means

Presence of ALSA, PulseAudio, PipeWire or AVB-related processes or files only suggests possible components. It does not establish that the combined audio playing through the BMW speakers is available to applications. Absence does not definitively rule it out either.

## Project boundaries

- Do not disturb the existing Ambient Config installation.
- No ECU coding, diagnostic writes, lighting writes or system changes.
- No microphone or speaker recordings.
- No stored credentials or audio content.
- Future reactive lighting must be parked-only and preserve OEM warnings.

Related implementation reference: [cauliflowermossgrape/idrive7-apps](https://github.com/cauliflowermossgrape/idrive7-apps). This is an independent project.
