---
name: ffmpeg-qsv
description: Encode or re-encode video with ffmpeg on Windows, using the Intel Arc iGPU through Quick Sync Video (QSV)
disable-model-invocation: true
---

# ffmpeg with QSV on Windows

## Hardware

Use the Arc iGPU through `-hwaccel qsv -hwaccel_output_format qsv` and the `_qsv` encoders, such as `av1_qsv`, `hevc_qsv`, and `h264_qsv`, because software encoders cannot match its real-time AV1. NVENC, AMF, and VAAPI appear in this full build, but the machine has no matching GPU.

## Default target: AV1 video, Opus audio

The proven baseline for re-encoding existing video, not primary capture:

```sh
ffmpeg -hwaccel qsv -hwaccel_output_format qsv -i <source> -c:v av1_qsv -preset:v fast -global_quality:v <q> -g:v 120 -c:a libopus -vbr:a on -b:a <bitrate> <target.mkv>
```

- `-global_quality:v` scales with source resolution: 26 at 4K, 28 at 1080p, and 30, 32, 34 down to 480p. Lower means higher quality.
- `-b:a` scales with channel count at 48k per channel, such as 96k for stereo. Raise it for music-heavy sources.
- `-extbrc:v`, `-look_ahead_depth:v`, `-adaptive_i:v`, and `-adaptive_b:v` are tunables to measure on a source that needs more quality, not defaults. `-look_ahead_depth:v` works only with `-extbrc:v 1`.
- Use Matroska or WebM for AV1 with Opus unless the playback target confirms support in another container.
- Expect to retune per source.

## Invocation

- Use `-hide_banner -nostdin -loglevel error -nostats` for scripted calls, and `-progress pipe:1` for machine-readable progress.
- Encode to a new path and never over the source. Probe the result before trusting it, because a zero exit status does not prove the output is valid.

## Windows gotchas

A filename with an unpaired UTF-16 surrogate, such as downloader output that mangled an emoji, cannot be opened by ffmpeg, because ffmpeg converts the wide path to UTF-8 and the surrogate becomes `U+FFFD`. The symptom is `Test-Path` succeeding while `ffprobe` reports "No such file or directory". Pass the 8.3 short path from `GetShortPathNameW` or a temporary ASCII-named hardlink instead.

## This install

The gyan.dev full build from winget, `Gyan.FFmpeg`. Check `ffmpeg -version` for the version and enabled libraries.
