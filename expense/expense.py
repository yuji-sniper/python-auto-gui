from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pyautogui as pag
import pyperclip as pc
from PIL import Image
import pyocr
import cv2
from dotenv import dotenv_values
from time import sleep


class Mizuho:

    def __init__(self):
        self.envs = dotenv_values(".env")
        self.browser = None
        self.expense = []
    
    def execute(self):
        self.open_chrome()
        self.open_mizuho()
        self.input_cust_no()
        self.input_password()
        self.click_next()
        self.click_detail()
        self.show_detail()
        self.get_expense()
    
    def open_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        self.browser = webdriver.Chrome(options=options)
    
    def close_chrome(self):
        self.browser.quit()
    
    def open_mizuho(self):
        mizuho_url = self.envs['MIZUHO_LOGIN_URL']
        self.browser.get(mizuho_url)

    def input_cust_no(self):
        cust_no_input = self.browser.find_element(by=By.ID, value='txbCustNo')
        submit_button = self.browser.find_element(by=By.XPATH, value="//input[@name='N00000-next' and @type='submit']")
        cust_no_input.send_keys(self.envs['MIZUHO_CUST_NO'])
        submit_button.click()
    
    def input_password(self):
        password_input = self.browser.find_element(by=By.ID, value='PASSWD_LoginPwdInput')
        submit_button = self.browser.find_element(by=By.XPATH, value="//input[@value='ログイン' and @type='submit']")
        password_input.send_keys(self.envs['MIZUHO_PASSWORD'])
        submit_button.click()
    
    def click_next(self):
        next_button = self.browser.find_element(by=By.XPATH, value="//section[@id='button-section']/a")
        if next_button:
            next_button.click()
    
    def click_detail(self):
        detail_button = self.browser.find_element(by=By.ID, value='MB_R011N040')
        detail_button.click()
    
    def show_detail(self):
        select = self.browser.find_element(by=By.ID, value='lstAccSel')
        select = Select(select)
        select.select_by_value('1')
        submit_button = self.browser.find_element(by=By.XPATH, value="//section[@class='CenterBlock']/input")
        submit_button.click()
    
    def get_expense(self):
        table = self.browser.find_element(by=By.XPATH, value="//table[@class='n04110-t2']")
        tbody = table.find_element(by=By.TAG_NAME, value='tbody')
        rows = tbody.find_elements(by=By.TAG_NAME, value='tr')
        for i, row in enumerate(rows):
            if i == 0: continue
            cols = row.find_elements(by=By.TAG_NAME, value='td')
            date = cols[0].text.replace('.', '-')
            amount = int(cols[1].text.replace(' 円', '').replace(',', ''))
            self.expense.append([date, amount])
        for d in self.expense:
            print(d)


class Mitsui:
    
    def __init__(self):
        self.envs = dotenv_values(".env")
        self.browser = None
        self.expense = []
    
    def execute(self):
        self.open_chrome()
        self.open_mitsui()
    
    def open_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        self.browser = webdriver.Chrome(options=options)
    
    def close_chrome(self):
        self.browser.quit()
    
    def open_mitsui(self):
        mitsui_url = self.envs['MITSUI_LOGIN_URL']
        self.browser.get(mitsui_url)
    
    
    
    
# mizuho = Mizuho()
mitsui = Mitsui()
# mizuho.execute()
mitsui.execute()
