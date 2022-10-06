import json
import os
from typing import Optional, Tuple


def get_config_path(filename: str) -> map:
    paths = ["/etc/"]
    if os.geteuid():
        xdg_config_home = os.getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            paths.append(xdg_config_home)
        else:
            paths.append(os.path.expanduser("~/.config"))
    return map(lambda path: os.path.join(path, filename), paths)


def read_config() -> Optional[Tuple[str, str]]:
    paths = get_config_path("bit-user.json")
    for path in paths:
        try:
            with open(path) as f:
                data = json.loads(f.read())
                return data["username"], data["password"]
        except Exception:
            continue
    return None
