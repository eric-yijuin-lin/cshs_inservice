from machine import Pin, I2C
from utilities import *
import network
import time
import ssd1306


# 設定 OLED 螢幕
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
cursor_index = 0

# 設定按鈕
query_button = Pin(25, Pin.IN, Pin.PULL_UP)
move_button = Pin(26, Pin.IN, Pin.PULL_UP)
select_button = Pin(27, Pin.IN, Pin.PULL_UP)


# 建立 wifi 連線
WIFI_SSID = 'Wokwi-GUEST'
WIFI_PASSWORD = ''
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while True:
    if not wifi.isconnected():
        print('正在連接到 wifi...')
        oled_wifi_connecting(oled)
        time.sleep(1)
    else:
        print('wifi 已連接！')
        oled_wifi_connected(oled)
        break
    

question = {}
while True:
    time.sleep(0.25)
    if query_button.value() == 0 : # 按下
        question = get_question()
        print("question: ", question)
        cursor_index = 0
        oled_show_question(oled, question, cursor_index)
        
    if move_button.value() == 0 and question:
        cursor_index = (cursor_index + 1) % 3
        oled_show_question(oled, question, cursor_index)

    if select_button.value() == 0 and question:
        answer = question["options"][cursor_index]
        result = send_answer(answer)
        oled_show_text_list(oled, result.split(","))
        
