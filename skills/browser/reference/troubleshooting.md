# Why a chrome-devtools command fails

## The two timeouts

They look alike and are told apart by how long they take.

`Network.enable timed out` returning in about a second means the daemon's attach
to some target is wedged. `stop`, then `start` again.

`Timeout waiting for daemon response` returning at exactly 60 seconds is the
CLI's own hardcoded give-up, not a failed connect. The daemon is still working,
so do not `stop` between retries, because that discards the attach in progress.
The cause is almost always too many open targets, counting tabs, workers, and
iframes, because upstream attaches to all of them without a cap. Once attached,
the daemon stays warm and later calls return in seconds.

## Could not connect to Chrome

`--autoConnect` attaches to a running browser through the `DevToolsActivePort`
file in the user-data root. It never launches one.

- **`Could not connect to Chrome in <dir>`** means that file is missing or
  unreadable. Either the browser is not running, or remote debugging is off.
  Have the user open the browser and turn on the toggle at
  `chrome://inspect/#remote-debugging` or `edge://inspect/#remote-debugging`,
  then `start` again.
- **An error from the connection itself**, such as a 403 or a refused
  connection, means the file points at a browser that is gone or that refused
  the request. Have the user reopen the browser and accept the remote debugging
  prompt, then `start` again.

Do not use a copy of the profile unless asked, because it will not have later
logins.

## Only about:blank in list_pages

The daemon is driving a browser it launched, not the user's. That happens when
it was started without `--autoConnect`, or when a tool command ran with no
daemon and started one by itself. Check the `args` line of `status`, then
`start` again with `--autoConnect` and the user-data root.

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

**Several profiles, one user-data root.** An attach covers the whole root, so
`list_pages` includes the tabs of every open profile. Pick pages by the id the
user gave or by the scratch tab you opened, not by position.

## Tabs and focus

`new_page` always brings the new tab to the front. `--isolatedContext` does not
change that, and it also isolates cookies, so the logged-in session is gone.

Nothing reports which tab the user is looking at. `document.visibilityState` and
`document.hasFocus()` report visible and focused on every page, and `selected`
in `list_pages` is only the page the daemon itself last selected, which starts
as the first page. Hand focus back only to a tab the user named.
