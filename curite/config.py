from dataclasses import dataclass
from lib2to3.pgen2 import token
from re import compile as re_compile
from typing import Pattern, Tuple

import yaml


@dataclass
class Config:
    server: Tuple[str, int, bool]
    nickname: str
    password: str
    nickserv_name: str
    httpd_port: int
    unix_socket_path: str

    url_success: str
    url_failure: str

    account_re: str
    token_re: str


def load(filepath: str):
    with open(filepath) as file:
        config_yaml = yaml.safe_load(file.read())

    nickname = config_yaml["nickname"]
    server = config_yaml["server"]
    hostname, port_s = server.split(":", 1)
    tls = False

    if port_s.startswith("+"):
        tls = True
        port_s = port_s.lstrip("+")
    port = int(port_s)

    return Config(
        server=(hostname, port, tls),
        nickname=nickname,
        password=config_yaml["password"],
        nickserv_name=config_yaml.get("nickserv-name", "NickServ"),
        httpd_port=config_yaml.get("httpd-port", -1),
        unix_socket_path=config_yaml.get("unix-socket-path", ""),
        url_success=config_yaml["url-success"],
        url_failure=config_yaml["url-failure"],
        account_re=config_yaml.get("account-re", r"[^/]+"),
        token_re=config_yaml.get("token-re", r"[^/]+"),
    )
