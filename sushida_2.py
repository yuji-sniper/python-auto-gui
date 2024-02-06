import pyautogui as pag
from time import sleep
from PIL import Image
import pyocr
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# 無理そうだったので断念...！！！


class Browser:
    
    SUSHIDA_URL = 'https://sushida.net/play.html'
    CANVAS_ID = '#canvas'
    START_BTN_POSITION = {'x': 250, 'y': 250}
    COURSE_BTN_POSITION = {'x': 195, 'y': 325}
    CHARS_POSITION = {'x': 70, 'y': 234, 'w': 360, 'h': 22}
    
    def __init__(self) -> None:
        self.driver = None
        self.action = None
        self.canvas = None
        self.canvas_position = {'x': 0, 'y': 0}
        self.chars_position_in_screen = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
    
    # 寿司打のページを開く
    def open_sushida(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(self.SUSHIDA_URL)
        sleep(20)
        self.set_canvas()
        self.set_action_chains()
        self.set_chars_position_in_screen()
    
    # キャンバスをセット
    def set_canvas(self):
        self.canvas = self.get_element_by_id(self.CANVAS_ID)
    
    # ActionChainsをセット
    def set_action_chains(self):
        self.action = ActionChains(self.driver)

    # 文字列の座標をセット（スクリーン座標）
    def set_chars_position_in_screen(self):
        self.action.move_to_element_with_offset(
            self.canvas,
            self.CHARS_POSITION['x'],
            self.CHARS_POSITION['y']
        )
        self.action.perform()
        # position = pag.position()
        # self.chars_position_in_screen = {
        #     'x': position.x,
        #     'y': position.y,
        #     'w': self.CHARS_POSITION['w'],
        #     'h': self.CHARS_POSITION['h'],
        # }
        self.action.move_to_element_with_offset(self.canvas, 0, 0)
    
    # 文字列の座標を取得
    def get_chars_position(self) -> dict:
        return self.chars_position_in_screen
    
    # スタートボタンをクリック
    def click_start(self):
        self.click_in_canvas(
            self.START_BTN_POSITION['x'],
            self.START_BTN_POSITION['y']
        )
    
    # コースボタンをクリック
    def click_course(self):
        self.click_in_canvas(
            self.COURSE_BTN_POSITION['x'],
            self.COURSE_BTN_POSITION['y']
        )
    
    ### 以下、汎用メソッド ###
    
    # idを指定して要素を取得
    def get_element_by_id(self, id: str) -> WebElement:
        return self.driver.find_element(by='id', value=id)
    
    # キャンバス内の指定の座標をクリック（キャンバス左上が原点）
    def click_in_canvas(self, x: int, y: int):
        self.action.move_to_element_with_offset(self.canvas, x, y)
        self.action.click()
        self.action.perform()
        # カーソルの位置をログに出力
        
        self.action.move_to_element_with_offset(self.canvas, 0, 0)
    
    # キーを入力
    def send_keys(self, keys):
        self.canvas.send_keys(keys)


class SushidaPlayer:
    
    MAX_CYCLE = 3
    VIEW_SHURINK_SIZE = 3
    CYCLE_INTERVAL = 0.42
    
    def __init__(self, browser: Browser) -> None:
        self.browser = browser
        self.tool = pyocr.get_available_tools()[0]
        self.view_position = browser.get_chars_position()
        self.is_shurinked = False
        self.curr_text = ''
        self.prev_text = '1'
        self.count = 0
    
    # プレイ
    def play(self):
        self.start_game()
        self.cycle()
    
    # 寿司打を開始
    def start_game(self):
        self.browser.open_sushida()
        self.browser.click_start()
        sleep(1)
        self.browser.click_course()
        sleep(1)
        self.browser.send_keys(Keys.ENTER)
        sleep(2)
    
    # サイクル
    def cycle(self):
        for i in range(self.MAX_CYCLE):
            img = self.look()
            self.read(img)
            self.change_view_width()
            self.update_prev_text()
            if self.is_shurinked:
                sleep(0.5)
                continue
            self.type_text()
            print(i+1, '回目')
            sleep(self.CYCLE_INTERVAL)
    
    # 文字列を見る（スクリーンショットを撮る）
    def look(self) -> Image:
        img_path = 'images/chars/sushida.png'
        img = pag.screenshot(
            img_path,
            region=tuple(self.view_position.values())
        )
        print(self.view_position)
        img = img.convert('L') # グレースケールに変換
        img = Image.eval(img, lambda x: 255 - x) # 白黒反転
        img.save(img_path)
        return img
    
    # 文字列を読み取る（文字認識）
    def read(self, img: Image) -> str:
        self.curr_text = self.tool.image_to_string(
            img, lang='eng',
            builder=pyocr.builders.TextBuilder()
        )
    
    # 前回の文字列を更新
    def update_prev_text(self):
        self.prev_text = self.curr_text
    
    # キーを入力
    def type_keys(self, keys):
        self.browser.send_keys(keys)
    
    # スクショの幅を調整する（空文字列の場合または前回と同じ文字列の場合に幅を縮める）
    def change_view_width(self):
        is_empty = (self.curr_text == '')
        is_equal_to_prev = (self.curr_text == self.prev_text)
        if (is_empty or is_equal_to_prev):
            self.shurink_view_width()
            self.is_shurinked = True
            reason = '[空文字列]' if is_empty else '[前回と同じ]'
            print('縮めた', reason, self.view_position['x'], self.curr_text)
        elif self.is_shurinked:
            self.reset_view_position()
            self.is_shurinked = False
    
    # スクショの幅を縮める
    def shurink_view_width(self):
        self.view_position['x'] -= self.VIEW_SHURINK_SIZE
        self.view_position['h'] -= self.VIEW_SHURINK_SIZE * 2
    
    # スクショの座標をリセット
    def reset_view_position(self):
        self.view_position = self.browser.get_chars_position()


pag.FAILSAFE = True
# print(pag.position())
# pag.moveTo(1187, 372, duration=1)

browser = Browser()
player = SushidaPlayer(browser)
player.play()
