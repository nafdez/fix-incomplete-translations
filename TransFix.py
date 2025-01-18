import os
import sys
from pathlib import Path

src_count = 0
copy_count = 0
updated_count = 0

def sync_file():
    print("file sync")

def sync_files(src: list[Path], src_lang: str, dst_lang: str):
    global src_count
    global copy_count
    for src_file in src:
        src_count += 1
        dst_file = Path(str(src_file).replace(src_lang, dst_lang))
        if not dst_file.exists():
            print(f"From: ", src_file, " to: ", dst_file)
            copy_count += 1


def sync_folders(src_lang: str, dst_lang: str):
    src = Path(src_lang)
    dst = Path(dst_lang)

    for root, dirs, files in src.walk():
        src_files = map(lambda x: Path(root, x), files)
        sync_files(src_files, src_lang, dst_lang)
        # dst_root = Path(str(root).replace(src_lang, dst_lang))
        # dst_files = map(lambda x: Path(dst_root, x.replace(src_lang, dst_lang)), files)
    
    sync_files(src_files, src_lang, dst_lang)

def error(msg: str):
    print(msg, file=sys.stderr)
    sys.exit()

def main(args: list[str]):
    if len(args) <= 2:
        error("Not enough arguments: provide source language and target language")

    src = Path(args[1])

    if not src.exists():
        error(f"Source language '" + args[1] + "' does not exist.")

    sync_folders(args[1], args[2])
    print(f"Source file count: ", src_count)
    print(f"Copied files count: ", copy_count)


if __name__ == "__main__":
    main(sys.argv)