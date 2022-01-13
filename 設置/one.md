
## 系統重新安裝
## 預設密碼更改
## 更新套件

[參考](http://angeloeyez.blogspot.com/2019/09/blog-post_19.html)

sudo apt-get update #更新套件清單

sudo apt-get upgrade #更新套件 

sudo rpi-update #更新韌體(非必要，如使用請先備份)

因套件找不到部分檔案改用手動下載更新

[參考](https://help.ubuntu.com/kubuntu/desktopguide/zh_TW/manual-install.html)

[base-files_10.3+rpi1+deb10u11_armhf.deb](http://raspbian.raspberrypi.org/raspbian/pool/main/b/base-files/base-files_10.3+rpi1+deb10u11_armhf.deb)

[libwebkit2gtk-4.0-37_2.32.4-1~deb10u1+rpi1_armhf.deb](http://raspbian.raspberrypi.org/raspbian/pool/main/w/webkit2gtk/libwebkit2gtk-4.0-37_2.32.4-1~deb10u1+rpi1_armhf.deb)

[libjavascriptcoregtk-4.0-18_2.32.4-1~deb10u1+rpi1_armhf.deb](http://raspbian.raspberrypi.org/raspbian/pool/main/w/webkit2gtk/libjavascriptcoregtk-4.0-18_2.32.4-1~deb10u1+rpi1_armhf.deb)

sudo wget + 網址 #下載到當前目錄

sudo dpkg -i 軟體套件名.deb #安裝套件

sudo apt-get --purge remove + 檔名 #刪除套件檔案

再執行一次sudo apt-get upgrade

sudo reboot #重新開機

## 增加網路設定檔與開啟ssh功能
wpa_supplicant.conf

放在boot目錄中

## 開機後自動發送ip功能
[自動發送ip的email功能](https://blog.csdn.net/m0_50601931/article/details/114002373)

## 新增gooogle語音助理金鑰

assistant.json

cloud_speech.json

## 修改DEMO程式

cloudspeech_demo.py

## 安裝vim

[參考](https://www.twblogs.net/a/5c3f656abd9eee35b21e32fa)

清理原vi軟件

sudo apt-get remove vim-common

sudo apt autoremove

安裝vim

sudo apt-get install vim

## 安裝gTTs套件

sudo pip3 install gTTS #安裝gtts

sudo pip3 install pydub

## 測試google語音助理功能

更改cloudspeech.py檔案程式碼

[參考](https://github.com/google/aiyprojects-raspbian/issues/716)

原版
```
from google.cloud import speech
...
END_OF_SINGLE_UTTERANCE = speech.types.StreamingRecognizeResponse.END_OF_SINGLE_UTTERANCE
...
encoding=speech.types.RecognitionConfig.LINEAR16,
```
更新後
```
from google.cloud import speech_v1 as speech
...
END_OF_SINGLE_UTTERANCE = speech.types.StreamingRecognizeResponse.SpeechEventType.END_OF_SINGLE_UTTERANCE
...
encoding=speech.types.RecognitionConfig.AudioEncoding.LINEAR16,
...
```
