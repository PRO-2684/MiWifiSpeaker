# MiWifispeaker
[English version](README.md)
## ðª åè½
æ§å¶å°ç±³ç½ç»é³ç®±æ­æ¾æ¬å°é³ä¹ðµã
## ð æ¬å°é³ä¹çç®¡ç
### ðª Windows
ç¡®ä¿çµèä¸é³ç®±**å¨åä¸å±åç½ä¸**ï¼ç³»ç»æä»¶ç®¡çå¨å°åæ è¾å¥ `\\<ip>` ï¼å¶ä¸­ `<ip>` ä¸ºé³ç®± ip å°åï¼å³å¯è®¿é®ãè¥åºç°éè¯¯ï¼è¯·å°è¯[å¯ç¨ SMBv1 å®¢æ·ç«¯](https://docs.microsoft.com/zh-cn/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3#smbv1-on-smb-client)ï¼è½ç¶å¨éå¸¸æåµä¸æä»¬[å¹¶ä¸å»ºè®®è¿ä¹å](https://techcommunity.microsoft.com/t5/storage-at-microsoft/stop-using-smb1/ba-p/425858)ã
### ð¤ å¶ä»ç³»ç»
ç¡®ä¿çµèä¸é³ç®±**å¨åä¸å±åç½ä¸**ï¼ä½¿ç¨ SMB å®¢æ·ç«¯è¿æ¥è³é³ç®± ip ï¼è¥éè¦æä¾ç¨æ·åï¼åå¡«å¥ `GUEST` ï¼å¯ç çç©ºãä½ å¯è½ä¹éè¦å¨æå¤å¯ç¨ SMBv1 ã
## ð© ç»å½
### ð ä½¿ç¨ç¨æ·idåå¯ç ç»å½
```python
wifi_speaker = WifiSpeakerV3('<å°ç±³id>', '<å¯ç >', '<åºåå·>')
# å¦æä½ æ¥æå¤ä¸ªç½ç»é³ç®±å¹¶ä¸æ³æå®ä½ è¦æ§å¶çç½ç»é³ç®±ï¼åºåå·æ¯å¿é¡»çã
# ä½ éå¸¸å¯ä»¥å¨é³ç®±åºé¨çå°åºåå·ã
```
### ðª ä½¿ç¨ Cookie ç»å½
1. ç¡®ä¿**å¯æ­£å¸¸æåææº/æ¨¡æå¨ç https å**ï¼å³ä½¿åºç¨ä¸ä¿¡ä»»ç¨æ·è¯ä¹¦ã*(å»ºè®®ä½¿ç¨å®å6åä»¥ä¸çæ¨¡æå¨ï¼éå Fiddler å®ç°æå)*
2. ææº/æ¨¡æå¨å®è£âå°ç±é³ç®±âAPP(`com.xiaomi.mico`)ã
3. æå¼æåè½¯ä»¶ï¼ç¡®è®¤å¯å·¥ä½åç»å½âå°ç±é³ç®±âè½¯ä»¶ã
4. å¨æåå°çæ°æ®åä¸­ï¼å¤å¶ä»»ä¸ååä¸º `api*.mina.mi.com` çè¯·æ±ç cookie ï¼ç¡®ä¿ cookie å«æ `userId`, `deviceSNProfile`, `sn`, `deviceId` å `serviceToken` å­æ®µãä»¥ä¸æ¯ä¸ä¸ªä¾å­ã
    ```
    userId=2574549865
	deviceSNProfile=eyJzaWduIjoiNzMzMDA4NzFmNDRjMTY4ZTdjOTQ5ZGUyYzc1MGU2MGMyYzliYjhmZjUzMDAxN2M1YTI2NzIzNGU5Y2I0ZGI4ZSIsInNuIjoiMTUwODcvNTYwMDE1NjQ4In0=
	sn=15087/560015648
	deviceId=6e8h7506-8d34-65df-c0d7-e19480s7d3b4
	serviceToken=tJYUMjSdn6MHAaEJzdchU8XZVqkGnbmrT3n4hhQaIqrrAl9OwgyWGwEZohfPDUENSaQ/aPJF1JVaX32nwCaHAvOACyJ7aJW5g7hw+GYJ5SrKBqVN8XG0wjvPaFYpyQ3Ha8Oelx6IH8OxydiqNop98RTUnOxHLW9G7AkfowucoGiYRls8XbhqBL22q3lBVntfZ7EnEpXY6x9FaNGE0DQWVQ==
    ```
5. è½¬æ¢ä¸º Python dict ï¼å³å¯å¼å§ä½¿ç¨ï¼
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
### ð¡ ç»åä»¥ä¸ä¸¤ç§æ¹æ³
å½ä½ ç»å½æååï¼ä¿å­ cookie ä»¥å¤ä»¥åä½¿ç¨ãä¸æ¬¡ä½¿ç¨èæ¬æ¶ï¼ä½ å°±å¯ä»¥ä½¿ç¨ä¿å­ç cookie ãå¦æ cookie è¿æï¼éæ°ç»å½å¹¶ä¿å­ cookie ã
Cookie å¯ä»¥éè¿ `WifiSpeakerV3.cookie` è·åã
ä¾å­ï¼
```python
from json import load, dump
try:
    with open('cookie') as f:
        wifi_speaker = WifiSpeakerV3(cookie=load(f))
        status = wifi_speaker.status
except:
    print('Refreshing cookie...')
    wifi_speaker = WifiSpeakerV3('<Mi id>', '<password>')
    status = wifi_speaker.status
    with open('cookie', 'w') as f:
        dump(wifi_speaker.cookie.get_dict(), f)
```
## ð ç¨æ³
ææ ææ¡£ï¼è¯·åè `demo.py`ã
## â æ¯æçåå·
> ä½ å¯ä»¥éè¿ [token extractor](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor) æ [`miiocli device --ip <ip_address> --token <token> info`](https://github.com/rytilahti/python-miio) ä»¥ç¡®å®ä½ çè®¾å¤çåå·ã
* `xiaomi.wifispeaker.v3`
## â ï¸ æ³¨æäºé¡¹
ææ ã
## ðï¸ Todo
* [x] æ·»å  `set_loop_type`ã
* [ ] æ·»å æ­æ¾åè¡¨ã
