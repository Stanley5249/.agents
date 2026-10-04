---
name: browser
description:
  Drive the user's open, logged-in Chrome or Edge with the Chrome DevTools MCP
  server, including inspecting live pages, filling forms, and running scripts in
  a page.
---

# Drive a browser

Ask for browser automation approval before the first DevTools call. Use the
`chrome-devtools` MCP server that is already configured. Do not start a CLI
daemon, a raw CDP socket, or a second MCP server, because every new browser
connection can prompt the user to allow remote debugging again.

## Setup

The server attaches to the running browser through its user-data root, not a
profile folder inside it, and never launches one:

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

The two `--no-*` flags stop data from being sent to Google. Remote debugging
must be on at `edge://inspect/#remote-debugging`, and the user accepts the
connection prompt once per server start.

## Verify first

A connected server proves nothing about the browser. Call `list_pages` first.

- Real tabs mean the attach works.
- `Could not connect to Chrome` means the browser is closed or remote debugging
  is off. Ask the user to fix it.
- A timeout is often a slow first attach, because the server attaches to every
  tab, worker, and iframe. Retry once.
- **A second timeout means Edge needs a reload.** Stop, ask the user to restart
  Edge, and do not retry or try another route.

For a login-dependent task, confirm the signed-in state on the intended site
without exposing credentials.

## Core loop

1. Use a page the user named, or open one scratch tab with `new_page`.
2. `take_snapshot` returns the accessibility tree with a `uid` per element.
3. `click`, `fill`, `type_text`, and similar tools act on that `uid`.

A `uid` is valid only for the snapshot it came from, so take a fresh snapshot
after anything that changes the page. Take a targeted screenshot only after the
interaction that matters.

## How to reach a page

Stop at the first option that fits, because each one disturbs the user more.

1. **Plain HTTP, no browser.** A 403 is often hotlink protection, and a browser
   `User-Agent` plus a same-origin `Referer` usually passes it.
2. **In-page `fetch()`.** Run it with `evaluate_script` in a page that is
   already open. One script doing N fetches beats N tool calls.
3. **One scratch tab, reused.** Drive it with `navigate_page`, and close it when
   done.

A new tab always comes to the front, and nothing reports which tab the user is
looking at. When the user named their tab, `select_page` with `bringToFront`
right after opening hands focus back.

## Rules

- **Do not browse the user's tabs.** `list_pages` is metadata, not a place to
  look around.
- **Check for a thrown script.** A failed `evaluate_script` returns an error,
  not a value. `Execution context was destroyed` after a click means the
  navigation worked, so poll the new page instead of clicking again.
- **Never claim an attachment you do not have.** If a page looks logged out,
  check `list_pages` for the user's real tabs before going on.
- If the same call fails twice for the same reason, stop and report the raw
  error.
