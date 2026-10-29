import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

// Agent Skills limits shared by Claude Code, Codex, and Pi.
const NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const MAX_NAME = 64;
const MAX_DESCRIPTION = 1024;

function frontmatter(text: string): Map<string, string> | undefined {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(text);
  if (!match) return undefined;
  const fields = new Map<string, string>();
  for (const line of match[1].split(/\r?\n/)) {
    const field = /^([\w-]+):\s*(.*)$/.exec(line);
    if (field) fields.set(field[1], field[2].replace(/^(["'])(.*)\1$/, "$2"));
  }
  return fields;
}

function validateSkill(dir: string, name: string): string[] {
  const path = join(dir, "SKILL.md");
  if (!existsSync(path)) return [`${name}: missing SKILL.md`];
  const text = readFileSync(path, "utf8");
  const fields = frontmatter(text);
  if (!fields) return [`${name}: missing frontmatter`];

  const errors: string[] = [];
  if (fields.get("name") !== name) {
    errors.push(`${name}: name must match the directory`);
  }
  if (!NAME.test(name) || name.length > MAX_NAME) {
    errors.push(`${name}: name must be lowercase words joined by hyphens`);
  }
  const description = fields.get("description") ?? "";
  if (!description) errors.push(`${name}: missing description`);
  if (description.length > MAX_DESCRIPTION) {
    errors.push(`${name}: description is over ${MAX_DESCRIPTION} characters`);
  }

  const manual = fields.get("disable-model-invocation") === "true";
  const yaml = join(dir, "agents", "openai.yaml");
  const codexManual =
    existsSync(yaml) &&
    /allow_implicit_invocation:\s*false/.test(readFileSync(yaml, "utf8"));
  if (manual !== codexManual) {
    errors.push(
      `${name}: disable-model-invocation and agents/openai.yaml disagree`,
    );
  }

  for (const [reference] of text.matchAll(/references\/[\w.-]+\.md/g)) {
    if (!existsSync(join(dir, reference))) {
      errors.push(`${name}: missing ${reference}`);
    }
  }
  return errors;
}

function markdownFiles(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name.startsWith(".") || entry.name === "node_modules") return [];
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return markdownFiles(path);
    return entry.name.endsWith(".md") ? [path] : [];
  });
}

function validateLinks(root: string): string[] {
  const errors: string[] = [];
  for (const file of markdownFiles(root)) {
    const text = readFileSync(file, "utf8");
    for (const [, target] of text.matchAll(/\]\(([^)\s#]+)(?:#[^)]*)?\)/g)) {
      if (/^[a-z]+:/i.test(target)) continue;
      if (!existsSync(resolve(dirname(file), target))) {
        errors.push(`${file.slice(root.length + 1)}: broken link ${target}`);
      }
    }
  }
  return errors;
}

export function validate(root: string): string[] {
  const skills = join(root, "skills");
  const names = readdirSync(skills, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);
  return [
    ...names.flatMap((name) => validateSkill(join(skills, name), name)),
    ...validateLinks(root),
  ];
}

if (import.meta.main) {
  const errors = validate(resolve(import.meta.dir, ".."));
  for (const error of errors) console.error(error);
  if (errors.length > 0) process.exit(1);
}
