import pyautogui as pag
import time
from PIL import Image
import pyocr


# 寿司打の自動プレイ
# https://sushida.net/play.html


# セットアップ
def setup():
    pag.FAILSAFE = True

# ツールを取得
def get_tool():
    return pyocr.get_available_tools()[0]

# タイトル画面からゲーム開始まで
def start_game():
    pag.moveTo(730, 510, duration=0.5)
    pag.doubleClick()
    pag.moveTo(670, 575, duration=0.5)
    pag.click()
    pag.press('enter')
    time.sleep(4)

# スクリーンショットを撮る
def screenshot() -> Image:
    img = pag.screenshot(
        'images/chars/sushida.png',
        region=(540, 483, 352, 24)
    )
    img.save('images/chars/sushida.png')
    return img

# スクショから文字列を読み取る
def read_chars(tool, img: Image) -> str:
    text = tool.image_to_string(
        img,
        lang='eng',
        builder=pyocr.builders.TextBuilder()
    )
    return text

# 読み取った文字列をタイプする
def type_chars(text: str):
    pag.write(text)

# プレイ
def play(n: int):
    setup()
    tool = get_tool()
    start_game()
    for _ in range(n):
        img = screenshot()
        text = read_chars(tool, img)
        type_chars(text)
        time.sleep(1)


play(150)
