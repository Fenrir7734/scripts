import string
import argparse
import secrets
import pyperclip

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
        "-c",
        "--copy",
        action="store_true",
        help="do not print, copy to clipboard instead"
    )
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
            print("-d option cannot be combined with " \
            "any of the following options: -L -U -N -S")
            exit(0)
        alphabet = args.define

    if not alphabet:
        alphabet += string.ascii_letters + string.digits + string.punctuation
    return alphabet

def get_passwd_lenght(args: argparse.Namespace) -> int:
    if not args.lenght:
        return 16
    number = args.lenght
    if number <= 0:
        print("Incorrect password lenght")
        exit(0)
    if number < 8:
        print("Recommended password lenght is at least 8 characters. " \
            "For password of lenght smaller than 8 password policy is disabled.")
    return number

def check_for_lowercase(passwd: str, alphabet: str) -> bool:
    return (not any(c.islower() for c in alphabet) or 
                any(c.islower() for c in passwd))

def check_for_uppercase(passwd: str, alphabet: str) -> bool:
    return (not any(c.isupper() for c in alphabet) or 
                any(c.isupper() for c in passwd))

def check_for_digit(passwd: str, alphabet: str) -> bool:
    return (not any(c.isdigit() for c in alphabet) or 
                any(c.isdigit() for c in passwd))

def check_for_special(passwd: str, alphabet: str) -> bool:
    return (not any(c in string.punctuation for c in alphabet) or 
                any(c in string.punctuation for c in passwd))

def check_password(passwd: str, alphabet: str) -> bool:
    return  (len(passwd) < 8 or (check_for_lowercase(passwd, alphabet) and 
                                check_for_uppercase(passwd, alphabet) and 
                                check_for_digit(passwd, alphabet) and 
                                check_for_special(passwd, alphabet)))

def generate_passwd(alphabet: str, n: int) -> str:
    while True:
        passwd = "".join(secrets.choice(alphabet) for i in range(n))
        if check_password(passwd, alphabet):
            return passwd

def main() -> None:
    args = cmdline_args()
    alphabet = create_alphabet(args)
    lenght = get_passwd_lenght(args)
    passwd = generate_passwd(alphabet, lenght)
    
    if args.copy:
        pyperclip.copy(passwd)
    else:
        print(passwd)

if __name__ == '__main__':
    main()