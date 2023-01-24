import hmac
import json
from enum import Enum
from hashlib import sha1
from typing import Dict, Optional, Union

from requests import Session

from bitsrun.utils import fkbase64, parse_homepage, xencode

API_BASE = "http://10.0.0.55"
TYPE_CONST = 1
N_CONST = 200


class Action(Enum):
    LOGIN = "login"
    LOGOUT = "logout"


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        self.ip, self.acid = parse_homepage(api_base=API_BASE)
        self.session = Session()

    def login(self) -> Dict[str, Union[str, int]]:
        logged_in_user = self._user_validate()

        # Raise exception if device is already logged in
        if logged_in_user == self.username:
            raise Exception(f"{logged_in_user}, you are already online")

        return self._do_action(Action.LOGIN)

    def logout(self) -> Dict[str, Union[str, int]]:
        logged_in_user = self._user_validate()

        # Raise exception if device is not logged in
        if logged_in_user is None:
            raise Exception("you have already logged out")

        return self._do_action(Action.LOGOUT)

    def _do_action(self, action: Action) -> Dict[str, Union[str, int]]:
        params = self._make_params(action)
        response = self.session.get(API_BASE + "/cgi-bin/srun_portal", params=params)
        return json.loads(response.text[6:-1])

    def _get_user_info(self) -> Optional[str]:
        """Get current logged in user info if exists.

        Returns:
            The username of the current logged in user if exists.
        """

        resp = self.session.get(API_BASE + "/cgi-bin/rad_user_info")
        data = resp.text

        if data == "not_online_error":
            return None

        return data.split(",")[0]

    def _user_validate(self) -> Optional[str]:
        """Check if current logged in user matches the username provided.

        Raises:
            Exception: If current logged in user and username provided does not match.

        Returns:
            The username of the current logged in user if exists.
        """

        logged_in_user = self._get_user_info()

        # Raise exception only if username exists on this IP and
        # command line arguments provided another username
        if logged_in_user and logged_in_user != self.username:
            raise Exception(
                f"Current logged in user ({logged_in_user}) and "
                f"yours ({self.username}) does not match"
            )

        return logged_in_user

    def _get_token(self) -> str:
        params = {"callback": "jsonp", "username": self.username, "ip": self.ip}
        response = self.session.get(API_BASE + "/cgi-bin/get_challenge", params=params)
        result = json.loads(response.text[6:-1])
        return result["challenge"]

    def _make_params(self, action: Action) -> Dict[str, Union[int, str]]:
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
                token,
                self.username,
                hmd5,
                self.acid,
                self.ip,
                N_CONST,
                TYPE_CONST,
                info,
            ).encode()
        ).hexdigest()

        params.update({"password": "{MD5}" + hmd5, "chksum": chksum, "info": info})
        return params
