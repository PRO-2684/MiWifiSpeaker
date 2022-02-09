from requests import Session
from random import choice
from string import ascii_letters, digits
from json import loads
from enum import Enum
from base64 import b64encode

URL = "https://api2.mina.mi.com/remote/ubus"
STRING = ascii_letters + digits


def generate_request_id():
    s = ""
    for _ in range(20):
        s += choice(STRING)
    return s


class WifiSpeakerV3:
    """Main class representing `xiaomi.wifispeaker.v3` device."""

    def __init__(self, cookie: dict, local_ip: str = None) -> None:
        """`cookie` should contain `userId`, `deviceSNProfile`, `sn`, `deviceId` and `serviceToken`.

        `local_ip` is needed for listing directories."""
        self._session = Session()
        self._session.headers = {
            "User-Agent": "MICO/AndroidApp/@SHIP.TO.2A2FE0D7@/2.4.14",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "api2.mina.mi.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        self._session.cookies.update(cookie)
        self.device_id = cookie["deviceId"]
        self.local_ip = local_ip

    @property
    def status(self):
        """Get current status."""
        r = self._session.post(
            URL,
            params={
                "deviceId": self.device_id,
                "path": "mediaplayer",
                "method": "player_get_play_status",
                "message": "{}",
                "requestId": generate_request_id(),
            },
        )
        data = r.json()
        assert data["code"] == 0 and data["data"]["code"] == 0, (
            "Failed to fetch status. Response: " + r.text
        )
        return WifiSpeakerV3Status(loads(data["data"]["info"]))

    def play(self, local_path: str = "") -> bool:
        """Plays the given song at `local_path`. If `local_path` is empty, the song previously played is resumed."""
        if not local_path:
            r = self._session.post(
                URL,
                params={
                    "deviceId": self.device_id,
                    "path": "mediaplayer",
                    "method": "player_play_operation",
                    "message": '{"action":"play","media":"app_android"}',
                    "requestId": generate_request_id(),
                },
            ).json()
            return r["code"] == 0 and r["data"]["code"] == 0
        local_path = local_path.replace("\\", "/")
        local_path = local_path.replace("//", "/")
        if local_path.startswith("./"):
            local_path = local_path[1:]
        elif not local_path.startswith("/"):
            local_path = "/" + local_path
        r = self._session.post(
            URL,
            params={
                "deviceId": self.device_id,
                "path": "mediaplayer",
                "method": "player_play_filepath",
                "message": f'{{"name":"media","path":"{local_path}","nameBase64":"bWVkaWE=","pathBase64":"{b64encode(local_path.encode()).decode()}"}}',
                "requestId": generate_request_id(),
            },
        ).json()
        return r["code"] == 0 and r["data"]["code"] == 0

    def pause(self) -> bool:
        """Pause the song currently playing."""
        r = self._session.post(
            URL,
            params={
                "deviceId": self.device_id,
                "path": "mediaplayer",
                "method": "player_play_operation",
                "message": '{"action":"pause","media":"app_android"}',
                "requestId": generate_request_id(),
            },
        ).json()
        return r["code"] == 0 and r["data"]["code"] == 0


class WifiSpeakerV3Status:
    """Main class representing `xiaomi.wifispeaker.v3` status."""

    def __init__(self, info: dict):
        self._info = info
        self.play_status = PlayStatus(info["status"])
        self.volume = info["volume"]
        self.loop_type = LoopType(info["loop_type"])
        self.song_path = info["play_song_detail"]["title"][21:]

    def __str__(self):
        return f'<{self.__class__.__name__}: play_status={self.play_status} loop_type={self.loop_type} volumn={self.volume} song_path="{self.song_path}">'


class PlayStatus(Enum):
    Unknown = 0
    Playing = 1
    Paused = 2


class LoopType(Enum):
    Single = 0
    Ordered = 1
    Unknown = 2
    Random = 3
