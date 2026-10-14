# Web and CDN

## Find what serves the domain

- Resolve the name with `Resolve-DnsName`, following CNAMEs, for both A and
  AAAA. Check the hosts file for an existing override first.
- Identify the CDN from the CNAME chain and response headers. Many CDNs name the
  serving edge with an airport code, such as `cf-ray` on Cloudflare,
  `x-amz-cf-pop` on CloudFront, or `x-served-by` on Fastly. `MNL`, `NRT`, and
  `SIN` mean Manila, Tokyo, and Singapore.
- Compare answers from different resolvers, such as the ISP resolver, `1.1.1.1`,
  and `8.8.8.8`. CDNs pick edges by resolver location, so a resolver far away
  can send the user to a far edge.

## Compare edges

- Test a candidate edge without changing the system with
  `curl.exe --resolve HOST:443:IP`, keeping the real URL, SNI, and certificate
  checks. Never use `-k`.
- Use `-w` to record connect, TLS, first byte, and total time, and download to
  `NUL`. Pick one representative static file and reuse it for every candidate.
- Get candidates from DNS answers on different resolvers or networks, and from
  the provider's documentation. Check that each candidate serves the hostname,
  because many CDNs route per tenant.
- Repeat rounds in alternating order, and watch cache headers so a warm cache
  does not look like a fast edge.

For example, x.com in Taiwan may land on a Singapore edge while Tokyo or Manila
is faster. Measure that rather than assume it, because CDN routing changes.

## Fix

- Changing the DNS resolver keeps CDN failover and is the gentlest fix.
- A hosts entry pins one edge. It breaks when the CDN retires that IP, so give a
  rollback trigger, and remember it affects every app on the machine.
- After a hosts change, flush with `ipconfig /flushdns`, restart the browser,
  and verify with a normal request. Browsers with secure DNS may resolve on
  their own, so check the browser too.
