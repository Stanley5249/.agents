import { afterEach, beforeEach, expect, test } from "bun:test";
import {
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { cleanSkillLinks } from "./clean-skill-links";

let root: string;
let skills: string;

beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), "skill-links-"));
  skills = join(root, "skills");
  mkdirSync(skills);
  mkdirSync(join(root, "healthy-target"));
  mkdirSync(join(root, "deleted-target"));
  symlinkSync(
    join(root, "healthy-target"),
    join(skills, "healthy"),
    "junction",
  );
  symlinkSync(join(root, "deleted-target"), join(skills, "broken"), "junction");
  rmSync(join(root, "deleted-target"), { recursive: true });
  mkdirSync(join(skills, "ordinary"));
  symlinkSync(
    join(root, "missing"),
    join(skills, "ordinary", "nested"),
    "junction",
  );
  writeFileSync(join(skills, "file"), "keep");
});

afterEach(() => rmSync(root, { recursive: true, force: true }));

test("dry run reports broken links without deleting them", () => {
  expect(cleanSkillLinks(skills, true)).toEqual(["broken"]);
  expect(lstatSync(join(skills, "broken")).isSymbolicLink()).toBe(true);
});

test("cleanup preserves healthy links, ordinary entries, and nested links", () => {
  expect(cleanSkillLinks(skills)).toEqual(["broken"]);
  expect(() => lstatSync(join(skills, "broken"))).toThrow();
  expect(existsSync(join(root, "healthy-target"))).toBe(true);
  expect(lstatSync(join(skills, "healthy")).isSymbolicLink()).toBe(true);
  expect(lstatSync(join(skills, "ordinary")).isDirectory()).toBe(true);
  expect(lstatSync(join(skills, "ordinary", "nested")).isSymbolicLink()).toBe(
    true,
  );
  expect(existsSync(join(skills, "file"))).toBe(true);
  expect(cleanSkillLinks(skills)).toEqual([]);
});

test("CLI previews by default and requires --apply to delete", () => {
  const run = (...args: string[]) =>
    Bun.spawnSync(
      [
        process.execPath,
        join(import.meta.dir, "clean-skill-links.ts"),
        ...args,
      ],
      { env: { ...process.env, CLAUDE_CONFIG_DIR: root } },
    );

  const preview = run();
  expect(preview.exitCode).toBe(0);
  expect(preview.stdout.toString()).toContain("Would remove: broken");
  expect(lstatSync(join(skills, "broken")).isSymbolicLink()).toBe(true);

  const apply = run("--apply");
  expect(apply.exitCode).toBe(0);
  expect(apply.stdout.toString()).toContain("Removed: broken");
  expect(() => lstatSync(join(skills, "broken"))).toThrow();
});

test("an absent skills directory has no broken links", () => {
  expect(cleanSkillLinks(join(root, "absent"))).toEqual([]);
});
