from random import shuffle
import string
import argparse
import secrets

def cmdline_args() -> argparse.Namespace:
    """
    Initializing argparser
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-l",
        "--lenght",
        type=int,
        help="password lenght")
    parser.add_argument(
        "-d",
        "--define",
        type=str,
        help="define set of characters")
    parser.add_argument(
        "-L",
        "--Lowercase",
        action="store_true",
        help="include lowercase characters")
    parser.add_argument(
        "-U",
        "--Uppercase",
        action="store_true",
        help="include uppercase characters")
    parser.add_argument(
        "-N",
        "--Numbers",
        action="store_true",
        help="include numbers")
    parser.add_argument(
        "-S",
        "--Symbols",
        action="store_true",
        help="include symbols")

    return parser.parse_args()

def create_alphabet(args: argparse.Namespace) -> str:
    alphabet = ""

    if args.Lowercase:
        alphabet += string.ascii_lowercase
    
    if args.Uppercase:
        alphabet += string.ascii_uppercase
    
    if args.Numbers:
        alphabet += string.digits
    
    if args.Symbols:
        alphabet += string.punctuation
    
    if args.define:
        if alphabet:
            print("You cannot use any other option when -d option is specified")
            exit(0)
        alphabet = args.define

    if not alphabet:
        alphabet += string.ascii_letters + string.digits + string.punctuation
    
    return alphabet

def generate_passwd(alphabet: str, n: int) -> None:
    alphabet = shuffle(alphabet)
    passwd = "".join(secrets.choice(alphabet) for i in range(n))
    print(passwd)

def main() -> None:
    args = cmdline_args()
    alphabet = create_alphabet(args)
    lenght = 16

    if args.lenght:
        lenght = args.lenght

    generate_passwd(alphabet, lenght)


if __name__ == '__main__':
    main()