# Why a chrome-devtools command fails

## The two timeouts

They look alike and are told apart by how long they take.

`Network.enable timed out` returning in about a second means the daemon's attach
to some target is wedged. `stop`, then `start` again.

`Timeout waiting for daemon response` returning at exactly 60 seconds is the
CLI's own hardcoded give-up, not a failed connect. The daemon is still working,
so do not `stop` between retries, because that discards the attach in progress.
The cause is almost always too many open targets, counting tabs, workers, and
iframes, because upstream assumes 2 to 10 pages and attaches to all of them
without a cap
([#1921](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1921)).
Once attached, the daemon stays warm and later calls return in seconds.

Each new connection re-prompts the user for remote debugging
([#1794](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/1794)),
which is why one daemon should serve the whole task.

## 403 on connect

`Could not connect to Chrome ... Unexpected server response: 403` means the
browser is closed. `--autoConnect` attaches to a running browser, it never
launches one.

## Only about:blank in list_pages

The CLI launched its own browser instead of attaching. Remote debugging writes
`DevToolsActivePort` into the user-data root, so if that file is missing, have
the user turn on the toggle at `chrome://inspect/#remote-debugging` or
`edge://inspect/#remote-debugging`, then retry. Do not use a copy of the profile
unless asked, because it will not have later logins.

## Other causes worth ruling out

**A duplicate daemon.** An interrupted `start` or `stop` can orphan one, and the
next `start` adds a second on the same socket. Symptoms are identical commands
taking different times, or a flag being ignored. Kill every match, then start
once. On Windows:

```powershell
Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
  Where-Object { $_.CommandLine -like '*chrome-devtools*' } |
  Select-Object ProcessId,CommandLine
```

**`--headless` defaults to true.** A previous `start` carries nothing forward,
so pass `--no-headless` explicitly when a launched browser must be visible. It
is harmless on an `--autoConnect` daemon, which drives the window that is
already open.

**Two profiles, one user-data root.** Chromium's lock covers the whole
`User Data` root, so `list_pages` sees the targets of every open profile, and a
second launch fails with "already running ... Use --isolated". To scope to one
profile, close the other profile's windows, check that no `SingletonLock`
remains, then `start` without `--autoConnect` and with
`--chromeArg="--profile-directory=Profile 2"`.

## A new tab jumps to the front

`new_page` always makes the new tab the selected one, which pulls the user away
from what they were reading. Measured against `chrome-devtools-mcp` 1.9.0 on an
`--autoConnect` daemon:

| Attempt                              | Selected tab afterwards                                      |
| ------------------------------------ | ------------------------------------------------------------ |
| `new_page --background true`         | the new tab, the flag has no effect                          |
| `new_page --isolatedContext probe`   | the new tab, and cookies are isolated so the session is gone |
| `window.open` from `evaluate_script` | nothing opens, the popup blocker returns null                |

What works is handing focus back once with `select_page --bringToFront` after
opening. Later calls against that tab, including `navigate_page`,
`evaluate_script`, `take_snapshot`, and `close_page`, leave the user's selection
where it is.

`document.visibilityState` and `document.hasFocus()` are useless as probes here,
because every page reports visible and focused. The `selected` field from
`list_pages` is the only reliable signal.
