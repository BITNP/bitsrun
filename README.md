# bitsrun

> A headless login / logout script for 10.0.0.55 at BIT.

## Install

You need at least Python 3.8. We recommend installing with `pipx`.

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

After which, install `bitsrun` with `pipx`.

```bash
pipx install bitsrun
```

## Usage

### CLI

```bash
bitsrun login -u|--username xxxx -p|--password xxxx
bitsrun logout -u|--username xxxx -p|--password xxxx
```

Optional params:

- `-s|--silent`: No output what-so-ever.
- `-nc|--no-color`: No color in error or verbose output.
- `-v|--verbose`: Output verbose information including full response from the API.

### Configuration file

Create new file named `bit-user.json`:

```json
{
    "username": "xxxx",
    "password": "xxxx"
}
```

This file should be put under the following directory:

- Windows: `%APPDATA%\bitsrun`
- macOS and Linux: `~/.config/bitsrun` (Following the XDG spec)

Now you can simply call:

```bash
bitsrun login
bitsrun logout
```

Besides, a system-wide configuration file is supported, and the location also depends on your platform.

To list all possible paths for your system (including those only for backward compatibility), call:

```shell
bitsrun config-paths
```

### Raycast script (macOS)

![Raycast Script Screenshot](assets/raycast-screenshot.png)

Import the two Raycast scripts from [`./scripts`](./scripts/) and setup your config file in `~/.config/bit-user.json`. The script uses `/usr/bin/python3` by default, so you either need to install `bitsrun` with this Python interpreter or setup your own Python interpreter path in the script.

## Developing

Install and run:

```bash
# Create virtual env and install deps
poetry install

# Enter poetry virtual env
poetry shell
```

Build:

```bash
# Bump version
poetry version x.x.x

# Building the wheel
poetry build
```

Publish:

```bash
poetry publish
```

## License

[WTFPL License](LICENSE)
