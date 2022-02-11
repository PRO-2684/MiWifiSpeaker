from requests import Session
from random import choice
from string import ascii_letters, digits
from json import loads
from enum import Enum
from base64 import b64encode
from typing import Union

URL = "https://api2.mina.mi.com/remote/ubus"
STRING = ascii_letters + digits
RETRY = 3
DEBUG = 0
if DEBUG:
    from rich import print_json


def generate_request_id():
    s = ""
    for _ in range(20):
        s += choice(STRING)
    return s


class PlayStatus(Enum):
    Stopped = 0
    Playing = 1
    Paused = 2


class LoopType(Enum):
    Single = 0
    Ordered = 1
    # Unknown = 2
    Random = 3


class WifiSpeakerV3Status:
    """Main class representing `xiaomi.wifispeaker.v3` status."""

    def __init__(self, info: dict, countdown: dict):
        self._info = info
        if info['media_type'] != 3:
            raise TypeError('Unsupported media type. Try manually play a song and then restart the script.')
            # Known media types
            # 3: music
            # 13: video
        self.play_status = PlayStatus(info["status"])
        self.loop_type = LoopType(info["loop_type"])
        self.volume = info["volume"]
        self.duration = info["play_song_detail"]["duration"]
        self.position = info["play_song_detail"]["position"]
        self.countdown = countdown["remain_time"] if countdown["type"] == 1 else 0
        self.song_path = info["play_song_detail"]["title"][20:]

    def __str__(self):
        return f'<{self.__class__.__name__}: play_status={self.play_status} loop_type={self.loop_type} volumn={self.volume}% duration={self.duration}ms position={self.position}ms countdown={self.countdown}s song_path="{self.song_path}">'


class WifiSpeakerV3:
    """Main class representing `xiaomi.wifispeaker.v3` device."""

    def __init__(self, cookie: dict) -> None:
        """`cookie` should contain `userId`, `deviceSNProfile`, `sn`, `deviceId` and `serviceToken`. Note that `serviceToken` can change frequently."""
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

    def _post(self, *args, **kwargs):
        flag = False
        for _ in range(RETRY):
            try:
                r = self._session.post(*args, **kwargs)
            except:
                pass
            finally:
                flag = True
        assert flag, f"Post failed after {RETRY} retries."
        return r

    def send_raw_command(self, method: str, message: str) -> bool:
        r = self._post(
            URL,
            params={
                "deviceId": self.device_id,
                "path": "mediaplayer",
                "method": method,
                "message": message,
                "requestId": generate_request_id(),
            },
        ).json()
        if DEBUG:
            print(method, message)
            print_json(data=r)
        return r["code"] == 0 and r["data"]["code"] == 0

    @property
    def status(self) -> WifiSpeakerV3Status:
        """Get current status."""
        r = self._post(
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
        if DEBUG:
            print('self.status, #1')
            print_json(data=data)
        assert data["code"] == 0 and data["data"]["code"] == 0, (
            "Failed to fetch device status. Response: " + r.text
        )
        r = self._post(
            URL,
            params={
                "deviceId": self.device_id,
                "path": "mediaplayer",
                "method": "get_shutdown_timer",
                "message": "{}",
                "requestId": generate_request_id(),
            },
        )
        countdown = r.json()
        if DEBUG:
            print('self.status, #2')
            print_json(data=countdown)
        assert countdown["code"] == 0 and countdown["data"]["code"] == 0, (
            "Failed to fetch countdown status. Response: " + r.text
        )
        return WifiSpeakerV3Status(
            loads(data["data"]["info"]), loads(countdown["data"]["info"])
        )

    def play(self, local_path: str = "") -> bool:
        """Plays the given song/folder at `local_path`. If `local_path` is empty, the song previously paused is resumed."""
        if not local_path:
            return self.send_raw_command(
                "player_play_operation", '{"action":"play","media":"app_android"}'
            )
        local_path = local_path.replace("\\", "/")
        local_path = local_path.replace("//", "/")
        if local_path.startswith("./"):
            local_path = local_path[1:]
        elif not local_path.startswith("/"):
            local_path = "/" + local_path
        return self.send_raw_command(
            "player_play_filepath",
            f'{{"name":"media","path":"{local_path}","nameBase64":"bWVkaWE=","pathBase64":"{b64encode(local_path.encode()).decode()}"}}',
        )

    def pause(self) -> bool:
        """Pause the song currently playing."""
        return self.send_raw_command(
            "player_play_operation", '{"action":"pause","media":"app_android"}'
        )

    def toggle(self) -> bool:
        """If playing, then pause; if paused, then play."""
        return self.send_raw_command(
            "player_play_operation", '{"action":"toggle","media":"app_android"}'
        )

    def next_song(self) -> bool:
        """Go to the next song."""
        return self.send_raw_command(
            "player_play_operation", '{"action":"next","media":"app_android"}'
        )

    def prev_song(self) -> bool:
        """Go to the previous song."""
        return self.send_raw_command(
            "player_play_operation", '{"action":"prev","media":"app_android"}'
        )

    def set_volume(self, volume: int) -> bool:
        """Set device volume. `volumn` should be between 1 and 100.
        Unit: percentage(%)."""
        assert 1 <= volume <= 100, "Volume should be between 1 and 100."
        return self.send_raw_command(
            "player_set_volume", f'{{"volume":{volume},"media":"app_android"}}'
        )

    def set_position(self, position: int) -> bool:
        """Set song position.
        Unit: milliseconds(ms)."""
        assert position >= 0, f"Position must be positive."
        # They seemed to have made a spelling mistake...
        return self.send_raw_command(
            "player_set_positon", f'{{"position":{position},"media":"app_android"}}'
        )

    def set_loop_type(self, loop_type: LoopType) -> bool:
        """Set loop type."""
        return self.send_raw_command(
            "player_set_loop", f'{{"media":"app_android","type":{loop_type.value}}}'
        )

    def set_countdown(self, seconds: int) -> bool:
        """After `seconds`, pause the music. If `seconds == 0`, cancel the timer.
        Unit: seconds(s)."""
        if seconds > 0:
            return self.send_raw_command(
                "player_set_shutdown_timer",
                f'{{"action":"pause_later","second":{seconds % 60},"minute":{seconds % 3600 // 60},"hour":{seconds // 3600}}}',
            )
        elif seconds == 0:
            return self.send_raw_command(
                "player_set_shutdown_timer", '{"action":"cancel_ending"}'
            )
        else:
            raise ValueError("Countdown time should be positive!")
