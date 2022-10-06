import math
from base64 import b64encode
from html.parser import HTMLParser
from typing import Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests

API_BASE = "http://10.0.0.55"


def parse_homepage() -> Tuple[str, str]:
    """Parse homepage of 10.0.0.55 and get the acid + ip of current session

    Raises:
        Exception: Throw exception if acid not present in the redirected URL
        Exception: Throw exception if response text does not contain IP

    Returns:
        Tuple[str, str]: Both the ip and the acid of the current session
    """

    res = requests.get(API_BASE)

    # ac_id appears in the url query parameter of the redirected URL
    query = parse_qs(urlparse(res.url).query)
    ac_id = query.get("ac_id")

    if not ac_id:
        raise Exception("failed to get acid")

    # ip appears in the response HTML
    class IPParser(HTMLParser):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ip = None

        def handle_starttag(self, tag, attrs):
            if tag == "input":
                attr_dict = dict(attrs)
                if attr_dict.get("name") == "user_ip":
                    self.ip = attr_dict["value"]

        def feed(self, *args, **kwargs):
            super().feed(*args, **kwargs)
            return self.ip

    parser = IPParser()
    ip = parser.feed(res.text)

    if not ip:
        raise Exception("failed to get ip")

    return ip, ac_id[0]


def get_user_info() -> Tuple[bool, Optional[str]]:
    """Get current logged in user info if exists

    Returns:
        tuple[bool, Optional[str]]
        - a boolean indicating whether the current IP is logged in
        - the username of the current logged in user if exists
    """

    is_logged_in = True
    username = None

    resp = requests.get(API_BASE + "/cgi-bin/rad_user_info")
    data = resp.text

    if data == "not_online_error":
        is_logged_in = False
    else:
        username = data.split(",")[0]

    return is_logged_in, username


def fkbase64(raw_s: str) -> str:
    """Encode string with a magic base64 mask"""
    trans = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
        "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA",
    )
    ret = b64encode(bytes(ord(i) & 0xFF for i in raw_s))
    return ret.decode().translate(trans)


def xencode(msg, key) -> str:
    def sencode(msg, key):
        def ordat(msg, idx):
            if len(msg) > idx:
                return ord(msg[idx])
            return 0

        msg_len = len(msg)
        pwd = []
        for i in range(0, msg_len, 4):
            pwd.append(ordat(msg, i) | ordat(msg, i + 1) << 8 | ordat(msg, i + 2) << 16 | ordat(msg, i + 3) << 24)
        if key:
            pwd.append(msg_len)
        return pwd

    def lencode(msg, key) -> str:
        msg_len = len(msg)
        ll = (msg_len - 1) << 2
        if key:
            m = msg[msg_len - 1]
            if m < ll - 3 or m > ll:
                return ""
            ll = m
        for i in range(0, msg_len):
            msg[i] = chr(msg[i] & 0xFF) + chr(msg[i] >> 8 & 0xFF) + chr(msg[i] >> 16 & 0xFF) + chr(msg[i] >> 24 & 0xFF)
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
