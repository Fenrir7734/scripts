import os.path
import shutil
import sys
import requests
from tqdm import tqdm

OUT_DIR = "./ligman_books"
BOOKS_URL = "http://ligman.me/2sZVmcG"


def get_books_list() -> list:
    res = requests.get(BOOKS_URL)

    if res.status_code == 200:
        return list(res.iter_lines(decode_unicode=True))[1:]

    print(f"Failed to get list of books. Http status code: {res.status_code}")
    sys.exit()


def make_out_dir() -> None:
    if os.path.exists(OUT_DIR):
        res = input(f"{OUT_DIR} already exists. Override it? (Y/n) ")

        if res == "Y":
            shutil.rmtree(OUT_DIR)
        else:
            print("Abort.")
            sys.exit()

    os.makedirs(OUT_DIR)


def clear_lines(count: int) -> None:
    for _ in range(count):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")


def download_book(url: str) -> None:
    res = requests.get(url, stream=True)
    book_name = res.url.split("/")[-1]

    print(f"Downloading {book_name}")

    with open(os.path.join(OUT_DIR, book_name), "wb") as file:
        pbar = tqdm(total=int(res.headers['Content-Length']), unit="B", unit_scale=True)
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                pbar.update(len(chunk))
                file.write(chunk)

    clear_lines(2)


def main() -> None:
    make_out_dir()
    book_list = get_books_list()

    for i in range(len(book_list)):
        print(f"Downloaded {i}/{len(book_list)} books.", end="\n\n")
        download_book(book_list[i])
        clear_lines(2)

    print(f"Downloaded {len(book_list)}/{len(book_list)} books.", end="\n\n")
    print("Download completed.")


if __name__ == '__main__':
    main()
