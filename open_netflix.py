import pyautogui as pag
import time

# p = pag.position()
# print(p)

pag.rightClick(305, 947)
pag.moveTo(305, 753, duration=0.5)
pag.click()
pag.moveTo(611, 555, duration=0.5)
pag.doubleClick()
time.sleep(3)
pag.moveTo(577, 160, duration=0.5)
pag.click()
