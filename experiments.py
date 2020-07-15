import os
import time
from pathlib import Path, PureWindowsPath
from selenium import webdriver, common
from browsermobproxy import Server
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TOE
from selenium.common.exceptions import NoSuchElementException as NSEE
from selenium.common.exceptions import ElementNotInteractableException as ENIE
import logging
from threading import Thread
import traceback
import sqlite3 
import importlib


class_names = {
    "ytb_ad_msg_container": ".ytp-ad-preview-container",
    "ytb_video_element": "html5-main-video",
    "ad_msg": ".ytp-ad-preview-text",
    "skip_ad_button": "//button[contains(@class, 'ytp-ad-skip-button ytp-button')]",
    "you_there_button": "//paper-button[contains(@class, 'style-scope yt-button-renderer style-blue-text') and @id='button' and @aria-label='Yes']",
    "title": "//yt-formatted-string[contains(@class, 'title style-scope ytmusic-player-bar')]",
    "chat_list": "//div[contains(@class, '-GlrD _2xoTX')]" #or# "/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div"
    }

script_path = os.path.realpath(__file__)
script_dir = os.path.split(script_path)[0]
user_dir = os.path.join(script_dir, "gc")
log_file = os.path.join(script_dir, "wa.log")

def log(*msg, print_msg=True, encode=False):    
    msg = " ".join(msg)+"\n"
    
    if (encode):
        msg = msg.encode('utf-8')
        
    with open(log_file, "ba+" if encode else "a+") as logger:
        logger.write(msg)
        
    if print_msg:
        print(msg, end="")

driver = None
proxy = None
server = None
wait = None
log("user_dir:", user_dir)



def initialize_chrome():
    global driver
    global server
    global proxy
    dict={'port':8090}

    server = Server(path=os.path.join(script_dir, "binaries/browsermob-proxy-2.1.4/bin/browsermob-proxy"), options=dict)
    server.start()
    proxy = server.create_proxy()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={user_dir}")
    driver = webdriver.Chrome(str(Path(os.path.join(script_dir, "binaries/chromedriver83")).absolute()), options = chrome_options)
    log('initialized Chrome window!')




def main():    
    if os.path.isfile(log_file):
        os.remove(log_file)
    open(log_file, "w+").close()
    
    initialize_chrome()

    driver.get("https://web.whatsapp.com/")

    input("Opened? ")

    import get_list_chats

    while True:
        try:
            get_list_chats = importlib.reload(get_list_chats)
            get_list_chats.exp(driver)
        except KeyboardInterrupt:
            pass
        if input("Again[*/n]?") =="n":
                break
        

    
    
    
    
    

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("CTRL + C hitted. Hope you enjoy your media :)")
    except Exception as error:
        log(str(error))
        log(traceback.format_exc())
    
    driver.quit()