# 10_0_0_55

> A headless login / logout script for 10.0.0.55.

## Install

You need at least Python 3.9.

```bash
python -m pip install 10_0_0_55
```

## Usage

### CLI

```bash
python -m 10_0_0_55 login -u|--username xxxx -p|--password xxxx [-v|--verbose]
python -m 10_0_0_55 logout -u|--username xxxx -p|--password xxxx [-v|--verbose]
```

### Config file

Either `/etc/bit-user.json` or `~/.config/bit-user.json`:

```json
{
    "username": "xxxx",
    "password": "xxxx"
}
```

```bash
python -m 10_0_0_55 login [-v|--verbose]
python -m 10_0_0_55 logout [-v|--verbose]
```

<details>
<summary>Using networkmanager-dispatcher (deprecated).</summary>

### 使用 NetworkManager-dispacher

将 `10_0_0_55.py` 复制为 `/usr/bin/bit-login`，权限+x

将 `login-bit.sh` 复制到 `/etc/NetworkManager/dispatcher.d/`

将配置文件保存在 `/etc/bit-user.json`

start 并且 enable NetworkManager-dispatcher

</details>

## Developing

```bash
# Create virtual env and install deps
poetry install

# Enter poetry virtual env
poetry shell

# ... normal stuff with python -m 10_0_0_55 ...

# Building the wheel
poetry build
```
