import argparse
from genericpath import isdir
import os
from typing import Dict
from PIL import Image
import re
import glob

BOLD = '\033[1m'
BOLD_END = '\033[0m'

default_resolutions = [
    (320, 480), 
    (320, 568), 
    (360, 640), 
    (375, 667), 
    (480, 800), 
    (480, 854), 
    (800, 600), 
    (540, 960), 
    (600, 1024), 
    (640, 960), 
    (1024, 600), 
    (640, 1136), 
    (768, 1024), 
    (1024, 768), 
    (720, 1208), 
    (1280, 720), 
    (720, 1280), 
    (1280, 768), 
    (750, 1334), 
    (800, 1280), 
    (1280, 800), 
    (1366, 768), 
    (1440, 900), 
    (1280, 1024), 
    (1600, 900), 
    (828, 1792), 
    (2048, 768), 
    (1680, 1050), 
    (1200, 1600), 
    (1600, 1200), 
    (1080, 1800), 
    (1080, 1812), 
    (1920, 1080), 
    (1080, 1920), 
    (1080, 2160), 
    (3072, 768), 
    (1080, 2340), 
    (2880, 900), 
    (1125, 2436), 
    (1242, 2208), 
    (2560, 1080), 
    (3200, 900), 
    (1170, 2532), 
    (1400, 2160), 
    (3840, 800), 
    (2160, 1440), 
    (1536, 2048), 
    (2048, 1536), 
    (4098, 768), 
    (1242, 2588), 
    (2160, 1620), 
    (1620, 2160), 
    (1284, 2778), 
    (1440, 2560), 
    (2560, 1440), 
    (1668, 2224), 
    (2224, 1668), 
    (2360, 1640), 
    (1640, 2360), 
    (4320, 900), 
    (2388, 1668), 
    (1668, 2388), 
    (2560, 1600), 
    (3840, 1080), 
    (2732, 1536), 
    (1440, 2960), 
    (4800, 900), 
    (3440, 1440), 
    (2736, 1824), 
    (1824, 2736), 
    (2880, 1800), 
    (2048, 2732), 
    (2732, 2048), 
    (3200, 1800), 
    (5760, 1080), 
    (3840, 2160), 
    (4096, 2304), 
    (5120, 2880)
]

valid_images_extensions = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".tiff",
    ".psd",
    ".raw",
    ".bmp",
    ".heif",
    ".indd",
    ".svg",
    ".ai",
    "eps"
]

def list_resolutions() -> None:
    for resolution in default_resolutions:
        print(f"{resolution[0]}x{resolution[1]}", end=" ")
    print("\n")

def dir_path(path: str) -> str:
    if(os.path.isdir(path)):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def cmdline_args() -> None:
    parser = argparse.ArgumentParser(
        description="Sort images by resolution by moving them to the appropriate subdirectories.")
    parser.add_argument(
        "-i",
        "--input", 
        type=dir_path, 
        help="path to the directory with images")
    parser.add_argument(
        "-o",
        "--output", 
        type=dir_path, 
        help="path to the root directory where the sorted images will be placed")
    parser.add_argument(
        "-R", 
        "--recursive", 
        action="store_true", 
        help="sort images from all subdirectories")
    parser.add_argument(
        "-r", 
        "--resolutions", 
        nargs="+", 
        type=str, 
        help=f"""override default resolution list. 
        Resolution format {BOLD}width{BOLD_END}x{BOLD}height{BOLD_END} 
        for e.g. 1920x1080""")
    parser.add_argument(
        "-a",
        "--append",
        nargs="+", 
        type=str,
        help=f"""append resolutions to default resolution list. 
        Resolution format {BOLD}width{BOLD_END}x{BOLD}height{BOLD_END} 
        for e.g. 1920x1080""")
    parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        type=str,
        help=f"""exclude resolutions from default resolution list. 
        Resolution format {BOLD}width{BOLD_END}x{BOLD}height{BOLD_END} 
        for e.g. 1920x1080""")
    parser.add_argument(
        "-c", 
        "--copy", 
        action="store_true", 
        help="sorted images will be copied to the new location")
    parser.add_argument(
        "-l",
        "--list",
        action="store_true", 
        help="list all default resolutions"
    )
    
    return parser.parse_args()

def resolve_resolution(args: list) -> list:
    resolutions = []

    pattern = re.compile("^\d+x\d+$")

    for arg in args:
        if not pattern.match(arg):
            raise ValueError(f"{arg} <- Incorrect resolution format")
        
        width, height = re.split("x", arg)
        resolutions.append((width, height))

    return resolutions

def is_image(path: str) -> bool:
    for extension in valid_images_extensions:
        if path.endswith(extension):
            return True
    return False

def get_images(root_dir: str, is_recursive: bool) -> Dict:
    images = {}

    for path in glob.iglob(root_dir + '**', recursive=is_recursive):
        if is_image(path):
            width, height = Image.open(path).size
            images.setdefault((width, height), []).append(path)
    return images        

def move(target: str, dest: str):
    print("move")

def copy(target: str, dest: str):
    print("copy")

def sort(input: str, output: str, is_copy: bool, recursive: bool) -> None:
    action = copy if is_copy else move

def main():
    input = "./"
    output = "./"
    is_copy = False
    recursive = False

    args = cmdline_args()

    if args.input:
        input = args.input

    if args.output:
        output = args.output

    if args.recursive:
        recursive = True

    if args.copy:
        is_copy = True

    if args.resolutions:
        default_resolutions = resolve_resolution(args.resolutions)

    if args.append:
        new_resolutions = resolve_resolution(args.append)
        default_resolutions = list(set(default_resolutions + new_resolutions))

    if args.exclude:
        new_resolutions = resolve_resolution(args.exclude)
        default_resolutions = list(set(default_resolutions) - set(new_resolutions))

    if args.list:
        list_resolutions()
        exit(0)

main()