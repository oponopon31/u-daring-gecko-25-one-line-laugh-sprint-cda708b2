#!/usr/bin/env python3
"""One-Line Laugh Sprint entry.

The competition asks for a single funny line about ordinary life, at
most 200 characters, and this program is the whole entry: it carries
the line, checks it against the rules, and drops it into entry.txt
for the judge to read. Nothing is fetched, nothing is random, and the
same input always produces the same file.

The line itself: a houseplant is the smallest possible responsibility
and still too much for the narrator, so the dead plant's empty pot
becomes a performance review — the driest, most corporate verdict
imaginable, delivered by an object on a windowsill that cannot talk.
"""

import hashlib
import os
from pathlib import Path

LINE = (
    "My houseplant died in a week, and now the empty pot sits on the "
    "sill like a tiny, silent performance review of my entire adult life."
)
MAX_CHARS = 200
OUTPUT_NAME = "entry.txt"


def check_line(line: str) -> int:
    """Make sure the line obeys the competition's limits; return its length."""
    chars = len(line)
    if not 1 <= chars <= MAX_CHARS:
        raise ValueError(f"line is {chars} characters, allowed 1-{MAX_CHARS}")
    if line != line.strip():
        raise ValueError("line starts or ends with blank space")
    if "\n" in line or "\t" in line:
        raise ValueError("line must be one plain line, no newline or tab")
    if "  " in line:
        raise ValueError("line contains a double space")
    if not line.endswith("."):
        raise ValueError("line must end with a full stop")
    if line.count(".") != 1:
        raise ValueError("line must be a single sentence")
    return chars


def publish(line: str, folder: str) -> tuple[Path, str]:
    """Save the line as entry.txt inside folder and prove the bytes match."""
    target = Path(folder) / OUTPUT_NAME
    encoded = line.encode("utf-8")
    encoded.decode("utf-8")
    target.write_bytes(encoded)
    back = target.read_bytes()
    if back != encoded:
        raise ValueError("entry.txt on disk differs from the line")
    digest = hashlib.sha256(encoded).hexdigest()
    if hashlib.sha256(back).hexdigest() != digest:
        raise ValueError("entry.txt checksum does not match")
    return target, digest


def pick_folder() -> str:
    """Where entry.txt goes: the harness folder, or the current directory."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return folder if Path(folder).is_dir() else "."


def main() -> None:
    chars = check_line(LINE)
    words = len(LINE.split())
    target, digest = publish(LINE, pick_folder())
    print(f"characters: {chars} (limit {MAX_CHARS})")
    print(f"words: {words}")
    print(f"sha256: {digest}")
    print(f"wrote: {target}")
    print("verified: entry.txt holds exactly the line above")


if __name__ == "__main__":
    main()
