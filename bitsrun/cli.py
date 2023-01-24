import sys
from getpass import getpass
from pprint import pprint

import click

from bitsrun.config import get_config_paths, read_config
from bitsrun.user import User

# A hacky way to specify shared options for multiple click commands:
# https://stackoverflow.com/questions/40182157/shared-options-and-flags-between-commands
_options = [
    click.option("-u", "--username", help="Your username.", required=False),
    click.option("-p", "--password", help="Your password.", required=False),
    click.option("-v", "--verbose", is_flag=True, help="Verbosely echo API response."),
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
def login(username, password, verbose):
    """Log into the BIT network."""
    do_action("login", username, password, verbose)


@cli.command()
@add_options(_options)
def logout(username, password, verbose):
    """Log out of the BIT network."""
    do_action("logout", username, password, verbose)


def do_action(action, username, password, verbose):
    # Support reading password from stdin when not passed via `--password`
    if username and not password:
        password = getpass(prompt="Please enter your password: ")

    # Try to read username and password from args provided. If none, look for config
    # files in possible paths. If none, fail and prompt user to provide one.
    if username and password:
        user = User(username, password)
    elif conf := read_config():
        user = User(**conf[0])
        if verbose:
            click.echo(
                click.style("bitsrun: ", fg="blue")
                + "Reading config from "
                + click.style(conf[1], fg="yellow", underline=True)
            )
    else:
        ctx = click.get_current_context()
        ctx.fail("No username or password provided")

    try:
        if action == "login":
            resp = user.login()
            message = f"{user.username} ({resp['online_ip']}) logged in"
        elif action == "logout":
            resp = user.logout()
            message = f"{resp['online_ip']} logged out"
        else:
            # Should not reach here, but just in case
            raise ValueError(f"Unknown action `{action}`")

        # Output direct result of the API response if verbose
        if verbose:
            click.echo(f"{click.style('bitsrun:', fg='cyan')} Response from API:")
            pprint(resp)

        # Handle error from API response. When field `error` is not `ok`, then the
        # login/logout action has likely failed. Hints are provided in the `error_msg`.
        if resp["error"] != "ok":
            raise Exception(
                resp["error_msg"]
                if resp["error_msg"]
                else "Action failed, use --verbose for more info"
            )

        # Print success message
        click.echo(f"{click.style('bitsrun:', fg='green')} {message}")

    except Exception as e:
        # Exception is caught and printed to stderr
        click.echo(f"{click.style('error:', fg='red')} {e}", err=True)
        # Throw with error code 1 for scripts to pick up error state
        sys.exit(1)


if __name__ == "__main__":
    cli()
