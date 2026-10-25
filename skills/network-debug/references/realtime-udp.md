# Real-time UDP

Games and voice calls use UDP, where jitter and loss matter more than bandwidth. HTTP tools such as `curl` and `Test-NetConnection` test TCP, so they do not measure the game path.

## Measure

- Find the server address and port from the game or its docs, such as Minecraft Bedrock servers on UDP 19132 by default. Resolve the name to see which region serves you.
- Use the game's own latency display as the main measure. Add `ping` and `pathping` to the server IP when it answers ICMP, and to hops near it when it does not.
- Watch jitter and loss over a few minutes, not one sample. Loss that only appears on Wi-Fi is the local link, which `path-and-link.md` covers.

## Common causes

- Wi-Fi jitter and bufferbloat, which hurt UDP games long before web pages feel slow.
- Router NAT handling of UDP, such as short UDP timeouts, missing UPnP, or a strict NAT type in the game.
- ISP routing to the game's region, which differs between the home ISP and the mobile ISP.
- IPv4 against IPv6, when the game supports both.

## Fix

- Wired or 5 GHz Wi-Fi for the local link.
- UPnP or a port forward on the router for strict NAT, which the user changes.
- A VPN or game accelerator for a bad ISP route. Compare latency with it on and off before recommending it.
