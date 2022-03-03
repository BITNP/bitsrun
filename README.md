# 10_0_0_55

登录 10.0.0.55

## Install

```bash
python -m pip install 10_0_0_55-2.0.0-py3-none-any.whl
```

## Usage

### CLI

```bash
python -m 10_0_0_55 login --username xxxx --password xxxx [--verbose]
python -m 10_0_0_55 logout --username xxxx --password xxxx [--verbose]
```

### Config file

配置文件路径：`/etc/bit-user.json` 或者 `~/.config/bit-user.json`：

```json
{
    "username": "xxxx",
    "password": "xxxx"
}
```

```bash
python -m 10_0_0_55 login
python -m 10_0_0_55 logout
```

### 使用 NetworkManager-dispacher

将 `10_0_0_55.py` 复制为 `/usr/bin/bit-login`，权限+x

将 `login-bit.sh` 复制到 `/etc/NetworkManager/dispatcher.d/`

将配置文件保存在 `/etc/bit-user.json`

start 并且 enable NetworkManager-dispatcher

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
