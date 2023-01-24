import sys
from getpass import getpass

import click

from bitsrun.action import Action
from bitsrun.config import get_config_paths, read_config
from bitsrun.user import User

# A hacky way to specify shared options for multiple click commands:
# https://stackoverflow.com/questions/40182157/shared-options-and-flags-between-commands
_options = [
    click.option("-u", "--username", help="Username.", required=False),
    click.option("-p", "--password", help="Password.", required=False),
    click.option("-v", "--verbose", is_flag=True, help="Verbosely echo API response."),
    click.option("-s", "--silent", is_flag=True, help="Silent, no output to stdout."),
]


# Decorator to add options to a click command (used w/ the hack above)
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


# Declaration of the main command group starts here
@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
def config_paths():
    """List possible paths of the configuration file."""
    click.echo("\n".join(map(str, get_config_paths())))


@cli.command()
@add_options(_options)
def login(username, password, verbose, silent):
    """Log into the BIT network."""
    do_action("login", username, password, verbose, silent)


@cli.command()
@add_options(_options)
def logout(username, password, verbose, silent):
    """Log out of the BIT network."""
    do_action("logout", username, password, verbose, silent)


def do_action(action, username, password, verbose, silent):
    """Log in/out the BIT network."""
    if username and not password:
        password = getpass(prompt="Please enter your password: ")
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
                click.echo(f"{res.get('username')} ({res.get('online_ip')}) logged in")

        else:
            res = user.do_action(Action.LOGOUT)

            # Output logout result by default if not silent
            if not silent:
                click.echo(res.get("online_ip"), "logged out")

        # Output direct result of response if verbose
        if verbose:
            click.secho(f"Info: {res}", fg="blue")

    except Exception as e:
        click.secho(f"Error: {e}", fg="red")

        # Throw with error code 1 for scripts to pick up error state
        sys.exit(1)


if __name__ == "__main__":
    cli()
