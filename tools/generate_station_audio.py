#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 DISK TELEVISION contributors
"""Original DISK TELEVISION audio. Offline stdlib synthesis + local FFmpeg.

Edit SCORES (seconds, MIDI notes, amplitudes, pans) and PALETTE below.
No samples, soundfonts, downloads, API calls or third-party compositions.
Running this file only overwrites the six assets/audio/ident-* audio files.
Validation and measurements are printed as JSON, not written to the app.
"""
from array import array
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import wave

RATE = 44100
ROOT = Path(__file__).resolve().parents[1]
# start, duration, MIDI note, amplitude, pan [-1 left, +1 right], timbre
# Shared original signature F#4, A4, E5, D5; no reference transcription.
SCORES = {
    'station': (8.0, [
        (0.0, 7.7, 50, .20, -.12, 'pad'),
        (0.1, 7.5, 57, .12, .25, 'pad'),
        (.25, 7.2, 64, .10, -.36, 'pad'),
        (.40, 7.0, 66, .09, .34, 'pad'),
        (.50, 2.30, 66, .40, -.38, 'glass'),
        (1.34, 2.35, 69, .35, .31, 'glass'),
        (2.43, 2.70, 76, .28, -.18, 'glass'),
        (3.58, 3.30, 74, .37, .20, 'glass'),
        (4.50, 2.80, 55, .14, -.24, 'pad'),
        (4.55, 2.70, 62, .09, .30, 'pad'),
    ]),
    'next': (2.6, [
        (0.0, 2.5, 62, .18, -.20, 'pad'),
        (.0, 2.5, 69, .12, .30, 'pad'),
        (.10, 1.8, 66, .34, -.30, 'glass'),
        (.48, 1.7, 76, .28, .26, 'glass'),
        (.96, 1.5, 74, .36, -.08, 'glass'),
    ]),
    'night': (11.0, [
        (0.0, 10.8, 47, .22, -.18, 'pad'),
        (.2, 10.4, 54, .14, .30, 'pad'),
        (.4, 10.0, 61, .10, -.35, 'pad'),
        (.6, 9.8, 64, .11, .25, 'pad'),
        (1.0, 3.8, 66, .26, -.36, 'glass'),
        (2.45, 3.9, 69, .22, .30, 'glass'),
        (4.30, 4.2, 76, .18, -.18, 'glass'),
        (6.25, 4.2, 74, .24, .24, 'glass'),
        (5.0, 5.5, 50, .10, .08, 'pad'),
    ]),
}
PALETTE = {
    'pad': {'attack': .70, 'release': 1.30, 'partials': ((1, 1), (2, .12), (3, .025))},
    'glass': {'attack': .065, 'release': .48, 'partials': ((1, 1), (2, .18), (3, .035), (4.01, .012))},
}
PEAK_LIMIT = 10 ** (-4.5 / 20)  # MP3 overshoot margin below required -3 dBFS
TARGET_RMS = 10 ** (-20 / 20)


def smooth(x):
    """Raised-cosine ramp, clamped to [0, 1]."""
    return .5 - .5 * math.cos(math.pi * max(0., min(1., x)))


def synthesize(variant):
    seconds, events = SCORES[variant]
    count = round(seconds * RATE)
    left, right = array('d', [0.]) * count, array('d', [0.]) * count
    for start, duration, midi, amplitude, pan, timbre in events:
        color = PALETTE[timbre]
        frequency = 440. * 2 ** ((midi - 69) / 12)
        gains = (math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4))
        first = round(start * RATE)
        for j in range(min(round(duration * RATE), count - first)):
            t = j / RATE
            env = smooth(t / color['attack']) * smooth((duration - t) / color['release'])
            if timbre == 'glass':
                env *= math.exp(-1.65 * t / duration)
            # Mild, slow phase movement; no sirens, noise, gates or glitches.
            phase = 2 * math.pi * frequency * t + .015 * math.sin(2 * math.pi * .23 * t)
            value = sum(weight * math.sin(ratio * phase) for ratio, weight in color['partials'])
            value *= env * amplitude
            left[first + j] += value * gains[0]
            right[first + j] += value * gains[1]
    # Deterministic, soft cross-channel reflections, finite tails, no feedback.
    dry_l, dry_r = array('d', left), array('d', right)
    for delay, wet in ((.173, .12), (.311, .075), (.487, .04)):
        shift = round(delay * RATE)
        for i in range(shift, count):
            left[i] += dry_r[i - shift] * wet
            right[i] += dry_l[i - shift] * wet
    fade_in = .09 if variant == 'next' else .22
    fade_out = .46 if variant == 'next' else (1.65 if variant == 'night' else 1.2)
    for i in range(count):
        gain = smooth(i / (RATE * fade_in)) * smooth((count - 1 - i) / (RATE * fade_out))
        left[i] *= gain
        right[i] *= gain
    peak = max(max(map(abs, left)), max(map(abs, right)))
    rms = math.sqrt((sum(x*x for x in left) + sum(x*x for x in right)) / (2 * count))
    scale = min(PEAK_LIMIT / peak, TARGET_RMS / rms)
    pcm = array('h')
    for l, r in zip(left, right):
        pcm.extend((round(l * scale * 32767), round(r * scale * 32767)))
    if sys.byteorder != 'little':
        pcm.byteswap()
    return pcm


def resolve_tool(name, explicit):
    candidate = explicit or os.environ.get(name.upper()) or shutil.which(name)
    if not candidate:
        local = Path.home() / 'AppData/Local/hermes/tools/ffmpeg-9.0.1-win32-x64/bin' / (name + '.exe')
        if local.is_file():
            candidate = str(local)
    if not candidate:
        raise SystemExit(f'Local {name} not found. Supply --{name}; no auto-download is performed.')
    subprocess.run([candidate, '-version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return candidate


def inspect(path, ffmpeg, ffprobe):
    """Fully decode each file and reject violations; return measured evidence."""
    metadata = json.loads(subprocess.check_output([ffprobe, '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))
    stream = metadata['streams'][0]
    assert int(stream['sample_rate']) == RATE and stream['channels'] == 2
    decoded = subprocess.check_output([ffmpeg, '-v', 'error', '-xerror', '-i', str(path), '-f', 'f32le', '-acodec', 'pcm_f32le', '-'])
    samples = array('f'); samples.frombytes(decoded)
    if sys.byteorder != 'little':
        samples.byteswap()
    seconds = len(samples) / (2 * RATE)
    variant = path.stem.removeprefix('ident-')
    assert seconds == SCORES[variant][0], (path, seconds)
    assert all(math.isfinite(x) for x in samples)
    peak = max(map(abs, samples))
    rms = math.sqrt(sum(x*x for x in samples) / len(samples))
    assert 0 < peak <= 10 ** (-3 / 20), (path, peak)
    assert max(map(abs, samples[:882])) < .01
    assert max(map(abs, samples[-882:])) < .01
    assert any(samples[i] != samples[i+1] for i in range(0, len(samples), 2))
    volume = subprocess.run([ffmpeg, '-hide_banner', '-i', str(path), '-af', 'volumedetect', '-f', 'null', '-'], check=True, capture_output=True, text=True).stderr
    return {
        'file': path.relative_to(ROOT).as_posix(),
        'decoded_seconds': seconds,
        'container_seconds': float(metadata['format']['duration']),
        'codec': stream['codec_name'], 'sample_rate': RATE, 'channels': 2,
        'peak_dbfs': round(20 * math.log10(peak), 4),
        'rms_dbfs': round(20 * math.log10(rms), 4),
        'volumedetect': dict(re.findall(r'(mean_volume|max_volume):\s*([-\d.]+) dB', volume)),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg', help='Existing local FFmpeg executable')
    parser.add_argument('--ffprobe', help='Existing local ffprobe executable')
    parser.add_argument('--verify-only', action='store_true', help='Read/decode existing assets, without writing')
    args = parser.parse_args()
    ffmpeg, ffprobe = resolve_tool('ffmpeg', args.ffmpeg), resolve_tool('ffprobe', args.ffprobe)
    folder = ROOT / 'assets/audio'
    if not args.verify_only:
        folder.mkdir(parents=True, exist_ok=True)
        for variant in SCORES:
            wav = folder / f'ident-{variant}.wav'
            with wave.open(str(wav), 'wb') as writer:
                writer.setnchannels(2); writer.setsampwidth(2); writer.setframerate(RATE)
                writer.writeframes(synthesize(variant).tobytes())
            subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(wav),
                            '-map_metadata', '-1', '-c:a', 'libmp3lame', '-b:a', '192k', '-ar', str(RATE), '-ac', '2',
                            '-id3v2_version', '3', '-write_xing', '1',
                            '-metadata', f'title=DISK TELEVISION - {variant}',
                            '-metadata', 'artist=DISK TELEVISION',
                            '-metadata', 'copyright=2026 DISK TELEVISION contributors; MIT',
                            str(wav.with_suffix('.mp3'))], check=True)
    results = [inspect(folder / f'ident-{v}.{ext}', ffmpeg, ffprobe) for v in SCORES for ext in ('wav', 'mp3')]
    assert max(r['rms_dbfs'] for r in results) - min(r['rms_dbfs'] for r in results) < 1.5
    print(json.dumps({'validated': len(results), 'files': results}, indent=2))


if __name__ == '__main__':
    main()
