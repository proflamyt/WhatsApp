import time
import datetime as dt
import json
import os
import shutil
import pickle
import csv
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
from bs4 import BeautifulSoup

s=Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--user-data-dir=C:\\Users\\USER\\Desktop\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
class WhatsAppElements:
    
    search = (By.CSS_SELECTOR, "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")
 
class WhatsApp:
    browser =  None
    timeout = 10  # The timeout is set for about ten seconds
    def __init__(self, wait, screenshot=None, session=None):
        self.browser = webdriver.Chrome(service=s, options=options)# change path
        self.browser.get("https://web.whatsapp.com/") #to open the WhatsApp web
        # you need to scan the QR code in here (to eliminate this step, I will publish 
      
        WebDriverWait(self.browser,wait).until( 
        EC.presence_of_element_located(WhatsAppElements.search))  # wait till search element appears
        #print('hey')
      
    def goto_main(self):
        try:
            self.browser.refresh()
            Alert(self.browser).accept()
        except Exception as e:
            print(e)
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
            WhatsAppElements.search))
    
    def unread_usernames(self, scrolls=100):
       # self.goto_main()
        initial = 10
        usernames = []
        for i in range(0, scrolls):
            self.browser.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            for i in soup.find_all("div", class_="_2nY6U _3C4Vf"):
               # print(i)
                if i.find("div", class_="_3OvU8"):
                    username = i.find("div", class_="zoWT4").text
                #    print(username)
               # date     _1i_wG
                    usernames.append(username)
            initial += 10
        # Remove duplicates
        usernames = list(set(usernames))
        return usernames
 
 
    def get_last_message_for(self, name):
        messages = list()
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(name+Keys.ENTER)
        time.sleep(3)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="message-in"):
            message = i.find("span", class_="selectable-text")
            
            if message:
                for j in message:
                  
                    if 'Ref' in j.text:
                        messages.append(j.text)
            messages = list(filter(None, messages))
        return messages

whatsapp = WhatsApp(100, session="mysession")
#print('done ==================')
user_names = whatsapp.unread_usernames(scrolls=1000)
print(f'====================================={user_names}')
with open('readme.txt', 'a') as f:
    
    for name in user_names:
        messages = whatsapp.get_last_message_for(name)
        if messages:
            ola = ' '.join(messages)

            f.write(f'{ola},============ {name}')
            f.write('\n')

