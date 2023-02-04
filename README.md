# bitsrun

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Pre-commit](https://github.com/BITNP/bitsrun/actions/workflows/ci.yml/badge.svg)](https://github.com/BITNP/bitsrun/actions/workflows/ci.yml)
[![PyPI Publish](https://github.com/BITNP/bitsrun/actions/workflows/python-publish.yml/badge.svg)](https://github.com/BITNP/bitsrun/actions/workflows/python-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/bitsrun)](https://pypi.org/project/bitsrun/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bitsrun)
![PyPI - Downloads](https://img.shields.io/pypi/dm/bitsrun)

_A headless login / logout script for 10.0.0.55 at BIT._

## Install

You need at least **Python 3.8**. We recommend installing with `pipx`.

```shell
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

After which, install `bitsrun` with `pipx`.

```shell
pipx install bitsrun
```

## Usage

### CLI

Check login status of your device.

![bitsrun status](https://user-images.githubusercontent.com/32114380/216757172-368d74bc-ad74-4122-9b1f-9568ce0341d3.png)

```text
Usage: bitsrun status [OPTIONS]

  Check current network login status.

Options:
  --help  Show this message and exit.
```

> **Note**: this is the output of `bitsrun status --help`.

Login or logout with your username and password.

![bitsrun login](https://user-images.githubusercontent.com/32114380/216757151-b6e8c620-48b6-4411-ac41-f07b79ef9827.png)

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

```shell
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

```shell
# Create virtual env and install deps
pdm install

# Enter virtual env
eval $(pdm venv activate)

# Install pre-commit hooks
pre-commit install
```

Build:

```shell
pdm build
```

Publish:

```shell
pdm publish
```

## Credits

- [Aloxaf/10_0_0_55_login](https://github.com/Aloxaf/10_0_0_55_login)

## License

[WTFPL License](LICENSE)
