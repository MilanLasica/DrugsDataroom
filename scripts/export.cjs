/*
 Cross-platform export script for Next.js static site.
 - Builds (if needed) with output: export (configured in next.config.js)
 - Copies from ./out to DEST_DIR (default ../elysia/api/static)
 - If the destination parent directory doesn't exist, falls back to ./export
*/

const fs = require('fs');
const fsp = require('fs/promises');
const path = require('path');
const { execSync } = require('child_process');

async function pathExists(p) {
  try {
    await fsp.access(p, fs.constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function ensureDir(p) {
  await fsp.mkdir(p, { recursive: true });
}

async function rmrf(p) {
  await fsp.rm(p, { recursive: true, force: true });
}

async function main() {
  const ROOT = process.cwd();
  const sourceDir = path.resolve(ROOT, 'out');
  const defaultDest = path.resolve(ROOT, '..', 'elysia', 'api', 'static');
  const destDir = process.env.DEST_DIR ? path.resolve(ROOT, process.env.DEST_DIR) : defaultDest;

  console.log('Clearing .next cache...');
  await rmrf(path.resolve(ROOT, '.next'));

  if (!(await pathExists(sourceDir))) {
    console.log("'out' directory not found. Running build to generate static export...");
    try {
      execSync('npx --yes next build', {
        stdio: 'inherit',
        env: { ...process.env, NEXT_PUBLIC_IS_STATIC: 'true' },
      });
    } catch (err) {
      console.error('Build failed:', err?.message || err);
      process.exit(1);
    }
  }

  if (!(await pathExists(sourceDir))) {
    console.error("Error: 'out' directory still not found after build. Check Next.js config (output: 'export').");
    process.exit(1);
  }

  const parentOfDest = path.dirname(destDir);
  let finalDest = destDir;
  if (!(await pathExists(parentOfDest))) {
    console.warn(`Destination parent directory not found: ${parentOfDest}`);
    finalDest = path.resolve(ROOT, 'export');
    console.warn(`Falling back to local export directory: ${finalDest}`);
  }

  console.log(`Writing export to: ${finalDest}`);
  await rmrf(finalDest);
  await ensureDir(finalDest);

  // Node 16.7+ supports fs.cp
  if (typeof fs.cp === 'function') {
    await fs.promises.cp(sourceDir, finalDest, { recursive: true });
  } else {
    // Fallback: copy via platform-agnostic method (simple readdir recursion)
    async function copyRecursive(src, dest) {
      const entries = await fsp.readdir(src, { withFileTypes: true });
      await ensureDir(dest);
      for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
          await copyRecursive(srcPath, destPath);
        } else if (entry.isSymbolicLink()) {
          const link = await fsp.readlink(srcPath);
          await fsp.symlink(link, destPath);
        } else {
          await fsp.copyFile(srcPath, destPath);
        }
      }
    }
    await copyRecursive(sourceDir, finalDest);
  }

  console.log('Export completed successfully.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
