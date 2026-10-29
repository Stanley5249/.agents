---
name: network-debug
description: Diagnose and fix a slow, unstable, or unreachable network service, such as a slow website or CDN, a game that lags on Wi-Fi but not on mobile data, or a domain that fails on one network.
argument-hint: "[symptom, domain, or app]"
disable-model-invocation: true
---

# Debug a network problem

Find the slow part of the path, then fix the narrowest part the user controls. The machine is Windows, so use PowerShell and built-in tools such as `Resolve-DnsName`, `Test-NetConnection`, `pathping`, and `curl.exe`.

## Principles

- Isolate the cause by comparison, such as another network, another device, IPv4 against IPv6, another endpoint, or another resolver. Ask the user first what differs between the fast and slow cases, such as "fast on mobile data".
- Measure before changing anything, with small, bounded, read-only public requests.
- Prefer the narrowest reversible fix, and explain its later cost, such as a pinned CDN IP that stops failing over. Back up any file you change and give the rollback.
- A slow hop in a traceroute can be ICMP rate limiting rather than real loss.

## Where to look

- A website, a download, or one domain is slow: `references/web-cdn.md`.
- Fast on one network or device and slow on another: `references/path-and-link.md`.
- A game, a voice call, or another real-time UDP app lags: `references/realtime-udp.md`.

Many problems span more than one file, such as a site that is slow only on Wi-Fi.

## Report

State where the problem is, the evidence, the fix recommended or applied, and its limits. List changed files, backups, and flushed caches.
