---
name: browser
description: Drive the user's open, logged-in Chrome or Edge with the Chrome DevTools MCP server, including inspecting live pages, filling forms, and running scripts in a page.
---

# Drive a browser

Use only the configured `chrome-devtools` MCP server, not a CLI daemon, a raw CDP socket, or a second server, because every new connection can make the user allow remote debugging again.

## Setup

The server attaches to the running browser through its user-data root, not a profile folder inside it, and never launches one:

```json
{
  "command": "bunx",
  "args": [
    "chrome-devtools-mcp",
    "--autoConnect",
    "--userDataDir",
    "C:/Users/<user>/AppData/Local/Microsoft/Edge/User Data",
    "--no-usage-statistics",
    "--no-performance-crux"
  ]
}
```

The two `--no-*` flags stop data from being sent to Google. Remote debugging must be on at `edge://inspect/#remote-debugging`, and the user accepts the connection prompt once per server start.

## Verify the attach

A connected server proves nothing about the browser, so call `list_pages` first.

- `Could not connect to Chrome` means the browser is closed or remote debugging is off. Ask the user to fix it.
- A timeout is often a slow first attach, because the server attaches to every tab, worker, and iframe. Retry once.
- A second timeout means Edge needs a restart. Stop and ask the user, and do not try another route.
- A page that looks logged out usually means the attach went to the wrong browser, so check `list_pages` for the user's real tabs.

## Reach a page

Stop at the first option that works, because each one disturbs the user more:

1. Plain HTTP without a browser. A 403 is often hotlink protection, which a browser `User-Agent` and a same-origin `Referer` usually pass.
2. `fetch()` through `evaluate_script` in a page that is already open. One script doing N fetches beats N tool calls.
3. One scratch tab from `new_page`, reused with `navigate_page` and closed when done. A new tab always comes to the front, so when the user named their own tab, hand focus back with `select_page` and `bringToFront`.

## Rules

- Act only on the tabs you open or the user names. Read `list_pages` as metadata without looking around the user's other tabs.
- `Execution context was destroyed` after a click means the navigation worked, so poll the new page instead of clicking again.
- Confirm a login-dependent state on the intended site without exposing credentials.
