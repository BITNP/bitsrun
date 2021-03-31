#!/usr/bin/env python
# Author: Aloxaf, felinae98

# 北理工校园网自动登录

import hmac
import json
import re
import requests
import socket
import math
import argparse
import os
import sys

from hashlib import sha1
from requests import Session
from enum import Enum
from base64 import b64encode
from typing import *
from html.parser import HTMLParser

Json = Union[int, str, float, bool, None, List["Json"], Dict[str, "Json"]]


def fkbase64(raw_s):
    """计算魔改base64"""
    trans = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
        "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA",
    )
    ret = b64encode(bytes(ord(i) & 0xFF for i in raw_s))
    return ret.decode().translate(trans)


def xencode(msg, key):
    def sencode(msg, key):
        def ordat(msg, idx):
            if len(msg) > idx:
                return ord(msg[idx])
            return 0

        l = len(msg)
        pwd = []
        for i in range(0, l, 4):
            pwd.append(
                ordat(msg, i)
                | ordat(msg, i + 1) << 8
                | ordat(msg, i + 2) << 16
                | ordat(msg, i + 3) << 24
            )
        if key:
            pwd.append(l)
        return pwd

    def lencode(msg, key):
        l = len(msg)
        ll = (l - 1) << 2
        if key:
            m = msg[l - 1]
            if m < ll - 3 or m > ll:
                return
            ll = m
        for i in range(0, l):
            msg[i] = (
                chr(msg[i] & 0xFF)
                + chr(msg[i] >> 8 & 0xFF)
                + chr(msg[i] >> 16 & 0xFF)
                + chr(msg[i] >> 24 & 0xFF)
            )
        if key:
            return "".join(msg)[0:ll]
        return "".join(msg)

    if msg == "":
        return ""
    pwd = sencode(msg, True)
    pwdk = sencode(key, False)
    if len(pwdk) < 4:
        pwdk = pwdk + [0] * (4 - len(pwdk))
    n = len(pwd) - 1
    z = pwd[n]
    y = pwd[0]
    c = 0x86014019 | 0x183639A0
    m = 0
    e = 0
    p = 0
    q = math.floor(6 + 52 / (n + 1))
    d = 0
    while 0 < q:
        d = d + c & (0x8CE0D9BF | 0x731F2640)
        e = d >> 2 & 3
        p = 0
        while p < n:
            y = pwd[p + 1]
            m = z >> 5 ^ y << 2
            m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
            m = m + (pwdk[(p & 3) ^ e] ^ z)
            pwd[p] = pwd[p] + m & (0xEFB8D130 | 0x10472ECF)
            z = pwd[p]
            p = p + 1
        y = pwd[0]
        m = z >> 5 ^ y << 2
        m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
        m = m + (pwdk[(p & 3) ^ e] ^ z)
        pwd[n] = pwd[n] + m & (0xBB390742 | 0x44C6F8BD)
        z = pwd[n]
        q = q - 1
    return lencode(pwd, False)


def get_host_ip() -> str:
    """
    获取本机 IP
    :return: IP
    """
    res = requests.get("http://10.0.0.55")
    class SimpleParser(HTMLParser):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.user_ip = ""
        def handle_starttag(self, tag, attrs):
            if tag == "input":
                attr_dict = dict(attrs)
                if attr_dict.get('name') == 'user_ip':
                    self.user_ip = attr_dict['value']
        def feed(self, *args, **kwargs):
            super().feed(*args, **kwargs)
            return self.user_ip
    parser = SimpleParser()
    ip = parser.feed(res.text)
    if not ip:
        raise RuntimeError("you are not in bit")
    return ip


class AlreadyOnline(Exception):
    pass


class Action(Enum):
    LOGIN = "login"
    LOGOUT = "logout"


class User:

    # magic number
    N = 200
    TYPE = 1

    _API = "http://10.0.0.55/cgi-bin"

    def __init__(self, username: str, password: str):
        """
        :param username: 用户名(学号)
        :param password: 密码
        """
        self.username = username
        self.password = password
        self.ip = get_host_ip()
        self.ses = Session()

    @staticmethod
    def get_acid() -> str:
        """
        获取 acid
        :return: acid
        """
        # http://detectportal.firefox.com 似乎不准
        res = requests.get("http://126.com")

        if "srun_portal" in res.url:
            acid = re.search(r"ac_id=(\d+)&", res.url).groups()[0]
            return acid
        elif "10.0.0.55" in res.text:
            res = requests.get('http://10.0.0.55/index_1.html')
            acid = re.search(r"ac_id=(\d+)&", res.url).groups()[0]
            return acid
        raise AlreadyOnline

    @staticmethod
    def get_login_acid() -> str:
        """
        获取缓存的 acid
        :return: acid
        """
        res = requests.get('http://10.0.0.55')
        acid = re.search(r'ac_id=(\d+)&', res.url).groups()[0]
        return acid

    def _get_token(self) -> str:
        """
        获取登录 TOKEN
        :return: TOKEN
        """
        params = {"callback": "jsonp", "username": self.username, "ip": self.ip}
        response = self.ses.get(f"{self._API}/get_challenge", params=params)
        result = json.loads(response.text[6:-1])
        return result["challenge"]

    def _make_params(self, action: Action) -> Dict[str, str]:
        """
        生成验证所需参数
        :param action: 动作(登入/登出)
        :return: 参数
        """
        token = self._get_token()

        if action is Action.LOGIN:
            acid = self.get_acid()
        else:
            acid = self.get_login_acid()

        params = {
            "callback": "jsonp",
            "username": self.username,
            "action": action.value,
            "ac_id": acid,
            "ip": self.ip,
            # 意义不明的 magic number
            "type": self.TYPE,
            "n": self.N,
        }
        data = {
            "username": self.username,
            "password": self.password,
            "acid": acid,
            "ip": self.ip,
            "enc_ver": "srun_bx1",
        }
        hmd5 = hmac.new(token.encode(), b"", "MD5").hexdigest()
        json_data = json.dumps(data, separators=(",", ":"))
        info = "{SRBX1}" + fkbase64(xencode(json_data, token))
        chksum = sha1(
            "{0}{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}".format(
                token, self.username, hmd5, acid, self.ip, self.N, self.TYPE, info
            ).encode()
        ).hexdigest()
        params.update({"password": "{MD5}" + hmd5, "chksum": chksum, "info": info})

        return params

    def do_action(self, action: Action) -> Json:
        """
        执行动作
        :param action: Action(LOGIN/LOGOUT)
        :return: API 返回的 JSON
        """
        params = self._make_params(action)
        response = self.ses.get(f"{self._API}/srun_portal", params=params)
        return json.loads(response.text[6:-1])

def get_config_path(filename: str) -> List[str]:
    "get config file path"
    paths = ['/etc/']
    if os.geteuid():
        if os.getenv('XDG_CONFIG_HOME'):
            paths.append(os.getenvb('XDG_CONFIG_HOME'))
        else:
            paths.append(os.path.expanduser('~/.config'))
    return map(lambda path: os.path.join(path, filename), paths)

def read_config():
    paths = get_config_path('bit-user.json')
    for path in paths:
        try:
            with open(path) as f:
                data = json.loads(f.read())
                return (data['username'], data['password'])
        except:
            continue
    return None

def main():
    """从命令行启动"""
    parser = argparse.ArgumentParser(description="Login to BIT network")
    parser.add_argument('action', choices=['login', 'logout'], help='login or logout')
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    if args.username and args.password:
        user = User(args.username, args.password)
    elif conf := read_config():
        user = User(*conf)
    else:
        sys.exit(1)
    if args.action == 'login':
        res = user.do_action(Action.LOGIN)
    else:
        res = user.do_action(Action.LOGOUT)
    if args.verbose:
        print(res)

if __name__ == "__main__":
    main()
