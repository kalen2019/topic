## 安裝lirc

[參考](https://blog.csdn.net/Destinyabc/article/details/107907251)

請到/boot/config.txt將以下更改或直接添加

sudo nano /boot/config.txt

或

sudo vim /boot/config.txt

原版
```
dtoverlay=gpio-ir,gpio_pin=17 #接收

dtoverlay=gpio-ir-tx,gpio_pin=18 #發射
```
更改
```
dtoverlay=gpio-ir,gpio_pin=24 #接收

dtoverlay=gpio-ir-tx,gpio_pin=26 #發射
```
sudo reboot #重開機

sudo nano /etc/lirc/lirc_options.conf

將者兩個變數更改以下內容

```
driver = default
device = /dev/lirc1
```

sudo apt-get install setserial ir-keytable #安裝相關套件


[參考](https://www.twblogs.net/a/5d409721bd9eee51742320bc)

mode2 -m -d /dev/lirc1 #錄製訊號

irsend SEND_ONCE 遙控器名稱 按鍵名稱  #發射紅外線

   #發射過程，發生socket.server報錯，最後發現下發射指令時，不能是超級使用者，也不能加sudo，實際原因好像跟lirc庫有關，故在此做註記。嘗試許多方式，包括降低lirc版本、降低核心版本、增加GCC庫、增加交叉編譯功能等等，都沒有改善問題，故使用此套件時，不要使用root的身分。
