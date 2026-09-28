---
name: browser
description:
  Drive Chrome or Edge from the terminal with `bunx chrome-devtools`, including
  attaching to the user's open, logged-in browser, inspecting live pages, and
  scripting many DevTools calls.
---

# Drive a browser from the terminal

`bunx chrome-devtools <tool> [arguments] [flags]` is the CLI that ships with
`chrome-devtools-mcp`. A background daemon holds the browser connection, and
every CLI call is a short-lived client of that daemon. Required arguments are
positional, optional ones are flags, and `--help` works on any command.

Run it through `bunx` so there is nothing to install globally. Pass
`--no-usage-statistics --no-performance-crux` when starting the daemon, because
both send data to Google by default.

## Quick start

```sh
timeout 120 bunx chrome-devtools status   # always first
```

`status` shows whether a daemon is running and with which flags. Skipping it and
calling `start` again throws away an attach that has already finished.

To attach to the browser the user already has open, pass its user-data root, not
a profile folder inside it:

```sh
timeout 180 bunx chrome-devtools start --autoConnect \
  --userDataDir "$LOCALAPPDATA/Microsoft/Edge/User Data" \
  --no-usage-statistics --no-performance-crux
```

For Chrome on Windows, the root is `$LOCALAPPDATA/Google/Chrome/User Data`.
Without `--autoConnect`, the daemon launches its own browser, which is headless
by default and has none of the user's logins. That is the right choice for
testing a local dev server.

Then check that the daemon really drives the intended browser:

```sh
timeout 180 bun <this skill>/scripts/probe.ts   # opens, reads, and closes one page
```

Bound every call with a timeout. The CLI gives up at 60 seconds, but a wedged
call can hang past that. In Bash, use coreutils `timeout`. In PowerShell, do not
use `timeout.exe`, because it is a sleep, not a limit.

## Core loop

1. `list_pages` gives page ids. Use a page the user named, or open your own.
2. `take_snapshot <pageId>` returns the accessibility tree with a `uid` per
   element.
3. `click`, `fill`, `type_text`, and similar tools act on that `uid`.

```
uid=1_0 RootWebArea "Example Domain" url="https://example.com/"
  uid=1_1 heading "Example Domain" level="1"
```

A `uid` is valid only for the snapshot it came from, so take a fresh snapshot
after anything that changes the page. For a visual or interaction change, take a
targeted screenshot after the interaction that matters, not a full-page one at
the start. `--output-format=json` gives machine-readable output.

## How to reach a page

Work down this list and stop at the first option that fits, because each step
costs more and disturbs the user more than the one before.

1. **Plain HTTP, no browser.** A 403 outside the browser is often hotlink
   protection, and a browser `User-Agent` plus a same-origin `Referer` is
   usually the whole gate. Move into the browser only when the host rejects the
   client itself, such as by TLS fingerprint.
2. **In-page `fetch()`.** A JSON API or plain HTML needs no tab of its own. Run
   the fetch inside a page that is already open. One `evaluate_script` doing N
   fetches also beats N CLI calls, each of which costs 1 to 2 seconds of
   startup.
3. **One scratch tab, reused.** For anything needing real navigation, rendering,
   or a click, open one tab, hand focus back to the user's tab, drive the
   scratch tab with `navigate_page`, and close it when done.

A new tab always steals focus. `new_page --background` has no effect, there is
no new-window option, and `window.open` is blocked by the popup blocker.
`select_page <userTab> --bringToFront true` right after opening restores the
user's tab, and later calls against the scratch tab leave the selection alone.
`newPage` in the bundled client does this for you.

## Rules

- **One connection.** Do not open a raw CDP socket, a second `--autoConnect`
  daemon, or a homegrown daemon. Each new connection re-prompts the user to
  allow remote debugging.
- **Do not browse the user's tabs.** `list_pages` is tab metadata, not a place
  to look around. Use a page the user named, or your own scratch tab.
- **Check for a thrown script.** A failed `evaluate_script` returns an error,
  not a value. `Execution context was destroyed` after a click means the
  navigation worked, so poll the new document instead of retrying the click.
- **Put quote-heavy JavaScript in a file.** Shells, PowerShell especially,
  mangle nested quotes.
- **End standalone scripts with `process.exit(0)`.** An open handle keeps the
  event loop alive after the socket closes.
- **Never claim an attachment you do not have.** A launched browser and an
  attached one both report a normal user agent. Check the `args` line
  of `status` for `--auto-connect` if a page looks logged out, and never do a task that needs the
  real session in a throwaway browser.

## When to stop

| Symptom                                            | Do                                             |
| -------------------------------------------------- | ---------------------------------------------- |
| `Network.enable timed out`, returns in about 1s    | `stop`, then `start` again                     |
| `Timeout waiting for daemon response`, exactly 60s | retry once without `stop`, then stop           |
| `Could not connect to Chrome ... 403`              | ask the user to open the browser, then `start` |
| `list_pages` shows only `about:blank`              | two attempts, then report the raw output       |

If a command fails twice for the same reason, stop and report the raw output. A
wait loop burns the turn, and the real fix is often fewer open tabs, so ask
before closing any.

## Scripting many calls

[scripts/devtools-client.ts](scripts/devtools-client.ts) talks to the daemon's
local control socket. That is local IPC, not a second browser connection, so it
never prompts and it skips the per-call CLI startup. `callTool` reaches any tool
the CLI has. Import it from a project script, or copy it into the project when
the project must not depend on this skill's path.

## Further reading

- [reference/troubleshooting.md](reference/troubleshooting.md): what each
  failure means, duplicate daemons, headless defaults, and two profiles sharing
  one user-data root.
- [reference/daemon-socket.md](reference/daemon-socket.md): the socket wire
  protocol and the fallback if a release changes it.

For deeper topics, the upstream repository ships its own skills, such as the
full CLI command reference, accessibility audits, LCP tuning, memory leaks, and
cookie debugging. List them with:

```sh
bunx skills add ChromeDevTools/chrome-devtools-mcp --list
```

For a one-off need, print one without installing anything:

```sh
bunx skills use ChromeDevTools/chrome-devtools-mcp@chrome-devtools-cli
```

When a project keeps needing one, ask the user, then install it into the
project:

```sh
bunx skills add ChromeDevTools/chrome-devtools-mcp --skill <name>
```

Upstream skills are written for the MCP server and for a global `npm` install.
Their tool names match the CLI commands, so read their tool calls as
`bunx chrome-devtools <tool>` and ignore their install steps.
