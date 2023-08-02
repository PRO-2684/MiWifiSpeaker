from MiWifiSpeakerV3 import WifiSpeakerV3, LoopType
from time import sleep

my_cookie = {
    "userId": "*",
    "deviceSNProfile": "*",
    "sn": "*",
    "deviceId": "*",
    "serviceToken": "*",
}
wifi_speaker = WifiSpeakerV3(my_cookie)
print(wifi_speaker.status)
music_path = "Afterglow.mp3"
assert wifi_speaker.play(music_path)
sleep(5)
music_path = '/'
assert wifi_speaker.play(music_path)
status = wifi_speaker.status
print(status)
assert wifi_speaker.set_volume(10)
assert wifi_speaker.set_loop_type(LoopType.Random)
assert wifi_speaker.set_countdown(100)
assert wifi_speaker.pause()
status = wifi_speaker.status
print(status)
print("Sleeping...")
sleep(5)
assert wifi_speaker.play()
sleep(5)
status = wifi_speaker.status
assert wifi_speaker.set_position(int(0.5 * status.duration))
sleep(5)
status = wifi_speaker.status
print(status)
assert wifi_speaker.pause()
