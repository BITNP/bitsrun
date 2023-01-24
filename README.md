# bitsrun

[![Pre-commit](https://github.com/BITNP/bitsrun/actions/workflows/ci.yml/badge.svg)](https://github.com/BITNP/bitsrun/actions/workflows/ci.yml) [![PyPI Publish](https://github.com/BITNP/bitsrun/actions/workflows/python-publish.yml/badge.svg)](https://github.com/BITNP/bitsrun/actions/workflows/python-publish.yml) [![PyPI](https://img.shields.io/pypi/v/bitsrun)](https://pypi.org/project/bitsrun/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bitsrun) ![PyPI - Downloads](https://img.shields.io/pypi/dm/bitsrun)

_A headless login / logout script for 10.0.0.55 at BIT._

## Install

You need at least **Python 3.8**. We recommend installing with `pipx`.

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

```text
Usage: bitsrun login/logout [OPTIONS]

  Log into or out of the BIT network.

Options:
  -u, --username TEXT  Your username.
  -p, --password TEXT  Your password.
  -v, --verbose        Verbosely echo API response.
  --help               Show this message and exit.
```

> **Note**: this is the output of `bitsrun login/logout --help`.

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

![raycast screenshot](https://user-images.githubusercontent.com/32114380/213919582-eff6d58f-1bd2-47b2-a5da-46dc6e2eaffa.png)

Import the two Raycast scripts from [`./scripts`](./scripts/) and setup your config file in `~/.config/bit-user.json`. The script uses `/usr/bin/python3` by default, so you either need to install `bitsrun` with this Python interpreter or setup your own Python interpreter path in the script.

## Developing

Install and run:

```bash
# Create virtual env and install deps
poetry install

# Enter poetry virtual env
poetry shell

# Install pre-commit hooks
pre-commit install
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

## Credits

- [Aloxaf/10_0_0_55_login](https://github.com/Aloxaf/10_0_0_55_login)

## License

[WTFPL License](LICENSE)
