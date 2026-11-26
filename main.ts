// Copy the bundled news poster to the grader's output directory.
// Node 22+, standard library only, no network access required.
import { copyFileSync, chmodSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(outputDir, "entry.png");

if (!statSync(source).isFile()) {
  throw new Error("entry.png is missing next to main.ts");
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);
chmodSync(target, 0o644);

// The gate rejects anything over 1 MiB; fail loudly instead of shipping it.
const bytes = statSync(target).size;
if (bytes === 0 || bytes > 1024 * 1024) {
  throw new Error(`entry.png has an invalid size: ${bytes} bytes`);
}

console.log(`wrote ${target} (${bytes} bytes)`);
