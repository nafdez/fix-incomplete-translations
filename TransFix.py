import os
import sys
from pathlib import Path

def sync_files():
    print("syncing...")

def sync_folders(src: Path, dest: Path):
    print("syncing...")

def error(msg: str):
    print(msg, file=sys.stderr)
    sys.exit()

def main(args: list[str]):
    if len(args) <= 2:
        error("Not enough arguments: provide source language and target language")

    src = Path(args[1])
    dest = Path(args[2])

    if not src.exists():
        error(f"Source language '" + args[1] + "' does not exist.")
    
    sync_folders(src, dest)


if __name__ == "__main__":
    main(sys.argv)