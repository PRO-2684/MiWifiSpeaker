# MiWifispeaker
[中文文档](README_CN.md)
## 🪄 Function
Control Xiaomi wifispeaker to play local musics🎵.
## 📁 Managing local musics
### 🪟 Windows
Ensure your computer and wifispeaker are **under the same LAN**, input `\\<ip>` on the address bar of explorer, where `<ip>` ip refers to the ip address of your wifispeaker, and press enter to access. If you encounter an error, you can try to [enable SMBv1 client](https://docs.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3#smbv1-on-smb-client), although it's [not recommend to do so](https://techcommunity.microsoft.com/t5/storage-at-microsoft/stop-using-smb1/ba-p/425858).
### 🤔 Other systems
Ensure your computer and wifispeaker are **under the same LAN**, and use a SMB client to connect to your wifispeaker. If a username is required, use `GUEST`, and leave the password blank. You may also need to enable SMB(v)1 somewhere.
## 🍪 Acquiring cookies
> A script *may* be developed to simplify this process.
1. Ensure you **can capture https traffic on your phone/emulator**, even when apps don't trust user certificates.*(Emulator of Android 6 and below, together with Fiddler is recommended)*
2. Install "小爱音箱" APP (`com.xiaomi.mico`).
3. Open your packet capture software, ensure it works and then login in your Mi account on the APP.
4. Among the packets you captured, copy any cookie of a request that has the domain `api*.mina.mi.com`, and ensure the cookie contains `userId`, `deviceSNProfile`, `sn`, `deviceId` and `serviceToken` field. An example is shown below.
    ```
    userId=2574549865
	deviceSNProfile=eyJzaWduIjoiNzMzMDA4NzFmNDRjMTY4ZTdjOTQ5ZGUyYzc1MGU2MGMyYzliYjhmZjUzMDAxN2M1YTI2NzIzNGU5Y2I0ZGI4ZSIsInNuIjoiMTUwODcvNTYwMDE1NjQ4In0=
	sn=15087/560015648
	deviceId=6e8h7506-8d34-65df-c0d7-e19480s7d3b4
	serviceToken=tJYUMjSdn6MHAaEJzdchU8XZVqkGnbmrT3n4hhQaIqrrAl9OwgyWGwEZohfPDUENSaQ/aPJF1JVaX32nwCaHAvOACyJ7aJW5g7hw+GYJ5SrKBqVN8XG0wjvPaFYpyQ3Ha8Oelx6IH8OxydiqNop98RTUnOxHLW9G7AkfowucoGiYRls8XbhqBL22q3lBVntfZ7EnEpXY6x9FaNGE0DQWVQ==
    ```
5. Convert it to Python dict, and start coding!
    ```python
    my_cookie = {
        'userId': '2574549865',
        'deviceSNProfile': 'eyJzaWduIjoiNzMzMDA4NzFmNDRjMTY4ZTdjOTQ5ZGUyYzc1MGU2MGMyYzliYjhmZjUzMDAxN2M1YTI2NzIzNGU5Y2I0ZGI4ZSIsInNuIjoiMTUwODcvNTYwMDE1NjQ4In0=',
        'sn': '15087/560015648',
        'deviceId': '6e8h7506-8d34-65df-c0d7-e19480s7d3b4',
        'serviceToken': 'tJYUMjSdn6MHAaEJzdchU8XZVqkGnbmrT3n4hhQaIqrrAl9OwgyWGwEZohfPDUENSaQ/aPJF1JVaX32nwCaHAvOACyJ7aJW5g7hw+GYJ5SrKBqVN8XG0wjvPaFYpyQ3Ha8Oelx6IH8OxydiqNop98RTUnOxHLW9G7AkfowucoGiYRls8XbhqBL22q3lBVntfZ7EnEpXY6x9FaNGE0DQWVQ=='
    }
    wifi_speaker = WifiSpeakerV3(my_cookie)
    ```
## 📖 Usage
No documentations yet. Please refer to `demo.py`.
## ✅ Supported models
> You can use [token extractor](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor) or [`miiocli device --ip <ip_address> --token <token> info`](https://github.com/rytilahti/python-miio) to determine the model of your wifispeaker.
* `xiaomi.wifispeaker.v3`
## ⚠️ Attention
Noting here yet.
## 🗒️ Todo
* [ ] Add `set_loop_type`.