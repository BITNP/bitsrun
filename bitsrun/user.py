import hmac
import json
from hashlib import sha1
from typing import Optional

import httpx

from bitsrun.models import LoginStatusRespType, UserResponseType
from bitsrun.utils import fkbase64, xencode

_API_BASE = "http://10.0.0.55"
_TYPE_CONST = 1
_N_CONST = 200


def get_login_status(client: Optional[httpx.Client] = None) -> LoginStatusRespType:
    """Get current login status of the device.

    Note:
        This function is also used without initializing a `User` instance. As such,
        the `client` argument is optional and will be initialized if not provided.

    Args:
        client: An optional reused httpx client if provided. Defaults to None.

    Returns:
        The login status of the current device. If the device is logged in, the
        `user_name` field will be present. Otherwise, it will be `None`. As such,
        the presence of `user_name` is used to check if the device is logged in.
    """

    if not client:
        client = httpx.Client(base_url=_API_BASE)

    resp = client.get("/cgi-bin/rad_user_info", params={"callback": "jsonp"})
    return json.loads(resp.text[6:-1])


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        # Initialize reused httpx client
        self.client = httpx.Client(base_url=_API_BASE)

        # Get `ac_id` from the redirected login page
        resp = self.client.get("/", follow_redirects=True)
        self.acid = resp.url.params.get("ac_id")

        # Check current login status and get device `online_ip`
        login_status = get_login_status(client=self.client)
        self.ip = login_status.get("online_ip")
        self.logged_in_user = login_status.get("user_name")

        # Validate if current logged in user matches the provided username
        if self.logged_in_user and self.logged_in_user != self.username:
            raise Exception(
                f"Current logged in user ({self.logged_in_user}) and "
                f"yours ({self.username}) does not match"
            )

    def login(self) -> UserResponseType:
        # Raise exception if device is already logged in
        if self.logged_in_user == self.username:
            raise Exception(f"{self.logged_in_user}, you are already online")

        # Get challenge token for login authentication
        token = self._get_token()

        # Prepare params for login request
        params = {
            "callback": "jsonp",
            "username": self.username,
            "action": "login",
            "ac_id": self.acid,
            "ip": self.ip,
            "type": _TYPE_CONST,
            "n": _N_CONST,
        }

        # Encode login data and generate checksum
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
                _N_CONST,
                _TYPE_CONST,
                info,
            ).encode()
        ).hexdigest()

        # Update params with login data, checksum, and encrypted password
        params.update({"password": "{MD5}" + hmd5, "chksum": chksum, "info": info})

        response = self.client.get("/cgi-bin/srun_portal", params=params)
        return json.loads(response.text[6:-1])

    def logout(self) -> UserResponseType:
        # Raise exception if device is not logged in
        if self.logged_in_user is None:
            raise Exception("you have already logged out")

        # Logout params contain only the following fields
        params = {
            "callback": "jsonp",
            "action": "logout",
            "ac_id": self.acid,
            "ip": self.ip,
            "username": self.username,
        }
        response = self.client.get("/cgi-bin/srun_portal", params=params)
        return json.loads(response.text[6:-1])

    def _get_token(self) -> str:
        """Get challenge token for login authentication."""
        params = {"callback": "jsonp", "username": self.username, "ip": self.ip}
        response = self.client.get("/cgi-bin/get_challenge", params=params)
        result = json.loads(response.text[6:-1])
        return result["challenge"]
