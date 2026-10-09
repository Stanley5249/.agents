---
description:
  Compare CDN endpoints for a hostname and recommend a faster stable route
argument-hint: "[hostname] [test-url]"
---

# Select a faster CDN endpoint

Help me find a stable, faster CDN endpoint for the target hostname on my current
network. Diagnose first, then propose a reversible configuration change only
when measurements support one. Use English internally and follow my conversation
language for explanations.

Target hostname: ${1:-ask me for the target hostname} Representative HTTPS URL:
${2:-select a suitable public URL with me}

## Scope and approval

- Follow applicable user, project, and system-change rules.
- Confirm the target hostname and a representative HTTPS URL before testing. If
  I provide several hostnames, measure and choose endpoints independently for
  each.
- Perform read-only diagnostics first. Show the exact diff and backup plan, then
  ask for approval before changing hosts, DNS, proxy, VPN, or browser settings.
- Use the configured browser connection only after browser-automation approval.
  Prefer public resources and command-line measurements when sufficient.
- Use existing tools. Ask before installing tools or starting delegated agents.
- Keep tests bounded across the entire task: at most six candidate IPs per
  hostname, three initial samples per candidate, a 15-second timeout per
  request, and 25 MB total downloaded response bodies, including discovery,
  warm-ups, and retests. Account for the expected sizes before testing, enforce
  a transfer limit, and stop when the remaining budget is insufficient. Ask
  before expanding the test.
- Use public, read-only requests. Ask before using authenticated URLs or private
  resources, protect credentials and signed URLs, and omit secrets from reports.

## Establish the baseline

1. Read the current hosts file and identify overrides for the target hostname.
   Preserve unrelated entries and explain whether the baseline uses an override
   or normal hostname resolution.
2. Inspect active interfaces, routes to resolved endpoints, system proxy
   settings, and DNS answers, including relevant CNAME, A, and AAAA records.
   Identify the CDN provider using DNS, response headers, and supporting
   provider documentation. Treat provider identification as uncertain when
   evidence is incomplete.
3. Identify the ISP only when relevant, and omit public client IPs from the
   final report. Explain when a proxy performs resolution or prevents direct
   endpoint comparisons.
4. Select a representative resource, normally around 200–500 KB, that reflects
   my use case and fits the traffic budget. Reuse the exact URL across
   candidates. Prefer a complete static resource; use an identical byte range
   only when the server supports it and explain what the partial transfer
   measures.
5. Record redirects and the hostname that actually serves the resource. Confirm
   any additional hostname before testing it. A redirect to another hostname
   does not measure the target endpoint's transfer performance.
6. Measure the current effective endpoint and DNS-selected endpoints explicitly.
   Distinguish hosts overrides from ordinary DNS answers. Compare IPv4 and IPv6
   separately when both are available, then verify normal client behavior.
7. Optionally compare a similarly sized file on another CDN. If a second network
   is available, ask me to switch manually, finish a bounded comparison, and
   clearly stop so I can switch back.

## Discover and measure candidates

- Obtain candidates from current DNS answers, provider documentation, or
  credible, dated references for the target service. Treat published lists as
  candidates to validate. Use a bounded list of known endpoints rather than
  scanning IP ranges.
- Verify that each candidate can serve the original hostname. CDN providers may
  use hostname-specific routing, tenant configuration, or dynamic endpoint
  pools. Recommend retaining managed DNS when a fixed mapping would weaken
  reliability.
- Test candidates with `curl --resolve HOST:443:IP`, retaining the original
  HTTPS URL, Host header, SNI, and certificate verification. Use curl's
  bracketed IPv6 address syntax when needed. Keep certificate verification
  enabled instead of using `-k` or `--insecure`.
- Use the same proxy mode and request options across candidates. Explain whether
  the test reaches the candidate directly or through a proxy; obtain approval
  before changing the network path. Verify the actual connected endpoint.
- Download each measured response body to the platform's null sink. Record HTTP
  status, remote IP, DNS/connect/TLS timing, time to first byte, total time,
  downloaded bytes, throughput, and provider-specific edge/cache headers when
  available. Label forced-resolution DNS timing separately from normal DNS
  lookup.
- Record cache hits and misses; keep warm-up results separate if cache state
  affects the comparison. Use identical cache keys instead of random query
  parameters that create unnecessary cache misses.
- Alternate candidate order between rounds and use low concurrency so tests do
  not compete with each other. Note other downloads or playback as a possible
  confounder; ask before interrupting them.
- Verify expected media type and content. Compare a content hash against the
  baseline when practical; equal byte counts alone are weaker evidence. Reject
  TLS failures, error pages, and unexpected content. Account for content
  encoding and dynamic responses when interpreting differences.
- Interpret edge-location and cache headers using the identified provider's
  documentation. Distinguish serving edges from shields and upstream caches.
  Report relevant labels and uncertainty; IP geolocation alone is insufficient.
- CDN anycast and routing can change. Distinguish selecting a serving edge from
  selecting the entire transit or CDN-internal path. Describe fixed mappings as
  temporary, network-specific workarounds rather than permanent location
  control.

## Select and report

Present a compact table per hostname with candidate IP, address family, observed
edge labels, success count, median total time, worst total time, and cache
state. Prioritize consistent successful transfers, then median and worst-case
performance. Explain whether the tested resource represents the actual workload,
including any limits from HTTP version, proxy behavior, or browser connection
reuse.

Retest the current endpoint and the proposed winner for three additional rounds
within the original traffic budget. Recommend a change only when the improvement
is repeatable and useful. Keep the current configuration when evidence is weak
or provider-managed routing is safer. Choose based on measurements rather than
assuming a particular provider, country, or city is fastest.

Separate measured facts from hypotheses. Endpoint comparisons can demonstrate a
path-specific problem but do not alone assign responsibility to an ISP, transit
provider, or CDN. Treat ICMP loss as supporting evidence, not proof of HTTP
packet loss. A fast DNS lookup does not rule out DNS-based endpoint selection as
a factor.

## Apply only after approval

1. Choose the narrowest reversible change supported by the evidence. For a hosts
   mapping, show the exact diff and explain that the mapping affects system
   hostname resolution, not just one browser. Explain that browsers or proxies
   may use their own resolution path and that IPv4 and IPv6 behavior both
   matter.
2. Explain the maintenance risk of pinning a CDN IP, including failover,
   endpoint retirement, and routing changes. Provide a rollback trigger if
   availability or performance worsens.
3. Back up any file being changed to a timestamped location. For hosts edits,
   preserve unrelated mappings, comments, encoding, and line endings. Update
   multi-hostname lines carefully and keep one intended mapping per hostname and
   address family, with the intended family preference documented.
4. Obtain administrator authorization through the normal OS prompt when
   required. Stop and report permission failures rather than bypassing OS
   protection.
5. Apply only the approved change. For hosts edits, flush the OS DNS cache and
   ask me to fully restart the browser; close it yourself only with explicit
   permission.
6. Verify hostname resolution with the system resolver, such as
   `[System.Net.Dns]::GetHostAddresses(...)` on Windows. Use a normal HTTPS
   request without `--resolve` to confirm the actual remote IP and transfer
   behavior. Use `nslookup` for DNS queries and the system resolver for
   hosts-file verification.
7. After browser restart, verify browser behavior if authorized. Label the
   result as system-level verification when browser verification is still
   pending.
8. Give exact rollback instructions and the backup path. If reverting after
   other edits, undo only this workaround so newer unrelated changes remain
   intact.

Finish with the measured recommendation, limitations, and completed side
effects: files changed, backup paths, cache flushing, and any processes or
browser sessions left open. Stop all diagnostic work when the bounded test is
complete.
