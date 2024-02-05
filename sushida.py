import pyautogui as pag
import time
from PIL import Image
import pyocr


# 寿司打の自動プレイ
# https://sushida.net/play.html


ini_x, ini_y, ini_w, ini_h = 540, 484, 352, 22
w_shrink_size = 3
cycle_sleep_time = 0.4


# セットアップ
def setup():
    pag.FAILSAFE = True

# ツールを取得
def get_tool():
    return pyocr.get_available_tools()[0]

# タイトル画面からゲーム開始まで
def start_game():
    # pag.moveTo(730, 510, duration=0.5)
    # pag.doubleClick()
    # pag.moveTo(670, 575, duration=0.5)
    pag.click()
    pag.press('enter')
    time.sleep(2.5)

# スクリーンショットを撮る
def screenshot(x, y, w, h) -> Image:
    img = pag.screenshot(
        'images/chars/sushida.png',
        region=(x, y, w, h)
    )
    img = img.convert('L')
    return img

# スクショから文字列を読み取る
def read_chars(tool, img: Image) -> str:
    text = tool.image_to_string(
        img,
        lang='eng',
        builder=pyocr.builders.TextBuilder()
    )
    return text

# スクショの幅を調整する（空文字列の場合または前回と同じ文字列の場合に幅を縮める）
def change_width(x, w, text, before_text):
    is_empty = (text == '')
    is_same_as_before = (text == before_text)
    is_changed = False
    if (is_empty or is_same_as_before):
        x -= w_shrink_size
        w -= w_shrink_size * 2
        is_changed = True
        reason = '[空文字列]' if is_empty else '[前回と同じ]'
        print('縮めた', reason, w, text)
    else:
        x = ini_x
        w = ini_w
    return x, w, is_changed

# 読み取った文字列をタイプする
def type_chars(text: str):
    pag.write(text)

# サイクル
def cycle(n: int, tool):
    count = 0
    x, y, w, h = ini_x, ini_y, ini_w, ini_h
    before_text = '1'
    for _ in range(n):
        img = screenshot(x, y, w, h)
        text = read_chars(tool, img)
        x, w, is_width_changed = change_width(x, w, text, before_text)
        before_text = text
        if is_width_changed: continue
        type_chars(text)
        count += 1
        print(count, '回目')
        if count == n: break
        time.sleep(cycle_sleep_time);

# プレイ
def play(n: int):
    setup()
    start_game()
    tool = get_tool()
    cycle(n, tool)


play(500)
