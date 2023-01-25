import json
from os import getenv
from pathlib import Path
from sys import platform
from typing import Optional, Tuple, TypedDict

from platformdirs import site_config_path, user_config_path

_APP_NAME = "bitsrun"


def get_config_paths() -> map:
    r"""Enumerate possible paths of the configuration file.

    On Windows, the possible paths are:

    - `C:\ProgramData\bitsrun\bit-user.json`
    - `~\AppData\Roaming\bitsrun\bit-user.json`

    On Linux:

    - `/etc/bitsrun/bit-user.json`
    - `/etc/xdg/bitsrun/bit-user.json`
    - `~/.config/bitsrun/bit-user.json`
    - `~/.config/bit-user.json`

    On macOS:

    - `/etc/bit-user.json`
    - `/Library/Preferences/bitsrun/bit-user.json`
    - `$HOME/Library/Preferences/bitsrun/bit-user.json`
    - `$HOME/.config/bit-user.json`
    - `$HOME/.config/bitsrun/bit-user.json`

    Returns:
        A map of possible paths of the configuration file based on the current platform.
    """

    paths = [
        site_config_path(_APP_NAME, appauthor=False),
        user_config_path(_APP_NAME, appauthor=False, roaming=True),
    ]

    # For backward compatibility
    if not platform.startswith("win32"):
        paths.insert(0, Path("/etc/"))

        if platform.startswith("darwin"):
            xdg_config_home = getenv("XDG_CONFIG_HOME", "")
            if xdg_config_home.strip():
                paths.append(Path(xdg_config_home))
            else:
                paths.append(Path.home() / ".config")
            paths.append(paths[-1] / _APP_NAME)
        else:
            paths.append(user_config_path())

    return map(lambda path: path / "bit-user.json", paths)


class ConfigType(TypedDict):
    username: str
    password: str


def read_config() -> Optional[Tuple[ConfigType, str]]:
    """Read config from the first available config file with name `bit-user.json`.

    The config file should be a JSON file with the following structure:

    ```json
    { "username": "xxxx", "password": "xxxx" }
    ```

    Returns:
        A tuple of (config, path to config file) if the config file is found.
    """

    paths = get_config_paths()
    for path in paths:
        try:
            with open(path) as f:
                data = json.loads(f.read())
                return data, str(path)
        except Exception:
            continue
    return None
