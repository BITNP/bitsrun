import json
from os import getenv
from pathlib import Path
from sys import platform
from typing import Optional, Tuple

from platformdirs import site_config_path, user_config_path

_APP_NAME = "bitsrun"


def get_config_paths() -> map:
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
        else:
            paths.append(user_config_path())

    return map(lambda path: path / "bit-user.json", paths)


def read_config() -> Optional[Tuple[str, str]]:
    paths = get_config_paths()
    for path in paths:
        try:
            with open(path) as f:
                data = json.loads(f.read())
                return data["username"], data["password"]
        except Exception:
            continue
    return None
