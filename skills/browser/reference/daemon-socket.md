# The daemon's control socket

The `chrome-devtools` CLI is a thin client. Every command opens a local socket
to the running daemon, sends one request, reads one response, and exits. The
daemon holds the real, already-approved CDP connection, and the CLI process
never touches the browser.

The socket protocol is not documented or versioned, but it is simple and stable
within a `chrome-devtools-mcp` release.

The daemon must already be running, as shown by `bunx chrome-devtools status`.
The bundled client does not start one, because starting a daemon means choosing
a `--userDataDir`, and a wrong guess silently attaches to the wrong browser.

## Protocol

- **Socket path:** `\\.\pipe\chrome-devtools-mcp-<username>\server.sock` on
  Windows. On POSIX, `$XDG_RUNTIME_DIR/chrome-devtools-mcp/server.sock`, or
  `/tmp/chrome-devtools-mcp-<uid>.sock` when that variable is unset. A daemon
  started with `--sessionId <id>` appends `-<id>` to `chrome-devtools-mcp`; the
  bundled client supports only the default session.
- **Framing:** write `JSON.stringify(message) + "\0"`. Messages are
  NUL-terminated, not newline-terminated.
- **Request:** `{ method: "invoke_tool", tool: "<name>", args: {...} }`. `tool`
  and `args` match the CLI's tool names and flag names exactly, such as
  `evaluate_script` with `{ pageId, function }`.
- **Response:** `{ success: boolean, result?: string, error?: string }`.
  `result` is a JSON string of the MCP `CallToolResult`, so parse it again to
  get `{ content, structuredContent?, isError? }`.

Prefer `structuredContent` over scraping `content[0].text`. Some tools still
wrap their payload in prose. `evaluate_script`, for example, puts its value in a
fenced JSON block inside `structuredContent.message`. Check each tool's shape
once with `--output-format=json` before relying on it in a script.

A tool that could not reach the browser answers with `isError: true` and prose
in `content`. Treat that as a failure, or an empty payload reads as an empty
browser.

## When this breaks

This depends on the daemon's internals, not the CLI's public surface. If a
release changes the protocol, socket scripts fail while the CLI keeps working,
because both ship in the same package. The fallback is to replace the socket
call with `bunx chrome-devtools <tool> ... --output-format=json` and parse
stdout. It is slower but depends only on the documented interface.
