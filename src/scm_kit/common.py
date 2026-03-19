import shutil
import subprocess
import sys

PRETTIER_EXTS = ("html", "md", "yaml", "yml")
PRETTIER_GLOB = "**/*.{" + ",".join(PRETTIER_EXTS) + "}"


def run(cmd: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=capture, text=capture)


def try_run(cmd: list[str]) -> bool:
    """Run a command, returning True on success or False on failure."""
    try:
        run(cmd)
        return True
    except subprocess.CalledProcessError:
        return False


def maybe_run(cmd: list[str]) -> None:
    """Run a command if the executable is on PATH, otherwise skip silently."""
    if not shutil.which(cmd[0]):
        return
    run(cmd)


def check_for_required_tools() -> None:
    """Check that required tools are available, exit if not."""
    missing = []
    if not shutil.which("npx"):
        missing.append("npx")
    if not shutil.which("uvx"):
        missing.append("uvx")
    if missing:
        print(f"Error: Required tools not found: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)


def has_files(*exts: str) -> bool:
    """Check if any files with the given extensions exist in the repo.

    Includes tracked-but-deleted files, which is fine since this only gates
    whether to invoke a tool against '.' — the tool scans the filesystem itself
    and will no-op if the files are actually gone.
    """
    for ext in exts:
        if run(["git", "ls-files", "-c", "-o", "--exclude-standard", f"*.{ext}"], capture=True).stdout.strip():
            return True
    return False


def get_files_by_ext(ext: str, all_files: bool) -> set[str]:
    """Return file paths with the given extension.

    If all_files is True, returns all non-deleted files in the repo. Otherwise,
    returns only files changed vs HEAD plus untracked files.
    """

    def _git(cmd: list[str]) -> set[str]:
        stdout = run(["git"] + cmd, capture=True).stdout.strip()
        return set(stdout.splitlines()) if stdout else set()

    if all_files:
        # All non-deleted files.
        files = _git(["ls-files", "-c", "-o", "--exclude-standard", f"*.{ext}"])
        deleted = _git(["ls-files", "-d"])
        return files - deleted
    else:
        # New or modified files relative to current branch, and untracked files.
        changed = _git(["diff", "--name-only", "--diff-filter=d", "HEAD"])
        changed = {x for x in changed if x.endswith(f".{ext}")}
        untracked = _git(["ls-files", "-o", "--exclude-standard", f"*.{ext}"])
        return changed | untracked
