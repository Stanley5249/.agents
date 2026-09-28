/** End-to-end check that the daemon drives the intended browser. */
import { DevToolsClient } from "./devtools-client.ts";

const c = new DevToolsClient();
const id = await c.newPage("https://example.com/");
console.log(
  await c.evaluate(
    id,
    "() => ({ title: document.title, ua: navigator.userAgent })",
  ),
);
await c.closePage(id);
process.exit(0);
