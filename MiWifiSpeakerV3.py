from requests import Session
from random import choice
from string import ascii_letters, digits
from json import loads
from enum import Enum
from base64 import b64encode
from hashlib import md5,sha1
from urllib.parse import quote


URL = "https://api2.mina.mi.com/remote/ubus"
STRING = ascii_letters + digits
RETRY = 3


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

    def __init__(self, info: dict):
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
        self.song_path = info["play_song_detail"]["title"][20:]

    def __str__(self):
        return f'<{self.__class__.__name__}: play_status={self.play_status} loop_type={self.loop_type} volumn={self.volume}% duration={self.duration}ms position={self.position}ms song_path="{self.song_path}">'


class WifiSpeakerV3:
    """Main class representing `xiaomi.wifispeaker.v3` device."""

    def __init__(self, user_id: str='', password: str='', sn: str='', cookie: dict=None) -> None:
        """You can either pass `cookie` or pass `user_id` and `password` (and `sn` if you have multiple wifispeakers in ordr to specify).  
        If you prefer cookie, note that it should contain `userId`, `deviceSNProfile`, `sn`, `deviceId` and `serviceToken`."""
        self.logined = False
        self._session = Session()
        self._session.headers = {
            "User-Agent": "MICO/AndroidApp/@SHIP.TO.2A2FE0D7@/2.4.14",
            "Accept-Encoding": "gzip",
        }
        self.device_id = ''
        if cookie:
            self._session.cookies.update(cookie)
            self.device_id = cookie["deviceId"]
            self.logined = True
        elif user_id and password:
            assert self._login(user_id=user_id, password=password), 'Login failed!'
            r = self._session.get(
                'https://api2.mina.mi.com/admin/v2/device_list',
                params={
                    'requestId': generate_request_id()
                }
            ).json()
            assert r['code'] == 0, 'Fetching device list failed!'
            device_list = r['data']
            if not sn:
                device = device_list[0]
                self.device_id = device['deviceID']
                sn = device['serialNumber']
            else:
                for d in device_list:
                    if d['serialNumber'] == sn:
                        device = d
                        self.device_id = d['deviceID']
                        break
                assert self.device_id, f'Device with sn {sn} not found!'
            cookie = {
                'userId': user_id,
                'deviceSNProfile': device['deviceSNProfile'],
                'sn': sn,
                'deviceId': self.device_id,
                'serviceToken': self.cookie.get('serviceToken'),
            }
            self.cookie.clear()
            self.cookie.update(cookie)
            self.logined = True


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
        if r.status_code == 401:
            raise PermissionError('Cookie expired!')
        return r

    def _login(self, user_id: str, password: str) -> bool:
        """`user_id` should be your Mi id, not phone number."""
        r = self._session.post(
            'https://account.xiaomi.com/pass/serviceLoginAuth2',
            params={
                '_json': True,
                'sid': 'micoapi',
                'locale': 'zh_CN',
                'user': user_id,
                'hash': md5(password.encode()).hexdigest().upper()
            }
        )
        json = loads(r.text[11:])
        if json['code']:
            return False
        clientSign = f"nonce={json['nonce']}&{json['ssecurity']}"
        clientSign = sha1(clientSign.encode('utf-8')).digest()
        clientSign = quote(b64encode(clientSign).decode())
        r = self._session.get(json['location'] + '&clientSign=' + clientSign)
        return 'OK' in r.text

    def send_raw_command(self, method: str, message: str) -> bool:
        assert self.logined, 'Not logined!'
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
        assert data["code"] == 0 and data["data"]["code"] == 0, (
            "Failed to fetch device status. Response: " + r.text
        )
        return WifiSpeakerV3Status(
            loads(data["data"]["info"])
        )

    @property
    def countdown(self) -> int:
        """Get countdown timer, 0 if none.  
        Unit: milliseconds(ms)."""
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
        assert countdown["code"] == 0 and countdown["data"]["code"] == 0, (
            "Failed to fetch countdown status. Response: " + r.text
        )
        countdown = countdown['data']['info']
        return countdown['remain_time'] if countdown['type'] else 0

    @property
    def cookie(self):
        """Returns current cookie."""
        return self._session.cookies

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
        """If playing, then pause; if paused, then resume."""
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
