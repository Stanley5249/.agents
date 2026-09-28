/**
 * Client for an already-running chrome-devtools-mcp daemon, over the same
 * local socket the `chrome-devtools` CLI uses. It reuses the daemon's single
 * approved browser connection, so it never re-prompts for remote debugging,
 * and it skips the CLI's per-call startup.
 *
 * See ../reference/daemon-socket.md for the protocol.
 */
import net from "node:net";
import os from "node:os";
import path from "node:path";

export interface PageInfo {
  pageId: string;
  title: string;
  url: string;
  /** True for the tab the user is looking at. */
  selected: boolean;
}

interface DaemonResponse {
  success: boolean;
  result?: string;
  error?: string;
}

// The CLI gives up at 60s. A script can wait out a slow first attach instead
// of re-sending a command the daemon is still running.
const COMMAND_TIMEOUT_MS = 300_000;

const NO_DAEMON =
  "No chrome-devtools-mcp daemon. Start one against the intended browser " +
  "first, as in the browser skill's Quick start. Starting it from here would " +
  "have to guess a --userDataDir, and a wrong guess attaches to the wrong " +
  "browser.";

function getSocketPath(): string {
  const { username, uid } = os.userInfo();
  if (process.platform === "win32") {
    return `\\\\.\\pipe\\chrome-devtools-mcp-${username}\\server.sock`;
  }
  const runtimeDir = process.env.XDG_RUNTIME_DIR;
  return runtimeDir
    ? path.join(runtimeDir, "chrome-devtools-mcp", "server.sock")
    : `/tmp/chrome-devtools-mcp-${uid}.sock`;
}

function sendDaemonCommand(command: unknown): Promise<DaemonResponse> {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection({ path: getSocketPath() });
    let buf = Buffer.alloc(0);
    const timer = setTimeout(() => {
      socket.destroy();
      reject(
        new Error("Timed out waiting for chrome-devtools-mcp daemon response."),
      );
    }, COMMAND_TIMEOUT_MS);

    socket.on("data", (chunk) => {
      buf = Buffer.concat([buf, chunk]);
      const idx = buf.indexOf(0);
      if (idx !== -1) {
        clearTimeout(timer);
        resolve(JSON.parse(buf.subarray(0, idx).toString("utf-8")));
        socket.end();
      }
    });
    socket.on("error", (err: NodeJS.ErrnoException) => {
      clearTimeout(timer);
      reject(
        err.code === "ENOENT"
          ? new Error(NO_DAEMON)
          : new Error(
              `Cannot reach chrome-devtools-mcp daemon: ${err.message}`,
            ),
      );
    });
    socket.on("close", () => {
      clearTimeout(timer);
      reject(
        new Error(
          "chrome-devtools-mcp daemon closed the connection with no response.",
        ),
      );
    });
    socket.write(JSON.stringify(command) + "\0");
  });
}

export class DevToolsClient {
  /**
   * Invokes any tool by its CLI name, with argument names matching its CLI
   * flags. Returns the raw MCP CallToolResult (`{ content, structuredContent }`).
   */
  async callTool<T = any>(
    tool: string,
    args: Record<string, unknown> = {},
  ): Promise<T> {
    const response = await sendDaemonCommand({
      method: "invoke_tool",
      tool,
      args,
    });
    if (!response.success) {
      throw new Error(
        `chrome-devtools-mcp tool '${tool}' failed: ${response.error}`,
      );
    }
    const result = JSON.parse(response.result!);
    // A tool that could not reach the browser answers with isError and prose.
    // Without this check, the caller reads an empty payload as an empty browser.
    if (result.isError) {
      throw new Error(`${tool}: ${result.content?.[0]?.text ?? "failed"}`);
    }
    return result;
  }

  async getPages(): Promise<PageInfo[]> {
    const result = await this.callTool("list_pages");
    const pages = result.structuredContent?.pages ?? [];
    return pages.map((p: any) => ({
      pageId: String(p.id),
      title: p.title,
      url: p.url,
      selected: Boolean(p.selected),
    }));
  }

  async findPage(match: (p: PageInfo) => boolean): Promise<PageInfo | null> {
    return (await this.getPages()).find(match) ?? null;
  }

  /**
   * Opens `url` in a new tab and returns its pageId. Close what you open.
   *
   * The new tab always steals focus, so this hands the user's tab back.
   * Later calls against the returned id leave the user's selection alone.
   */
  async newPage(url: string): Promise<string> {
    const before = (await this.getPages()).find((p) => p.selected);
    // new_page answers with the whole page list, not the id it just created.
    await this.callTool("new_page", { url });
    const opened = (await this.getPages())
      .filter((p) => p.url.startsWith(url))
      .at(-1);
    if (!opened) throw new Error(`no browser page found for ${url}`);
    if (before && before.pageId !== opened.pageId)
      await this.selectPage(before.pageId);
    return opened.pageId;
  }

  /** Brings `pageId` to the front, making it the tab the user sees. */
  async selectPage(pageId: string): Promise<void> {
    await this.callTool("select_page", {
      pageId: Number(pageId),
      bringToFront: true,
    });
  }

  async closePage(pageId: string): Promise<void> {
    await this.callTool("close_page", { pageId: Number(pageId) });
  }

  async navigate(pageId: string, url: string): Promise<void> {
    await this.callTool("navigate_page", { pageId: Number(pageId), url });
  }

  /**
   * Runs a function source (`() => ...` or `async () => ...`) in the page and
   * returns its JSON result. Throws if the script threw, including
   * `Execution context was destroyed`, which is what a click that navigates
   * looks like, so catch it where a navigation is expected.
   */
  async evaluate<T = any>(pageId: string, fn: string): Promise<T> {
    const result = await this.callTool("evaluate_script", {
      pageId: Number(pageId),
      function: fn,
    });
    // evaluate_script returns its value as fenced JSON inside a prose message.
    const message: string = result.structuredContent?.message ?? "";
    const match = message.match(/```json\s*([\s\S]*?)```/);
    if (!match)
      throw new Error(`Unexpected evaluate_script response: ${message}`);
    return JSON.parse(match[1]);
  }
}
