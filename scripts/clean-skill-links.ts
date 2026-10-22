import { lstatSync, readdirSync, statSync, unlinkSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

function isMissing(error: unknown): boolean {
  const code = (error as NodeJS.ErrnoException).code;
  return code === "ENOENT" || code === "ENOTDIR";
}

function isBrokenLink(path: string): boolean {
  try {
    if (!lstatSync(path).isSymbolicLink()) return false;
  } catch (error) {
    if (isMissing(error)) return false;
    throw error;
  }

  try {
    statSync(path);
    return false;
  } catch (error) {
    if (isMissing(error)) return true;
    throw error;
  }
}

export function cleanSkillLinks(directory: string, dryRun = false): string[] {
  let names: string[];
  try {
    names = readdirSync(directory);
  } catch (error) {
    if (isMissing(error)) return [];
    throw error;
  }

  const broken = names.filter((name) => isBrokenLink(join(directory, name)));
  if (!dryRun) {
    for (const name of broken) {
      const path = join(directory, name);
      if (isBrokenLink(path)) unlinkSync(path);
    }
  }
  return broken;
}

if (import.meta.main) {
  const args = process.argv.slice(2);
  if (args.some((arg) => arg !== "--apply")) {
    throw new Error("Usage: clean-skill-links.ts [--apply]");
  }
  const dryRun = !args.includes("--apply");
  const config = process.env.CLAUDE_CONFIG_DIR || join(homedir(), ".claude");
  const broken = cleanSkillLinks(join(config, "skills"), dryRun);
  for (const name of broken) {
    console.log(`${dryRun ? "Would remove" : "Removed"}: ${name}`);
  }
  if (broken.length === 0) console.log("No broken skill links.");
}
