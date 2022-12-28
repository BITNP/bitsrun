import sys
import click

from bitsrun.action import Action
from bitsrun.config import read_config
from bitsrun.user import User


@click.command()
@click.argument("action", type=click.Choice(["login", "logout"]))
@click.option("-u", "--username", help="Username.", required=False)
@click.option("-p", "--password", help="Password.", required=False)
@click.option("-v", "--verbose", is_flag=True, help="Verbose output.")
@click.option("-s", "--silent", is_flag=True, help="Silent output.")
@click.option("-nc", "--no-color", is_flag=True, help="No color output.")
def main(action, username, password, verbose, silent, no_color):
    """Login to the BIT network."""
    if username and password:
        user = User(username, password)
    elif conf := read_config():
        user = User(*conf)
    else:
        ctx = click.get_current_context()
        ctx.fail("No username/password provided.")

    try:
        if action == "login":
            res = user.do_action(Action.LOGIN)

            # Output login result by default if not silent
            if not silent:
                print(f"{res.get('username')} ({res.get('online_ip')}) logged in")

        else:
            res = user.do_action(Action.LOGOUT)

            # Output logout result by default if not silent
            if not silent:
                print(res.get("online_ip"), "logged out")

        # Output direct result of response if verbose
        if verbose:
            if no_color:
                print("Info:", res)
            else:
                print("\33[34m[Info]\033[0m", res)

    except Exception as e:
        if no_color:
            print("Error:", e)
        else:
            print("\033[91m[Error]", e, "\033[0m")

        # Throw with error code 1 for scripts to pick up error state
        sys.exit(1)


if __name__ == "__main__":
    main()
