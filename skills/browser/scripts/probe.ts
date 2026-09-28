/**
 * End-to-end check that the socket client can open, read, and close a page.
 * It does not prove the daemon attached to the user's browser. Check the
 * `args` line of `bunx chrome-devtools status` for that.
 */
import { DevToolsClient } from "./devtools-client.ts";

const c = new DevToolsClient();
const id = await c.newPage("https://example.com/");
try {
  console.log(await c.evaluate(id, "() => document.title"));
} finally {
  await c.closePage(id);
}
process.exit(0);
