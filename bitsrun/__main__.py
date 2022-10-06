import argparse
import sys

from .action import Action
from .config import read_config
from .user import User


def main():
    parser = argparse.ArgumentParser(description="Login to BIT network")
    parser.add_argument("action", choices=["login", "logout"], help="login or logout")
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-s", "--silent", action="store_true")
    parser.add_argument("-nc", "--no-color", action="store_true")
    args = parser.parse_args()

    if args.username and args.password:
        user = User(args.username, args.password)
    elif conf := read_config():
        user = User(*conf)
    else:
        parser.print_usage()
        sys.exit(1)

    try:
        if args.action == "login":
            res = user.do_action(Action.LOGIN)

            # Output login result by default if not silent
            if not args.silent:
                print(f"{res.get('username')} ({res.get('real_name')}) logged in")

        else:
            res = user.do_action(Action.LOGOUT)

            # Output logout result by default if not silent
            if not args.silent:
                print(res.get("online_ip"), "logged out")

        # Output direct result of response if verbose
        if args.verbose:
            if args.no_color:
                print("Info:", res)
            else:
                print("\33[34m[Info]\033[0m", res)

    except Exception as e:
        if args.no_color:
            print("Error:", e)
        else:
            print("\033[91m[Error]", e, "\033[0m")

        # Throw with error code 1 for scripts to pick up error state
        sys.exit(1)


if __name__ == "__main__":
    main()
