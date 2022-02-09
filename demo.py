from MiWifiSpeakerV3 import WifiSpeakerV3
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
music = "Afterglow.mp3"
if wifi_speaker.play(music):
    print(f'Play "{music}" success!')
else:
    print(f'Failed to play "{music}".')
sleep(5)
status = wifi_speaker.status
print(
    f"""Status: "{status.song_path}" {status.play_status.name}
Loop: {status.loop_type.name}
Volume: {status.volume}%
Progress: {status.position / status.duration:.2f}%"""
)
wifi_speaker.set_volume(10)
if wifi_speaker.pause():
    print("Pause success!")
else:
    print("Failed to pause.")
status = wifi_speaker.status
print(
    f"""Status: "{status.song_path}" {status.play_status.name}
Loop: {status.loop_type.name}
Volume: {status.volume}%
Progress: {status.position / status.duration:.2f}%"""
)
print("Sleeping...")
sleep(5)
if wifi_speaker.play():
    print("Resumn success!")
else:
    print("Failed to resume.")
sleep(5)
status = wifi_speaker.status
if wifi_speaker.set_position(int(0.5 * status.duration)):
    print("Set position success!")
else:
    print("Failed to set position.")
sleep(5)
status = wifi_speaker.status
print(
    f"""Status: "{status.song_path}" {status.play_status.name}
Loop: {status.loop_type.name}
Volume: {status.volume}%
Progress: {status.position / status.duration:.2f}%"""
)
print("Pausing...")
sleep(5)
wifi_speaker.pause()
