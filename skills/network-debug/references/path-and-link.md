# Path and local link

A service that is fast on mobile data but slow on Wi-Fi is not slow at the
server. The difference is somewhere in the home path:

```text
device -> Wi-Fi link -> router -> home ISP -> transit -> server
device -> mobile data --------> mobile ISP -> transit -> server
```

## Split the home path

- Wired or a phone hotspot on the same PC separates the Wi-Fi link from the home
  ISP. If the hotspot is fast, the device itself is fine.
- Check the Wi-Fi link with `netsh wlan show interfaces`: band, signal, and
  receive and transmit rates. 2.4 GHz and weak signal cause jitter.
- Test bufferbloat by pinging the router and an outside host while a large
  download runs. Latency that jumps under load points at the router queue, and
  router QoS or SQM fixes it.

## Compare the routes

- Run `pathping` or `tracert` to the server on both networks and compare where
  latency grows. A detour, such as Taiwan to Japan through the United States,
  points at ISP routing.
- Compare IPv4 and IPv6. One family may take a different route or be broken, and
  mobile networks often prefer IPv6.
- Probe MTU with `ping -f -l <size>` when large transfers stall but small
  requests work.

## Fix

- A Wi-Fi link problem: move to 5 GHz, closer to the router, or wired.
- A router problem: firmware, QoS, or a restart, which the user does on the
  router.
- An ISP route problem: the user can report it to the ISP with both traceroutes
  as evidence. A VPN or a game accelerator that exits on a better route is the
  workaround, and is also a cheap test of this hypothesis.
