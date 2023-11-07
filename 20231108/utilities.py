import urequests
import time

api_url = "https://goattl.tw/cshs/line_bot" # 伺服器網址
query_url = f"{api_url}/inservice/caesar-cipher?cmd=query" # 查詢密文網址
answer_url = f"{api_url}/inservice/caesar-cipher?cmd=answer" # 查詢密文網址
headers = {"Accept": "text/plain"}

def get_question() -> dict:
    try:
        print("querying", query_url)
        response = urequests.get(query_url)
        if response.status_code == 200:
            data = response.text
            print("Received data:", data)
            question = parse_question_response(data)
            return question
        else:
            print("HTTP GET request failed with status code:", response.status_code)
    except Exception as e:
        print("Exception:", e)
    # finally:
    #     response.close()


def parse_question_response(resp_text: str) -> dict:
    values = resp_text.split(",")
    return {
        "ciphertext": values[0],
        "options": values[1:]
    }


def send_answer(answer: str) -> str:
    try:
        answer = answer.replace(" ", "%20")
        url = f"{answer_url}&ans={answer}"
        print("answering", url)
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.text
            print("Received data:", data)
            return data
        else:
            print("HTTP GET request failed with status code:", response.status_code)

    except Exception as e:
        print("Exception!!:", e)


def oled_wifi_connecting(oled) -> None:
    oled.fill(0)   
    oled.text('Connecting', 10, 10)   
    oled.text('Wifi...', 10, 20)      
    oled.show()


def oled_wifi_connected(oled) -> None:
    oled.fill(0)   
    oled.text('Wifi connected', 10, 10)      
    oled.show()


def oled_show_question(oled, question: dict, cursor_index: int) -> None:
    oled.fill(0)
    ciphertext = question["ciphertext"]
    oled.text(f"{ciphertext}", 3, 3)

    options = question["options"]
    l = len(options)
    for i in range(l):
        if i == cursor_index:
            cursor = ">"
        else:
            cursor = " "
        oled.text(f"{cursor} {options[i]}", 3, 3 + (i + 1) * 15)
    oled.show()


def oled_show_text_list(oled, texts: list) -> None:
    if texts[0] == "try again":
        for i in range(9, -1, -1):
            oled.fill(0)
            oled.text("try again", 3, 3)
            oled.text(str(i), 3, 18)
            oled.show()
            time.sleep(1)
    else:
        oled.fill(0)
        for i in range(len(texts)):
            oled.text(texts[i], 3, 3 + (i + 1) * 15)
        oled.show()
