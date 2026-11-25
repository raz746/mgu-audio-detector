#!/usr/bin/env python3
"""Read-only audio-related Linux interface inventory; never captures sound."""

import datetime
import json
import os
from pathlib import Path
import platform
import re

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
AUDIO_HINT = re.compile(r"(alsa|audio|pipewire|pulse|jackd|avb|snd|sound|gstreamer)", re.I)


def read_text(path, limit=12000):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")[:limit]
    except (OSError, ValueError):
        return None


def names_in(path, limit=120):
    try:
        return sorted(p.name for p in Path(path).iterdir())[:limit]
    except (OSError, ValueError):
        return []


def available(cmd):
    for directory in os.environ.get("PATH", "/usr/bin:/bin").split(os.pathsep):
        if directory and os.access(os.path.join(directory, cmd), os.X_OK):
            return True
    return False


def audio_process_names(limit=80):
    result = []
    try:
        pids = [p for p in Path("/proc").iterdir() if p.name.isdigit()]
    except OSError:
        return result
    for pid in sorted(pids, key=lambda p: int(p.name)):
        # Never collect arguments or environment: these may contain secrets.
        name = (read_text(pid / "comm", 160) or "").strip()
        if AUDIO_HINT.search(name):
            result.append({"name": name[:80]})
        if len(result) >= limit:
            break
    return result


def scan():
    return {
        "schema": 1,
        "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "system": {
            "os": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
        },
        "device_nodes": {
            "/dev/snd": names_in("/dev/snd"),
            "/dev/audio_related": [n for n in names_in("/dev", 2000) if AUDIO_HINT.search(n)][:80],
        },
        "proc": {
            "asound_cards": read_text("/proc/asound/cards"),
            "asound_devices": read_text("/proc/asound/devices"),
        },
        "config_paths_present": [
            p for p in ("/etc/asound.conf", "/etc/pulse", "/etc/pipewire", "/usr/share/alsa")
            if Path(p).exists()
        ],
        "tools_present": {
            name: available(name)
            for name in ("arecord", "aplay", "amixer", "pactl", "pw-cli", "pw-dump", "gst-inspect-1.0", "dbus-send")
        },
        "audio_process_names": audio_process_names(),
        "conclusion": "INVENTORY_ONLY_CAPTURE_NOT_VERIFIED",
    }


def main():
    result = scan()
    print(json.dumps(result, indent=2))
    try:
        REPORTS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = REPORTS / ("audio_probe_" + stamp + ".json")
        with path.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)
            handle.write("\n")
        print("\nSaved:", path)
    except OSError as error:
        print("\nCould not save report (console output above is still available):", error)


if __name__ == "__main__":
    main()
