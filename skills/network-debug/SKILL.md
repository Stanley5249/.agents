---
name: network-debug
description:
  Diagnose and fix a slow, unstable, or unreachable network service, such as a
  slow website or CDN, a game that lags on Wi-Fi but not on mobile data, or a
  domain that fails on one network.
argument-hint: "[symptom, domain, or app]"
disable-model-invocation: true
---

# Debug a network problem

Find where the slow part of the path is, then fix the narrowest part you can
control. The user's machine is Windows, so prefer PowerShell and built-in tools
such as `Resolve-DnsName`, `Test-NetConnection`, `pathping`, and `curl.exe`.

## Principles

- Compare to isolate the cause: another network, another device, IPv4 against
  IPv6, another endpoint, another resolver. A difference between two paths is
  the strongest evidence you get.
- Ask the user what differs between the fast and slow cases before measuring.
  They often already know, such as "fast on mobile data".
- Measure before changing anything. Keep tests small and bounded, and use
  public, read-only requests.
- Prefer the narrowest reversible fix, and explain what it costs later, such as
  a pinned CDN IP that stops failing over. Back up any file you change and give
  the rollback.
- Separate measured facts from guesses about who is at fault. A slow hop in a
  traceroute can be ICMP rate limiting, not real loss.

## Where to look

| Symptom                                              | Read                          |
| ---------------------------------------------------- | ----------------------------- |
| A website or download is slow, or one domain is slow | `references/web-cdn.md`       |
| Fast on one network or device, slow on another       | `references/path-and-link.md` |
| A game, voice call, or other real-time UDP app lags  | `references/realtime-udp.md`  |

Most problems touch more than one file. A slow site on Wi-Fi only, for example,
starts in `path-and-link.md` and may end in `web-cdn.md`.

## Report

State where the problem is, the evidence for it, the fix you recommend or
applied, and its limits. List changed files, backups, and flushed caches.
