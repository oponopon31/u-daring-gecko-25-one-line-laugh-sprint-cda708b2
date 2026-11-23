#!/usr/bin/env python3
"""Entry for make.fun competition
u-daring-gecko-25-one-line-laugh-sprint-cda708b2.

Writes a single funny line (at most 200 Unicode code points) about
everyday life to entry.txt in the output directory. Pure standard
library, deterministic, no network.

Why this line: a dead houseplant is the most ordinary small failure
there is, and the joke turns the empty pot into something every adult
recognises — a performance review that never ends, delivered in total
silence, by an object that cannot even speak. The escalation from one
dead plant to "my entire adult life" is the punchline, and it lands in
one breath with nothing left to explain.
"""

import hashlib
import os

TEXT = (
    "My houseplant died in a week, and now the empty pot sits on the "
    "sill like a tiny, silent performance review of my entire adult life."
)

FILENAME = "entry.txt"


def write_entry(text: str, out_dir: str) -> tuple[str, str]:
    """Write text to entry.txt under out_dir and verify the bytes.

    Returns (path, sha256 hex digest) of the file as written.
    """
    data = text.encode("utf-8")
    data.decode("utf-8")  # reject anything that is not clean UTF-8

    path = os.path.join(out_dir, FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    with open(path, "rb") as handle:
        written = handle.read()
    digest = hashlib.sha256(data).hexdigest()
    assert written == data, "entry.txt bytes differ from the intended line"
    assert hashlib.sha256(written).hexdigest() == digest, "sha256 mismatch"
    return path, digest


def main() -> None:
    text = TEXT
    count = len(text)
    assert 1 <= count <= 200, f"line is {count} chars, limit is 200"
    assert text.strip(), "line must not be blank"
    # One line only: no newline, and a single sentence ending in a stop.
    assert "\n" not in text, "entry must be a single line"
    assert text == text.strip(), "line must not start or end with space"
    assert "  " not in text, "line must not contain a double space"
    assert text.endswith(".") and text.count(".") == 1, (
        "entry must be one sentence ending in a full stop"
    )

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isdir(out_dir):
        out_dir = "."
    path, digest = write_entry(text, out_dir)

    print(f"chars: {count}")
    print(f"sha256: {digest}")
    print(f"wrote: {path}")
    print("verified: entry.txt bytes match the line exactly")


if __name__ == "__main__":
    main()
