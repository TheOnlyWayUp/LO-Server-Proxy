"""Module to make interfacing with the configuration easier."""

import os, json, requests
from typing import List, cast, Dict, Union
from enum import Enum
from mcstatus import JavaServer

PROXY_CONFIG_PATH = os.getenv("PROXY_CONFIG_PATH")
assert (
    PROXY_CONFIG_PATH
), "Set the PROXY_CONFIG_PATH Environment Variable before running."
with open(PROXY_CONFIG_PATH) as config_file:
    config = json.load(config_file)

_PROXY_CONFIG = config["proxy"]
_API_CONFIG = config["api"]

BIND_ADDRESS = _PROXY_CONFIG["bind"]["address"]
BIND_PORT = _PROXY_CONFIG["bind"]["port"]

SERVER_ADDRESS = _PROXY_CONFIG["proxy_to"]["address"]
SERVER_PORT = _PROXY_CONFIG["proxy_to"]["port"]

PROXY_API_ADDRESS = _API_CONFIG["bind"]["address"]
PROXY_API_PORT = _API_CONFIG["bind"]["port"]

PLAYER_API_BASE_URL = os.environ["PLAYER_API_URL"]
STATS_API_BASE_URL = os.environ["STATS_API_URL"]
CONFG_API_BASE_URL = os.environ["DISCORD_BOT_URL"]
API_AUTH_KEY = os.environ["API_AUTH_KEY"]

UUID_TO_USERNAME_URL = "https://sessionserver.mojang.com/session/minecraft/profile/{}"
USERNAME_TO_UUID_URL = "https://api.mojang.com/users/profiles/minecraft/{}"

headers = {"authorization": API_AUTH_KEY}

# Commented out | This is going to be made a function
# while True:
#     try:
#         MAX_CONTROLLED_PLAYERS = requests.get(
#             PLAYER_API_BASE_URL + "/maxlen", headers=headers
#         ).json()["MAX_SIZE"]
#         break
#     except:
#         time.sleep(5)

MOTD = "LiveOverflow Proxy"

# Server MOTD is also going to be made a function
SERVER_MOTD = cast(
    Dict, JavaServer(SERVER_ADDRESS, SERVER_PORT).status().raw.get("description", {})
).get("text", "")


class ProxyModeEnum(Enum):
    """Enum to store valid Proxy Modes."""

    whitelist = 1
    blacklist = 2


def get_proxy_mode():
    """Request Configuration API for Proxy Mode."""
    return (
        requests.get(CONFG_API_BASE_URL + "/mode", headers=headers)
        .text.replace('"', "")
        .replace("'", "")
    )


def convert_uuid_to_username(uuid: str) -> Union[str, None]:
    """Convert a UUID to a Username through the Mojang API."""
    resp = requests.get(UUID_TO_USERNAME_URL.format(uuid))
    return resp.json().get("name", None)


def convert_username_to_uuid(username: str) -> Union[str, None]:
    """Convert a Username to a UUID through the Mojang API."""
    resp = requests.get(USERNAME_TO_UUID_URL.format(username))
    return resp.json().get("id", None)


def get_player_list() -> List[str]:
    """Request the Congfiguration API for the Player List. Returns a list of UUIDs."""
    return requests.get(CONFG_API_BASE_URL + "/players", headers=headers).json()
