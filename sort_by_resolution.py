import argparse
from genericpath import isdir
import os
from PIL import Image

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

def dir_path(path):
    if(os.path.isdir(path)):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def cmdline_args():
    parser = argparse.ArgumentParser(description="Sort images by resolution by moving them to the appropriate subdirectories.")
    parser.add_argument(
        "input", 
        type=dir_path, 
        help="path to the directory with images")
    parser.add_argument(
        "output", 
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
        help="resolution list, all images with a different resolution than specified will be placed in the directory others.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m", 
        "--move", 
        action="store_true", 
        help="sorted images will be moved to the new location")
    group.add_argument(
        "-c", 
        "--copy", 
        action="store_true", 
        help="sorted images will be copied to the new location")
    
    return parser.parse_args()

def main():
    args = cmdline_args()

    if args.recursive:
        pass

    if args.resolutions:
        pass

    if args.move:
        pass

main()