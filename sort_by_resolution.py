"""Sort by resolution script

The script allows the user to sort images according to their resolution. Sorted 
images will be placed in appropriate directories with names corresponding to the 
resolutions of the images in them. If the image has a non-standard resolution 
(not defined by default in the script or by the user) it will be placed in a 
directory named others.

In order for images to be sorted correctly, they must have one of the following 
extensions:
(.jpg, .jpeg, .png, .gif, .webp, .tiff, .psd, .raw, .bmp, .heif, .indd, .svg,
.ai, .eps)

This tool only works properly on UNIX systems.
"""

import os
import re
import glob
import shutil
import argparse

from PIL import Image

BOLD = '\033[1m'
BOLD_END = '\033[0m'

def list_resolutions() -> None:
    """
    List resolutions from default_resolutions list
    """
    for resolution in default_resolutions:
        print(f"{resolution[0]}x{resolution[1]}", end=" ")
    print("\n")

def dir_path(path: str) -> str:
    """
    Check if path is a directory
    """
    if(os.path.isdir(path)):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def cmdline_args() -> argparse.Namespace:
    """
    Initializing argparser
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
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
    """
    Checks that the provided arguments are resolutions and transforms them into 
    list of resolutions in a format that corresponds to the default_resolutions
    list.
    """
    resolutions = []
    pattern = re.compile("^\d+x\d+$")

    for arg in args:
        if not pattern.match(arg):
            raise argparse.ArgumentTypeError(f"{arg} <- Incorrect resolution format")

        width, height = re.split("x", arg)
        resolutions.append((width, height))

    return resolutions

def is_image(path: str) -> bool:
    """
    Check if path is image
    """
    for extension in valid_images_extensions:
        if path.endswith(extension):
            return True

    return False

def get_images(root_dir: str, is_recursive: bool) -> dict:
    """
    Returns dictionary which maps resolution to list of path to images with 
    this resolution from provided directory and, if recursive is enabled, 
    from subdirectories.
    """
    images = {}

    for path in glob.iglob(root_dir + '**', recursive=is_recursive):
        if is_image(path):
            width, height = Image.open(path).size

            if (width, height) in default_resolutions:
                images.setdefault(f"{width}x{height}", []).append(path)
            else:
                images.setdefault("others", []).append(path)

    return images        

def create_dirs(root_dir: str, to_create: list) -> None:
    """
    Creates subdirectories in destination directory
    """
    for dir in to_create:
        dir_path = os.path.join(root_dir, dir)
        os.makedirs(dir_path, exist_ok=True)

def sort(src_root_dir: str, dest_root_dir: str, is_copy: bool, recursive: bool) -> None:
    """
    Sorting images.
    """
    action = shutil.copyfile if is_copy else shutil.move
    
    images = get_images(src_root_dir, recursive)
    create_dirs(src_root_dir, images.keys())

    for resolution in images.keys():
        for image_path in images[resolution]:
            image_name = os.path.basename(image_path)
            dest_path = os.path.join(dest_root_dir, resolution, image_name)
            action(image_path, dest_path)

def main():
    global default_resolutions

    src_dir = "./"
    dest_dir = "./"
    is_copy = False
    recursive = False

    args = cmdline_args()

    if args.input:
        src_dir = args.input

    if args.output:
        dest_dir = args.output

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
    else:
        sort(src_dir, dest_dir, is_copy, recursive)

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
    ".eps"
]

if __name__ == '__main__':
    main()
