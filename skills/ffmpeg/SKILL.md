---
name: ffmpeg
description:
  ffmpeg guidance useful for hardware-accelerated media processing and Windows
  interoperability.
---

## Hardware

Use the Arc iGPU through `-hwaccel qsv -hwaccel_output_format qsv` and the
`_qsv` encoder family (`av1_qsv`, `hevc_qsv`, `h264_qsv`) instead of software
encoders. The iGPU handles real-time AV1 encoding that software encoders cannot
match on this machine. NVENC, AMF, and VAAPI appear in this full build but do
not have matching GPU hardware here.

## Default target: AV1 video, Opus audio

The proven baseline for re-encoding existing video (not primary capture):

```
ffmpeg -hwaccel qsv -hwaccel_output_format qsv -i <source> -c:v av1_qsv -preset:v fast -global_quality:v <q> -g:v 120 -c:a libopus -vbr:a on -b:a <bitrate> <target.mkv>
```

- `-global_quality:v` scales with source resolution, not a fixed number: 26 at
  4K, 28 at 1080p, 30/32/34 down to 480p. Lower = higher quality. 28 is the
  1080p figure — don't reuse it at other resolutions unchecked.
- `-b:a` scales with channel count, not a fixed number: 48k per channel (96k for
  stereo). Raise it further for music-heavy sources.
- `-look_ahead_depth:v`, `-extbrc:v`, `-adaptive_i:v`, `-adaptive_b:v` are QSV
  tunables to try when quality needs a push, not defaults to set upfront — leave
  them unset until a specific source justifies measuring them.
- Use Matroska or WebM for AV1 with Opus unless the requested playback target
  has confirmed support for that combination in another container.
- This is a starting point, "not always the exact setup we want" — expect to
  retune per source, that's normal, not a sign of a bad default.

## Invocation hygiene

- `-hide_banner -nostdin -loglevel error -nostats` for scripted calls, so output
  is errors only.
- `-progress pipe:1` for machine-readable progress instead of parsing the human
  status line.
- Call ffmpeg directly with an argv array, never through a shell — keeps paths
  with spaces/special characters from being re-parsed.
- A zero exit status is not proof the output is valid — probe/verify the result
  before trusting it.
- Encode to a new path; never write over the source. Let the caller decide
  whether to replace the original afterward.

## Windows gotchas

- A filename with an unpaired UTF-16 surrogate (downloader output that mangled
  an emoji) can't be opened by ffmpeg at all — it converts the wide path to
  UTF-8 internally, the surrogate becomes `U+FFFD`, and it opens a name nothing
  on disk has. `Test-Path` succeeding while `ffprobe` says "No such file or
  directory" on the same path is the symptom. Workaround: the 8.3 short name
  (`GetShortPathNameW`, needs `unsafe`) or a temporary ASCII hardlink via
  `std::fs::hard_link`.
- Quote every path; don't rely on ffmpeg's own glob expansion on Windows.

## This install

`ffmpeg version 9.0-full_build-www.gyan.dev` (winget `Gyan.FFmpeg`) — full
build: QSV/NVENC/VAAPI/AMF/D3D11VA/D3D12VA, `libsvtav1`, `libaom-av1`,
`libvmaf`, `libopus` all compiled in. Re-run `ffmpeg -version` if this looks
stale.
