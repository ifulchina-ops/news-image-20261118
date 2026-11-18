#!/usr/bin/env python3
"""Eighteen — 18 November 2026 in one front page.

Copies the pre-drawn broadsheet (entry.png, produced by build_art.py)
to the grader's output path and verifies the result before finishing.
Runs with no network; the image bytes are identical on every run.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "6076f11d53e81b5c1a639bdce1f7dba416e8916b5ffa58b985d6fae643a1a037"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    data = open(dst, "rb").read()
    if len(data) > 1_048_576:
        print(f"entry.png too large: {len(data)} bytes", file=sys.stderr)
        return 1
    if EXPECTED_SHA256 != "PLACEHOLDER":
        got = hashlib.sha256(data).hexdigest()
        if got != EXPECTED_SHA256:
            print(f"sha mismatch: {got} != {EXPECTED_SHA256}", file=sys.stderr)
            return 1
    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
