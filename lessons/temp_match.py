import cv2
import pyautogui as pag


pag.FAILSAFE = True


# 画像のパス
template_path = 'images/template.png'
img_path = 'images/image.png'


# 画面全体のスクリーンショットを撮る
screenshot = pag.screenshot()
screenshot.save(img_path)

# 画面全体のスクリーンショットから設定ボタンの位置を取得する
template = cv2.imread(template_path, 0)
img = cv2.imread(img_path, 0)
result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result) 

# テンプレートの位置を取得する
template_h, template_w = template.shape
top_left = max_loc
bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
print(top_left, bottom_right)

# # スクリーンショット内の設定ボタンを囲う
# cv2.rectangle(img, top_left, bottom_right, 0, 2)
# plt.imshow(img, cmap='gray')

# top_leftの位置を、スクリーンのサイズに合わせる
screen_size = pag.size()
screenshot = pag.screenshot()
x, y = (
    top_left[0] * screen_size[0] / screenshot.width,
    top_left[1] * screen_size[1] / screenshot.height
)
print(x, y)

# 設定ボタンの位置にマウスカーソルを移動する
pag.moveTo(x+50, y-80, duration=1)
pag.doubleClick()
pag.moveTo(x, y, duration=0.5)
pag.click()
pag.press('enter')
