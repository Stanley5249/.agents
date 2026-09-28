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
  pageId: number;
  title: string;
  url: string;
  /** The daemon's own selection, not the tab the user is looking at. */
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
  "No chrome-devtools-mcp daemon. Start one with `bunx chrome-devtools start` " +
  "as in the browser skill.";

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

// A promise settles once, so the handlers that fire after it are no-ops.
function sendDaemonCommand(command: unknown): Promise<DaemonResponse> {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection({ path: getSocketPath() });
    let buf = Buffer.alloc(0);
    socket.setTimeout(COMMAND_TIMEOUT_MS, () =>
      socket.destroy(new Error("Timed out waiting for the daemon response.")),
    );
    socket.on("data", (chunk: Buffer) => {
      buf = Buffer.concat([buf, chunk]);
      const idx = buf.indexOf(0);
      if (idx === -1) return;
      socket.end();
      try {
        resolve(JSON.parse(buf.subarray(0, idx).toString("utf-8")));
      } catch (err) {
        reject(err);
      }
    });
    socket.on("error", (err: NodeJS.ErrnoException) =>
      reject(err.code === "ENOENT" ? new Error(NO_DAEMON) : err),
    );
    socket.on("close", () =>
      reject(new Error("The daemon closed the connection with no response.")),
    );
    socket.write(JSON.stringify(command) + "\0");
  });
}

function toPageInfo(p: any): PageInfo {
  return {
    pageId: p.id,
    title: p.title,
    url: p.url,
    selected: Boolean(p.selected),
  };
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
      throw new Error(`${tool} failed: ${response.error}`);
    }
    const result = JSON.parse(response.result!);
    // isError means the browser was unreachable.
    if (result.isError) {
      throw new Error(`${tool}: ${result.content?.[0]?.text ?? "failed"}`);
    }
    return result;
  }

  async getPages(): Promise<PageInfo[]> {
    const result = await this.callTool("list_pages");
    return (result.structuredContent?.pages ?? []).map(toPageInfo);
  }

  /**
   * Opens `url` in a new tab and returns its pageId. Close what you open.
   *
   * The new tab always comes to the front. Pass `returnTo`, a tab the user
   * named, to bring that tab back. Later calls against the returned id leave
   * it in front.
   */
  async newPage(url: string, returnTo?: number): Promise<number> {
    // new_page selects the page it opened and answers with the page list.
    const result = await this.callTool("new_page", { url });
    const opened = (result.structuredContent?.pages ?? []).find(
      (p: any) => p.selected,
    );
    if (!opened) throw new Error(`new_page did not report a page for ${url}`);
    if (returnTo !== undefined) await this.selectPage(returnTo);
    return opened.id;
  }

  /** Brings `pageId` to the front, making it the tab the user sees. */
  async selectPage(pageId: number): Promise<void> {
    await this.callTool("select_page", { pageId, bringToFront: true });
  }

  async closePage(pageId: number): Promise<void> {
    await this.callTool("close_page", { pageId });
  }

  async navigate(pageId: number, url: string): Promise<void> {
    await this.callTool("navigate_page", { pageId, url });
  }

  /**
   * Runs a function source (`() => ...` or `async () => ...`) in the page and
   * returns its JSON result, or `undefined` when it returns nothing. Throws if
   * the script threw, including `Execution context was destroyed`, which is
   * what a click that navigates looks like, so catch it where a navigation is
   * expected.
   */
  async evaluate<T = any>(pageId: number, fn: string): Promise<T | undefined> {
    const result = await this.callTool("evaluate_script", {
      pageId,
      function: fn,
    });
    // evaluate_script returns its value as fenced JSON inside a prose message.
    const message: string = result.structuredContent?.message ?? "";
    const match = message.match(/```json\s*([\s\S]*?)```/);
    if (!match)
      throw new Error(`Unexpected evaluate_script response: ${message}`);
    const json = match[1].trim();
    return json === "undefined" ? undefined : JSON.parse(json);
  }
}
