import os
import sys
from pathlib import Path
import re

src_lang = ""

dst_lang = ""

src_count = 0
copy_count = 0
updated_count = 0

# def convert_string_to_dict(content: str) -> dict:
#     pairs = content.split()
#     new_dict = {}
#     for pair in pairs:
#         if ":" in pair:
#             key, value = pair.split(":", 1)
#             new_dict[key] = value
#     return new_dict

# def process_yaml(yaml_content: dict, lang: str) -> dict:
#     if isinstance(yaml_content.get(f"l_{lang}"), str):
#         yaml_content[f"l_{lang}"] = convert_string_to_dict(yaml_content[f"l_{lang}"])
#     return yaml_content

# def sync_file(src: Path, dst: Path):
#     with open(src, 'r', encoding="utf-8-sig") as file:
#         src_yaml = yaml.safe_load(file) or {}
        
#     with open(dst, 'r', encoding="utf-8-sig") as file:
#         dst_yaml = yaml.safe_load(file) or {}

#     src_yaml = process_yaml(src_yaml, src_lang)
#     dst_yaml = process_yaml(dst_yaml, dst_lang)

#     print("Source YAML structure:", src_yaml)

#     # Some files may have a localization section without anything in it
#     if not src_yaml.get(f"l_{src_lang}"):
#         print(f"No l_{src_lang} section found in {src}")
#         return
    
#     for key in src_yaml.get(f"l_{src_lang}"):
#         if key not in dst_yaml[f"l_{dst_lang}"]:
#             print(f"Found missing key: {key} with value: {src_yaml[f'l_{src_lang}'][key]}")

def get_keys_values(content: str):
    translations = dict()
    count = 0
    # Using my own regex instead of pyyaml bc the yaml may have versioning numbers that pyyml seems to no support
    for line in content.splitlines():
        line = line.strip()
        # Skip empty, comments or language tags
        if (not line or 
            line.startswith('#') or 
            'l_english:' in line or 
            'l_spanish:' in line):
            continue

        matches = re.match(r'(?:(.*?):\d+ "(.*?)"|(.+?): "(.*?)")', line, re.DOTALL)

        if not matches: continue

        key = matches.group(1) or matches.group(3)
        value = matches.group(2) or matches.group(4)

        if key and value:
            count += 1
            translations[key] = value
    
    return translations
    

def sync_file(src: Path, dst: Path):
    with open(src, 'r', encoding="utf-8-sig") as file:
        src_content = file.read()
        
    with open(dst, 'r', encoding="utf-8-sig") as file:
        dst_content = file.read()

    # Debugging
    # print("-------------------------------------------------------------")
    # print("Source file:", src)
    # print("Source YAML structure:", src_content)

    src_kv = get_keys_values(src_content)
    dst_kv = get_keys_values(dst_content)

    if not src_kv:
        print("skipped")
        return

    modified = False
    # print(len(src_kv))
    for k, v in src_kv.items():
        if k not in dst_kv:
            print(f"Added: {k} to {dst}")
            dst_kv[k] = v
            modified = True

    if modified:
        global updated_count
        updated_count += 1
    
def sync_files(src: list[Path]):
    global src_count
    global copy_count
    for src_file in src:
        src_count += 1
        dst_file = Path(str(src_file).replace(src_lang, dst_lang))
        if not dst_file.exists():
            # print(f"Copy::From {src_file} to {dst_file}")
            # dst_file.parent.mkdir(exist_ok=True)

            # # Change l_{src_lang} to l_{dst_lang} (l_english => l_spanish, for example)
            # with open(src_file, 'r', encoding="utf-8-sig") as file:
            #     content = file.read()
            # content = content.replace(f"l_{src_lang}", f"l_{dst_lang}")
            # with open(dst_file, 'w', encoding="utf-8-sig") as file:
            #     file.write(content)
            copy_count += 1
        else: # just sync those files that already exists, to avoid syncing the copied ones
            sync_file(src_file, dst_file)


def sync_folders():
    src = Path(src_lang)
    dst = Path(dst_lang)

    for root, dirs, files in src.walk():
        src_files = map(lambda x: Path(root, x), files)
        sync_files(src_files)
        # dst_root = Path(str(root).replace(src_lang, dst_lang))
        # dst_files = map(lambda x: Path(dst_root, x.replace(src_lang, dst_lang)), files)
    
    sync_files(src_files)

def error(msg: str):
    print(msg, file=sys.stderr)
    sys.exit()

def main(args: list[str]):
    if len(args) <= 2:
        error("Not enough arguments: provide source language and target language")

    src = Path(args[1])

    if not src.exists():
        error(f"Source language '" + args[1] + "' does not exist.")

    global src_lang
    global dst_lang
    src_lang = args[1]
    dst_lang = args[2]

    sync_folders()
    print(f"Source file count: {src_count}")
    print(f"Copied files count: {copy_count}")
    print(f"Already existing but modified: {updated_count}")


if __name__ == "__main__":
    main(sys.argv)