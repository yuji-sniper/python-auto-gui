import pyautogui as pag
import time
from PIL import Image
import pyocr
import cv2


# 寿司打の自動プレイ
# https://sushida.net/play.html



class Player:
    
    SCREEN_IMAGE_PATH = 'sushida/images/screenshot.png'
    SETTING_BUTTON_IMAGE_PATH = 'sushida/images/setting_button.png'
    START_BUTTON_POSITION = {'x': 250, 'y': 250}
    BEGINNER_COURSE_BUTTON_POSITION = {'x': 250, 'y': 180}
    COURSE_BUTTON_SPACE = 70
    COURSES = [1, 2, 3]
    DEFAULT_COURSE = 3
    CYCLE_MAX = 342
    CYCLE_INTERVALS = {1: 0.2, 2: 0.3, 3: 0.42,}
    CHARS_IMAGE_PATH = 'sushida/images/chars.png'
    CHARS_POSITIONS = {
        1: {'x': 170, 'y': 232, 'w': 160, 'h': 22},
        2: {'x': 150, 'y': 232, 'w': 200, 'h': 22},
        3: {'x': 80, 'y': 232, 'w': 340, 'h': 22},
    }
    SHRINK_SIZE = {1: 5, 2: 4, 3: 4}
    
    def __init__(self) -> None:
        self.tool = pyocr.get_available_tools()[0]
        self.canvas_position = {'x': 0, 'y': 0}
        self.chars_screenshot_position_ini = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
        self.chars_screenshot_position = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
        self.course = self.DEFAULT_COURSE
        self.course_button_position = {'x': 0, 'y': 0}
        self.curr_text = ''
        self.prev_text = '1'
        self.count = 0
    
    # プレイ
    def play(self):
        self.setup()
        self.start_game()
        self.cycle()
    
    # セットアップ
    def setup(self):
        pag.FAILSAFE = True
        self.set_canvas_position()

    # タイトル画面からゲーム開始まで
    def start_game(self):
        self.select_course()
        self.set_course_button_position()
        self.set_chars_screenshot_position()
        x, y = self.canvas_position['x'], self.canvas_position['y']
        pag.moveTo(
            x+self.START_BUTTON_POSITION['x'],
            y+self.START_BUTTON_POSITION['y'],
            duration=1)
        pag.doubleClick()
        pag.moveTo(
            x+self.course_button_position['x'],
            y+self.course_button_position['y'],
            duration=0.5)
        pag.click()
        time.sleep(0.5)
        pag.press('enter')
        time.sleep(2)

    # canvas左上の座標を取得
    def set_canvas_position(self):
        setting_btn_x, setting_btn_y = self.get_setting_button_position()
        self.canvas_position['x'] = setting_btn_x-170
        self.canvas_position['y'] = setting_btn_y-330

    # 設定ボタンの座標を取得
    def get_setting_button_position(self):
        # 画面全体のスクリーンショットを撮る
        screenshot = pag.screenshot()
        screenshot.save(self.SCREEN_IMAGE_PATH)
        # 画面全体のスクリーンショットから設定ボタンの位置を取得する
        template = cv2.imread(self.SETTING_BUTTON_IMAGE_PATH, 0)
        img = cv2.imread(self.SCREEN_IMAGE_PATH, 0)
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result) 
        # 設定ボタンの座標をスクリーンのサイズに合わせる
        screen_size = pag.size()
        x, y = (
            max_loc[0] * screen_size[0] / screenshot.width,
            max_loc[1] * screen_size[1] / screenshot.height
        )
        return int(x), int(y)

    # 文字列のスクリーンショットの座標をセット
    def set_chars_screenshot_position(self):
        chars_position = self.CHARS_POSITIONS[self.course]
        self.chars_screenshot_position_ini = {
            'x': chars_position['x'] + self.canvas_position['x'],
            'y': chars_position['y'] + self.canvas_position['y'],
            'w': chars_position['w'],
            'h': chars_position['h']
        }
        self.chars_screenshot_position = self.chars_screenshot_position_ini.copy()
    
    # コースのボタンの座標を取得
    def select_course(self):
        course_input = input('コース: ')
        course_input = int(course_input)
        if course_input not in self.COURSES:
            course_input = self.DEFAULT_COURSE
        self.course = course_input
    
    # コースのボタンの座標をセット
    def set_course_button_position(self):
        self.course_button_position['x'] = self.BEGINNER_COURSE_BUTTON_POSITION['x']
        self.course_button_position['y'] = self.BEGINNER_COURSE_BUTTON_POSITION['y'] + (self.course-1) * self.COURSE_BUTTON_SPACE
    
    # サイクル
    def cycle(self):
        for _ in range(self.CYCLE_MAX):
            img = self.take_screenshot_chars()
            self.read_chars(img)
            is_changed_width = self.change_chars_screenshot_width()
            self.update_prev_text()
            if is_changed_width:
                time.sleep(0.5)
                continue
            self.type_chars()
            self.count += 1
            print(f'{self.count}回', self.curr_text)
            time.sleep(self.CYCLE_INTERVALS[self.course])

    # スクリーンショットを撮る
    def take_screenshot_chars(self) -> Image:
        img_path = self.CHARS_IMAGE_PATH
        img = pag.screenshot(
            img_path,
            region=tuple(self.chars_screenshot_position.values())
        )
        img = img.convert('L') # グレースケールに変換
        img = Image.eval(img, lambda x: 255 - x) # 白黒反転
        img.save(img_path)
        return img

    # スクショから文字列を読み取る
    def read_chars(self, img: Image):
        text: str = self.tool.image_to_string(
            img, lang='eng',
            builder=pyocr.builders.TextBuilder()
        )
        remove_chars = dict.fromkeys(map(ord, ' _\\\'|”'), None)
        text = text.translate(remove_chars)
        text = text.lower()
        self.curr_text = text
    
    # 前回の文字列を更新
    def update_prev_text(self):
        self.prev_text = self.curr_text
    
    # スクショの幅を調整する（空文字列の場合または前回と同じ文字列の場合に幅を縮める）
    def change_chars_screenshot_width(self) -> bool:
        is_empty = (self.curr_text == '')
        is_equal_to_prev = (self.curr_text == self.prev_text)
        if (is_empty or is_equal_to_prev):
            self.shurink_chars_screenshot_width()
            reason = '[空文字列]' if is_empty else '[前回と同じ]'
            print('スクショ幅縮小', reason, self.chars_screenshot_position['w'], self.curr_text)
            return True
        else:
            self.reset_chars_screenshot_position()
            return False
    
    # スクショの幅を縮める
    def shurink_chars_screenshot_width(self):
        shrink_size = self.SHRINK_SIZE[self.course]
        self.chars_screenshot_position['x'] += shrink_size
        self.chars_screenshot_position['w'] -= shrink_size * 2
    
    # スクショの座標をリセット
    def reset_chars_screenshot_position(self):
        self.chars_screenshot_position = self.chars_screenshot_position_ini.copy()

    # 読み取った文字列をタイプする
    def type_chars(self):
        pag.write(self.curr_text)


player = Player()
player.play()

