from MiWifiSpeakerV3 import WifiSpeakerV3, LoopType
from time import sleep

my_cookie = {
    "userId": "2574549865",
    "deviceSNProfile": "eyJzaWduIjoiNzMzMDA4NzFmNDRjMTY4ZTdjOTQ5ZGUyYzc1MGU2MGMyYzliYjhmZjUzMDAxN2M1YTI2NzIzNGU5Y2I0ZGI4ZSIsInNuIjoiMTUwODcvNTYwMDE1NjQ4In0=",
    "sn": "15087/560015648",
    "deviceId": "6e8h7506-8d34-65df-c0d7-e19480s7d3b4",
    "serviceToken": "tJYUMjSdn6MHAaEJzdchU8XZVqkGnbmrT3n4hhQaIqrrAl9OwgyWGwEZohfPDUENSaQ/aPJF1JVaX32nwCaHAvOACyJ7aJW5g7hw+GYJ5SrKBqVN8XG0wjvPaFYpyQ3Ha8Oelx6IH8OxydiqNop98RTUnOxHLW9G7AkfowucoGiYRls8XbhqBL22q3lBVntfZ7EnEpXY6x9FaNGE0DQWVQ==",
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