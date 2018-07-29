#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Aloxaf
# 2018.7.27

# 北理工校园网自动登录

import hmac
import json
from hashlib import sha1
from requests import Session
from support import xencode, get_host_ip, fkbase64

class User:
    """登录校园网"""
    # some magic number
    n = 200
    acid = "1"
    _type = 1
    api = 'http://10.0.0.55/cgi-bin'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.ip = get_host_ip()
        self.ses = Session()

    def get_token(self):
        """获取token"""
        params = {
            'callback': 'jsonp',
            'username': self.username,
            'ip': self.ip,
        }
        res = self.ses.get(f'{self.api}/get_challenge', params=params).text
        ret = json.loads(res[6:-1])
        return ret['challenge']

    def make_params(self, action):
        """生成需要提交的参数"""
        token = self.get_token()
        params = {
            'callback': 'jsonp',
            'username': self.username,
            'action': action,
            'ac_id': self.acid,
            'type': self._type,
            'ip': self.ip,
            'n': self.n,
        }
        data = {
            'username': self.username,
            'password': self.password,
            'acid': self.acid,
            'ip': self.ip,
            'enc_ver': 'srun_bx1',
        }
        hmd5 = hmac.new(token.encode(), b'').hexdigest()
        _json = json.dumps(data, separators=(',', ':'))
        info = '{SRBX1}' + fkbase64(xencode(_json, token))
        chksum = sha1('{0}{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}'.format(
            token, self.username, hmd5, self.acid, self.ip, self.n,
            self._type, info
        ).encode()).hexdigest()
        params.update({
            'password': '{MD5}' + hmd5,
            'chksum': chksum,
            'info': info,
        })

        return params

    def login(self):
        """登录"""
        params = self.make_params("login")
        res = self.ses.get(f'{self.api}/srun_portal', params=params).text
        return json.loads(res[6:-1])

    def logout(self):
        """注销"""
        params = self.make_params("logout")
        res = self.ses.get(f'{self.api}/srun_portal', params=params).text
        return json.loads(res[6:-1])

def main():
    """从命令行启动"""
    from sys import argv
    from pprint import pprint
    config = json.load(open('./config.json'))
    username, password = config['username'], config['password']

    user = User(username, password)
    
    if len(argv) == 1 or argv[1] == 'login':
        pprint(user.login())
    elif argv[1] == 'logout':
        pprint(user.logout())

if __name__ == '__main__':
    main()
