# bitsrun

> A headless login / logout script for 10.0.0.55 at BIT.

## Install

You need at least Python 3.7. We recommend installing with `pipx`.

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

Edit `bit-user.json`:

```json
{
    "username": "xxxx",
    "password": "xxxx"
}
```

This file should be put under the following directory:

- macOS: `~/Library/Preferences/bitsrun`
- Windows: `%APPDATA%\bitsrun`
- Unix: We follow the XDG spec and support `$XDG_CONFIG_HOME`. That means, by default `~/.config/bitsrun`.

Now you can simply call

```bash
bitsrun login
bitsrun logout
```

Besides, a system-wide configuration file is supported, and the location also depends on your platform.

To list all possible paths for your system (including those only for backward compatibility), call

```shell
bitsrun config-paths
```

### Raycast script (macOS)

![Raycast Script Screenshot](assets/raycast-screenshot.png)

Import the two Raycast scripts from [`./scripts`](./scripts/) and setup your config file in `~/.config/bit-user.json`. The script uses `/usr/bin/python3` by default, so you either need to install `bitsrun` with this Python interpreter or setup your own Python interpreter path in the script.

<details>
<summary>Using networkmanager-dispatcher (deprecated).</summary>

### 使用 NetworkManager-dispacher

将 `bitsrun.py` 复制为 `/usr/bin/bit-login`，权限+x

将 `login-bit.sh` 复制到 `/etc/NetworkManager/dispatcher.d/`

将配置文件保存在 `/etc/bit-user.json`

start 并且 enable NetworkManager-dispatcher

</details>

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
