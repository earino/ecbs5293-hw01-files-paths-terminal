"""Pack this project for Moodle as hw1-submission.zip, written NEXT TO the project folder.

Run it from the project folder (the one containing pyproject.toml):

    uv run python make_submission.py

The zip lands one level up, so `git status` inside the project stays clean.
Environments, caches, and generated output are left out: the grader rebuilds
them from your run instructions, exactly as a classmate would.

Optional: give it a path and the zip goes there instead:

    uv run python make_submission.py ../somewhere/hw1-submission.zip
"""

import fnmatch
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent   # the project folder, whatever your terminal's cwd is
ZIP_NAME = "hw1-submission.zip"
SKIP_NAMES = {".venv", "venv", ".git", "output", "__pycache__",
              ".ipynb_checkpoints", ".pytest_cache", ".DS_Store"}
SKIP_GLOBS = ("*.pyc", "*.zip")


def skip(name: str) -> bool:
    return name in SKIP_NAMES or any(fnmatch.fnmatch(name, g) for g in SKIP_GLOBS)


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ZIP_NAME
    if out.is_dir():
        out = out / ZIP_NAME
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if not (ROOT / "output" / "report.csv").is_file():
        print("warning: output/report.csv not found - run the export first; the grader regenerates "
              "output/ from your instructions, but check that yours does too")
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = sorted(d for d in dirnames if not skip(d))
            for name in sorted(filenames):
                if skip(name):
                    continue
                path = Path(dirpath) / name
                zf.write(path, path.relative_to(ROOT).as_posix())
                count += 1
    print(f"wrote {out} ({count} files)")


if __name__ == "__main__":
    main()
