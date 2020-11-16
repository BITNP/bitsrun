# 10_0_0_55_login

登录 10.0.0.55

## 使用命令行传入参数

```bash
python 10_0_0_55.py login --username 1120xxxxxx --password xxxxxxxxx
python 10_0_0_55.py logout --username 1120xxxxxx --password xxxxxxxxx
```

## 使用配置文件
配置文件路径: `/etc/bit-user.json`或者`~/.config/bit-user.json`
```json
{
    "username": "1120xxxxxx",
    "password": "xxxx"
}
```
```bash
python 10_0_0_55.py login
python 10_0_0_55.py logout
```

## 使用NetworkManager-dispacher
将`10_0_0_55.py`复制为`/usr/bin/bit-login`，权限+x

将`login-bit.sh`复制到`/etc/NetworkManager/dispatcher.d/`

将配置文件保存在`/etc/bit-user.json`

start并且enable NetworkManager-dispatcher
