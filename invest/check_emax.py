from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import dotenv_values


# 環境変数を読み込む
envs = dotenv_values(".env")

# ブラウザを開く
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
browser = webdriver.Chrome(options=options)

# GMOクリック証券のログイン画面を開く
gmo_url = envs['GMO_LOGIN_URL']
browser.get(gmo_url)
sleep(5)

# ログイン操作
username_input = browser.find_element(by=By.ID, value='j_username')
password_input = browser.find_element(by=By.ID, value='j_password')
submit_button = browser.find_element(by=By.XPATH, value="//button[@type='submit' and contains(@value, 'Login')]")
username_input.send_keys(envs['GMO_USERNAME'])
password_input.send_keys(envs['GMO_PASSWORD'])
submit_button.click()
