import hmac
import json
from hashlib import sha1
from typing import Dict, Union

from requests import Session

from .action import Action
from .exception import AlreadyLoggedOutException, AlreadyOnlineException, UsernameUnmatchedException
from .utils import fkbase64, get_user_info, parse_homepage, xencode

API_BASE = "http://10.0.0.55"
TYPE_CONST = 1
N_CONST = 200


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        self.ip, self.acid = parse_homepage()
        self.session = Session()

    def do_action(self, action: Action) -> Dict[str, Union[str, int]]:
        # Check current state - whether device is logged in and whether current user the same as the provided one
        is_logged_in, username = get_user_info()

        if is_logged_in and action is Action.LOGIN:
            raise AlreadyOnlineException(f"{username}, you are already online")
        if not is_logged_in and action is Action.LOGOUT:
            raise AlreadyLoggedOutException("you have already logged out")

        # Raise exception only if username exists on this IP and command line arguments provided another username
        if username and username != self.username:
            raise UsernameUnmatchedException(
                f"current logged in user {username} and provided username {self.username} does not match"
            )

        # Perform login or logout action
        params = self._make_params(action)
        response = self.session.get(API_BASE + "/cgi-bin/srun_portal", params=params)
        return json.loads(response.text[6:-1])

    def _get_token(self) -> str:
        params = {"callback": "jsonp", "username": self.username, "ip": self.ip}
        response = self.session.get(API_BASE + "/cgi-bin/get_challenge", params=params)
        result = json.loads(response.text[6:-1])
        return result["challenge"]

    def _make_params(self, action: Action) -> Dict[str, str]:
        token = self._get_token()

        params = {
            "callback": "jsonp",
            "username": self.username,
            "action": action.value,
            "ac_id": self.acid,
            "ip": self.ip,
            "type": TYPE_CONST,
            "n": N_CONST,
        }

        data = {
            "username": self.username,
            "password": self.password,
            "acid": self.acid,
            "ip": self.ip,
            "enc_ver": "srun_bx1",
        }

        hmd5 = hmac.new(token.encode(), b"", "MD5").hexdigest()
        json_data = json.dumps(data, separators=(",", ":"))
        info = "{SRBX1}" + fkbase64(xencode(json_data, token))
        chksum = sha1(
            "{0}{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}".format(
                token, self.username, hmd5, self.acid, self.ip, N_CONST, TYPE_CONST, info
            ).encode()
        ).hexdigest()

        params.update({"password": "{MD5}" + hmd5, "chksum": chksum, "info": info})
        return params
