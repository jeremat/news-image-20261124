"""Entry for 24 November 2026: one front-page image of the day's news.

The finished page is drawn by draw_news.py and stored beside this file as
entry.png. This program only moves that exact file to the place the grader
reads it from. It uses nothing but the standard library, touches no network,
and writes the same bytes on every run because the source file is fixed.
"""

import os
import shutil
from pathlib import Path

IMAGE_NAME = "entry.png"


def source_image():
    return Path(__file__).resolve().parent / IMAGE_NAME


def output_directory():
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    folder = Path(wanted)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def main():
    source = source_image()
    if not source.is_file():
        raise FileNotFoundError(f"entry image is missing: {source}")
    target = output_directory() / IMAGE_NAME
    shutil.copyfile(source, target)
    return target


if __name__ == "__main__":
    main()
