# bitsrun

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://github.com/BITNP/bitsrun/actions/workflows/ci.yml/badge.svg)](https://github.com/BITNP/bitsrun/actions/workflows/ci.yml)
[![PyPI Publish](https://github.com/BITNP/bitsrun/actions/workflows/python-publish.yml/badge.svg)](https://github.com/BITNP/bitsrun/actions/workflows/python-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/bitsrun)](https://pypi.org/project/bitsrun/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bitsrun)](https://pypi.org/project/bitsrun/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/bitsrun?color=orange)](https://pypi.org/project/bitsrun/)

A headless login / logout script for 10.0.0.55 at BIT.

| :sparkles: | Blazingly™ Fast Rust re-implementation of `bitsrun` available at [spencerwooo/bitsrun](https://github.com/spencerwooo/bitsrun-rs), if you require or prefer a single compiled executable (or 🦀 Rust). |
| - |:-|

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

Alternatively, you can download a self-contained executable from [GitHub Releases](https://github.com/BITNP/bitsrun/releases/latest) if you are working from an environment that does not have internet access.

## Usage

### CLI

Check login status of your device.

![bitsrun status](https://github.com/BITNP/bitsrun/assets/32114380/e877d6a9-120a-444a-b580-0a0fcac857ce)

```text
Usage: bitsrun status [OPTIONS]

  Check current network login status.

Options:
  --json / --no-json  Output in JSON format.
  --help  Show this message and exit.
```

> **Note**: this is the output of `bitsrun status --help`.

Login or logout with your username and password.

![bitsrun login](https://github.com/BITNP/bitsrun/assets/32114380/4ca8cd64-580b-4ab8-824f-0049f41f78bb)

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

### Credentials config

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

**On unix, set the file permission to `600`, i.e., only read/writeable by the owner:**

```shell
chmod 600 path/to/bit-user.json
```

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

Create virtual environment and install deps:

```shell
python -m venv venv
source venv/bin/activate
pip install -e .
```

Running CLI entry:

```shell
python src/bitsrun/cli.py
```

Build:

```shell
pip install setuptools build
python -m build
```

## Credits and related

- [Aloxaf/10_0_0_55_login](https://github.com/Aloxaf/10_0_0_55_login) - BIT 10.0.0.55 的登入与登出的 Python 实现 (This project's predecessor, archived)
- [spencerwooo/bitsrun-rs](https://github.com/spencerwooo/bitsrun-rs) - A Rust implementation of `bitsrun`. (Rust)
- [zu1k/srun](https://github.com/zu1k/srun) - Srun authentication system login tools. (Rust)
- [Mmx233/BitSrunLoginGo](https://github.com/Mmx233/BitSrunLoginGo) - 深澜校园网登录脚本 Go 语言版 (Go)
- [vouv/srun](https://github.com/vouv/srun) - An efficient client for BIT campus network. (Go)

## License

[WTFPL License](LICENSE)
