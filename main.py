#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261118.

The entry image is poster.png, a one-page newspaper front page that sums
up the world news of Wednesday 18 November 2026 (rendered at build time
by build_poster.py; the grading sandbox is standard-library only, so the
program itself only has to place the image where the grader reads it).

It copies poster.png, which sits beside this file, to
$MAKEFUN_OUTPUT_DIR/entry.png -- or to /output/entry.png when the
variable is not set, which is the grader's container layout. The copy is
byte for byte, so two runs always write the same bytes.
"""

import os
import struct
from pathlib import Path

POSTER_NAME = "poster.png"
ENTRY_NAME = "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # the gate's 1 MiB cap
MAX_SIDE = 1024        # the gate's pixel cap


def poster_path() -> Path:
    """The poster file that ships in the repository beside this program."""
    return Path(__file__).resolve().parent / POSTER_NAME


def output_dir() -> Path:
    """Where the grader reads the entry image from."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def check_poster(data: bytes) -> None:
    """Fail loudly rather than hand the grader an image its gate refuses.

    Reads only the PNG signature and the IHDR width/height, which is all
    the gate's size rules need; the image bytes themselves pass through
    untouched.
    """
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("poster.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"poster is {width}x{height}, over the {MAX_SIDE}px cap")
    if len(data) > MAX_BYTES:
        raise ValueError(f"poster is {len(data)} bytes, over the {MAX_BYTES} cap")


def main() -> None:
    data = poster_path().read_bytes()
    check_poster(data)
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / ENTRY_NAME).write_bytes(data)


if __name__ == "__main__":
    main()
