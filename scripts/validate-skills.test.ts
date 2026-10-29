import { afterEach, beforeEach, expect, test } from "bun:test";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { validate } from "./validate-skills";

let root: string;

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), "validate-skills-"));
});

afterEach(() => {
  rmSync(root, { recursive: true, force: true });
});

function skill(name: string, frontmatter: string, body = ""): string {
  const dir = join(root, "skills", name);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "SKILL.md"), `---\n${frontmatter}\n---\n${body}`);
  return dir;
}

function codexManual(dir: string): void {
  mkdirSync(join(dir, "agents"));
  writeFileSync(
    join(dir, "agents", "openai.yaml"),
    "policy:\n  allow_implicit_invocation: false\n",
  );
}

test("accepts implicit and consistent manual skills", () => {
  skill("implicit", "name: implicit\ndescription: Use when testing.");
  const manual = skill(
    "manual",
    "name: manual\ndescription: Manual.\ndisable-model-invocation: true",
  );
  codexManual(manual);
  expect(validate(root)).toEqual([]);
});

test("reports a manual setting missing for Codex", () => {
  skill(
    "manual",
    "name: manual\ndescription: Manual.\ndisable-model-invocation: true",
  );
  expect(validate(root)).toEqual([
    "manual: disable-model-invocation and agents/openai.yaml disagree",
  ]);
});

test("reports a name mismatch and a missing description", () => {
  skill("dir-name", "name: other");
  expect(validate(root)).toEqual([
    "dir-name: name must match the directory",
    "dir-name: missing description",
  ]);
});

test("reports missing references and broken links", () => {
  skill(
    "refs",
    "name: refs\ndescription: Refs.",
    "Read `references/gone.md` and [docs](../../missing.md).\n",
  );
  expect(validate(root)).toEqual([
    "refs: missing references/gone.md",
    `${join("skills", "refs", "SKILL.md")}: broken link ../../missing.md`,
  ]);
});
