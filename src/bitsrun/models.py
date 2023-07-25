from typing import Literal, Optional, TypedDict, Union


class UserResponseType(TypedDict):
    client_ip: str
    online_ip: str
    # Field `error` is also `login_error` when logout action fails
    error: Union[Literal["login_error"], Literal["ok"]]
    error_msg: str
    res: Union[Literal["login_error"], Literal["ok"]]
    # Field `username` is not present on login fails and all logout scenarios
    username: Optional[str]


class LoginStatusRespType(TypedDict):
    # Field `error` is `not_online_error` when device is not logged in
    error: str
    client_ip: Optional[str]
    # Field `online_ip` is always present regardless of login status
    online_ip: str
    # Below are fields only present when device is logged in
    sum_bytes: Optional[int]
    sum_seconds: Optional[int]
    user_balance: Optional[int]
    user_name: Optional[str]
    wallet_balance: Optional[int]
