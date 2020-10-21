#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Aloxaf
# 2018.7.27

# 北理工校园网自动登录

import hmac
import json
import re
import requests
import socket
import math

from tempfile import gettempdir
from hashlib import sha1
from requests import Session
from enum import Enum
from base64 import b64encode
from typing import *

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
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


class AlreadyOnline(Exception):
    pass


class NetType(Enum):
    # 也可为空(旧接口)
    BIT = "@xiaoyuanwang"
    CMCC = "@yidong"
    CU = "@liantong"


class Action(Enum):
    LOGIN = "login"
    LOGOUT = "logout"


class User:

    # magic number
    N = 200
    TYPE = 1

    _API = "http://10.0.0.55/cgi-bin"

    def __init__(self, username: str, password: str, net_type: NetType):
        """
        :param username: 用户名(学号)
        :param password: 密码
        :param net_type: 网络类型(校园网/中国移动/中国联通)
        """
        self.username = username + net_type.value
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

        if "srun_portal" not in res.url:
            raise AlreadyOnline

        # acid = re.search(r"index_(\d+)\.html", res.url).groups()[0]
        acid = re.search(r"ac_id=(\d+)&", res.url).groups()[0]

        with open(f'{gettempdir()}/10_0_0_55_acid', 'w') as f:
            f.write(acid)

        return acid

    @staticmethod
    def get_acid_cached() -> str:
        """
        获取缓存的 acid
        :return: acid
        """
        return open(f'{gettempdir()}/10_0_0_55_acid').read()

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
            acid = self.get_acid_cached()

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


def main():
    """从命令行启动"""
    import argparse
    from pprint import pprint

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['login', 'logout'])
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('--net', choices=['BIT', 'CMCC', 'CU'], default='BIT', required=False)
    args = parser.parse_args()

    # action, username, password, net_type, *_ = argv[1:] + ["BIT"]
    net_type = {"BIT": NetType.BIT, "CMCC": NetType.CMCC, "CU": NetType.CU}[args.net]

    user = User(args.username, args.password, net_type)

    if args.action == "login":
        pprint(user.do_action(Action.LOGIN))
    elif args.action == "logout":
        pprint(user.do_action(Action.LOGOUT))


if __name__ == "__main__":
    main()
