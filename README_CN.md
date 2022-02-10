# MiWifispeaker
[English version](README.md)
## 🪄 功能
控制小米网络音箱播放本地音乐🎵。
## 📁 本地音乐的管理
### 🪟 Windows
确保电脑与音箱**在同一局域网下**，系统文件管理器地址栏输入 `\\<ip>` ，其中 `<ip>` 为音箱 ip 地址，即可访问。若出现错误，请尝试[启用 SMBv1 客户端](https://docs.microsoft.com/zh-cn/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3#smbv1-on-smb-client)，虽然在通常情况下我们[并不建议这么做](https://techcommunity.microsoft.com/t5/storage-at-microsoft/stop-using-smb1/ba-p/425858)。
### 🤔 其他系统
确保电脑与音箱**在同一局域网下**，使用 SMB 客户端连接至音箱 ip ，若需要提供用户名，则填入 `GUEST` ，密码留空。你可能也需要在某处启用 SMBv1 。
## 🍪 Cookie 的获取
> 后续*可能*推出脚本以简化此流程。
1. 确保**可正常抓取手机/模拟器的 https 包**，即使应用不信任用户证书。*(建议使用安卓6及以下的模拟器，配合 Fiddler 实现抓包)*
2. 手机/模拟器安装“小爱音箱”APP(`com.xiaomi.mico`)。
3. 打开抓包软件，确认可工作后登录“小爱音箱”软件。
4. 在抓取到的数据包中，复制任一域名为 `api*.mina.mi.com` 的请求的 cookie ，确保 cookie 含有 `userId`, `deviceSNProfile`, `sn`, `deviceId` 和 `serviceToken` 字段。以下是一个例子。
    ```
    userId=2574549865
	deviceSNProfile=eyJzaWduIjoiNzMzMDA4NzFmNDRjMTY4ZTdjOTQ5ZGUyYzc1MGU2MGMyYzliYjhmZjUzMDAxN2M1YTI2NzIzNGU5Y2I0ZGI4ZSIsInNuIjoiMTUwODcvNTYwMDE1NjQ4In0=
	sn=15087/560015648
	deviceId=6e8h7506-8d34-65df-c0d7-e19480s7d3b4
	serviceToken=tJYUMjSdn6MHAaEJzdchU8XZVqkGnbmrT3n4hhQaIqrrAl9OwgyWGwEZohfPDUENSaQ/aPJF1JVaX32nwCaHAvOACyJ7aJW5g7hw+GYJ5SrKBqVN8XG0wjvPaFYpyQ3Ha8Oelx6IH8OxydiqNop98RTUnOxHLW9G7AkfowucoGiYRls8XbhqBL22q3lBVntfZ7EnEpXY6x9FaNGE0DQWVQ==
    ```
5. 转换为 Python dict ，即可开始使用！
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
## 📖 用法
暂无文档，请参考 `demo.py`。
## ✅ 支持的型号
> 你可以通过 [token extractor](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor) 或 [`miiocli device --ip <ip_address> --token <token> info`](https://github.com/rytilahti/python-miio) 以确定你的设备的型号。
* `xiaomi.wifispeaker.v3`
## ⚠️ 注意事项
暂无。
## 🗒️ Todo
* [ ] 添加 `set_loop_type`。
* [ ] 添加播放列表。