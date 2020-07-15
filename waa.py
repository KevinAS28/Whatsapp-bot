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



class_names = {
    "ytb_ad_msg_container": ".ytp-ad-preview-container",
    "ytb_video_element": "html5-main-video",
    "ad_msg": ".ytp-ad-preview-text",
    "skip_ad_button": "//button[contains(@class, 'ytp-ad-skip-button ytp-button')]",
    "you_there_button": "//paper-button[contains(@class, 'style-scope yt-button-renderer style-blue-text') and @id='button' and @aria-label='Yes']",
    "title": "//yt-formatted-string[contains(@class, 'title style-scope ytmusic-player-bar')]"
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

def get_audio():
    audio = driver.execute_script(f'return document.getElementsByClassName("{class_names["ytb_video_element"]}")[0].volume;')    
    return float(audio)

def set_audio(level=0):
    driver.execute_script(f'document.getElementsByClassName("{class_names["ytb_video_element"]}")[0].volume = {level};')
    log(f"Audio set to {level}")

def set_seek_video(seek=0):
    log(f"Video seek set to {seek}")
    driver.execute_script(f'document.getElementsByClassName("{class_names["ytb_video_element"]}")[0].currentTime = {seek};')    

def wait_for_ad(timeout):
    #timeout 0 is accepted as infinity
    #minimal timeout is 2

    if timeout <= 2 and timeout != 0:
        timeout = 2

    loop_count = timeout+1 if timeout%2 != 0 else timeout

    while True:
        try:
            log("Waiting for ad...")
            wait = WebDriverWait(driver, 2, wait_new_video_refresh_rate)
            ad_msg_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, class_names["ytb_ad_msg_container"])))
            log("Ad detected")
            set_audio(0)
            return True
        except TOE:
            if timeout==0:
                continue
            loop_count-=2
            if (loop_count!=0):
                continue
            return False    

def handle_ad():
    wait = WebDriverWait(driver, 5000)
    ad_msg = str(driver.find_element_by_css_selector(class_names["ad_msg"]).get_attribute("innerHTML"))
    log("Ad message:", ad_msg)
    if "you can" in ad_msg.lower():
        log("Must click ad detected...")
        skip_button = wait.until(EC.presence_of_element_located((By.XPATH, class_names["skip_ad_button"])))
        while True:
            try:
                skip_button.click()
                break
            except ENIE:
                continue        
        log("Clicked!")
        set_seek_video(0)
    else:
        log("Must wait ad detected")
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, class_names["ytb_ad_msg_container"])))
        log("Passed!")

def get_title():
    try:
        return driver.find_element_by_xpath(class_names["title"]).get_attribute("innerHTML")
    except NSEE:
        log("Can't get title")

def wait_video():
    class_wait = "."+class_names["ytb_video_element"]
    log("Waiting for video...", class_wait)    
    while True:
        try:
            wait = WebDriverWait(driver, 1000, wait_new_video_refresh_rate)
            video = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, class_wait)))
            time.sleep(1)
            current_video = video.get_attribute("src")
            if (current_video==""):
                continue
            log(f"Video detected: {current_video} with title '{get_title()}'")
            return current_video
        except TOE:
            pass       

def wait_new_video(__old_video):
    old_video = __old_video
    
    def __new_video(new_driver):
        old_video = __old_video
                
        global the_new_video

        class_wait = "."+class_names["ytb_video_element"]
        video = new_driver.find_element_by_css_selector(class_wait)
        the_new_video = video.get_attribute("src")
        
        old_video = str(old_video)
        
        if the_new_video==False or len(str(the_new_video))<=5:
            return False
                
        result = old_video!=the_new_video
        
        return result

    log(f"Waiting for new video... old: {old_video}\n")

    loop = True
    while loop:
        try:
            wait = WebDriverWait(driver, 10000, wait_new_video_refresh_rate)
            wait.until(__new_video)
            break
        except TOE:
            continue

    log(f"New video detected: |{the_new_video}| with title '{get_title()}'")
    return the_new_video


def prevent_ad():
    log("prevent_ad() called")
    
    #need to get the first video link in order to to compare with the future video
    #in case the first is an ad
    current_video = wait_video()
    set_audio(0)
    
    if (wait_for_ad(timeout=2)):
        handle_ad()
    set_seek_video(0)
    set_audio(1)

    while True:
        current_video = wait_new_video(current_video)
        set_audio(0)
        if (wait_for_ad(timeout=2)):
            handle_ad()
        set_seek_video(0)
        set_audio(1)

    return 0

def keep_continue():
    while True:    
        try:
            wait = WebDriverWait(driver, 5000)
            you_there_button = wait.until(EC.presence_of_element_located((By.XPATH, class_names["you_there_button"])))
            fail = 0
            while True:
                try:
                    you_there_button.click()
                    break
                except ENIE:
                    fail+=1
                    # if (fail>=50):
                    #     log("Can't hit skip button. No such element")
                    time.sleep(1)
                    continue        
        except TOE:
            continue
        time.sleep(10)

def monitor_audio(): #debugging
    log("Monitor audio started [debugging]")
    old = get_audio()
    while True:
        new = get_audio()
        if (new!=old):
            print(f"audio changed from {str(old)} to {str(new)}")
            old = new
        time.sleep(5)

def online_statistic():
    #prepare the database
    connection = sqlite3.connect("online_timestamp.db") 
    



def main():    
    if os.path.isfile(log_file):
        os.remove(log_file)
    open(log_file, "w+").close()
    
    initialize_chrome()

    driver.get("https://web.whatsapp.com/")
    
    
    

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("CTRL + C hitted. Hope you enjoy your media :)")
    except Exception as error:
        log(str(error))
        log(traceback.format_exc())
    
    driver.quit()