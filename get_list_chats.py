class_names = {
    "ytb_ad_msg_container": ".ytp-ad-preview-container",
    "ytb_video_element": "html5-main-video",
    "ad_msg": ".ytp-ad-preview-text",
    "skip_ad_button": "//button[contains(@class, 'ytp-ad-skip-button ytp-button')]",
    "you_there_button": "//paper-button[contains(@class, 'style-scope yt-button-renderer style-blue-text') and @id='button' and @aria-label='Yes']",
    "title": "//yt-formatted-string[contains(@class, 'title style-scope ytmusic-player-bar')]",
    "chat_list": "//div[contains(@class, '-GlrD _2xoTX')]", #or# "/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div"
    "last_seen": "//span[contains(@class, '_3-cMa _3Whw5')]",
    "msg_box": "//div[contains(@class, '_3FRCZ copyable-text selectable-text') and @contenteditable='true' and @data-tab='1']",
    "msg_container": "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]",
    "pane_side": "//div[@id='pane-side']",
    "search_box": "//div[contains(@class, '_3FRCZ copyable-text selectable-text') and @contenteditable='true' and @data-tab='3']",
    "search_container": "/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div",
    "search_result_list": "//div[@aria-label='Search results.']"
    
    }
import os, time, math
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_msg(msg):
    if msg.tag_name == "img":
        return msg.get_attribute("alt")
    elif msg.tag_name == "span":
        #in group
        try:
            temp = msg.find_elements_by_xpath("./*")
            if len(temp)==0:
                return temp[0].get_attribute("innerHTML")
            else:
                return msg.get_attribute("innerHTML")    
        except:
            return msg.get_attribute("innerHTML")
    else:
        #emot
        return msg.get_attribute("innerHTML")
    

def send_msg(driver, chat=False, bot_msg = "Hello, this is kevin bot. this account is using custom bot. Kevin is not holding his phone right now. He will reply you soon :)"):
    if chat!=False:
        try:
            chat.click()
        except:
            print("send_msg(): error while click")
    msg_box = driver.find_element_by_xpath(class_names["msg_box"])
    msg_container = driver.find_element_by_xpath(class_names["msg_container"])
    driver.execute_script("arguments[0].focus();", msg_container)
    # driver.execute_script(f"arguments[0].innerHTML='{bot_msg}'", msg_box)
    msg_box.send_keys(bot_msg + Keys.ENTER)
    print(bot_msg)

def get_chat_info(driver, chat0):
    chat = chat0.find_elements_by_xpath("./div/div/div")
    try:
        dp = chat[0].find_element_by_xpath(".//img").get_attribute("src")
    except:
        #no dp 
        dp = ""
    text = chat[1].find_elements_by_xpath("./div")
    name_day = text[0].find_elements_by_xpath("./*")
    name = None
    try:
        
        name = name_day[0].find_element_by_xpath("./span/span").get_attribute("title")
    except:
        try:
            
            name = name_day[0].find_element_by_xpath("./div/span").get_attribute("title")
            
        except:
            print("Cannot get name")
                
    
    day = name_day[1].get_attribute("innerHTML")
    
    msg = text[1].find_element_by_xpath("./div/span").find_elements_by_xpath("./*") #inside _2iq-U#[i.tag_name for i in text[1].find_element_by_xpath("./div/span").find_elements_by_xpath("./*")]

    new_msg = False
    try:
        new_msgg = text[1].find_element_by_xpath("./div[2]/span/div/span").get_attribute("aria-label")
        if "unread message" in new_msgg:
            new_msg = True
    except:
        pass

    print(name, new_msg)

    if new_msg:
        send_msg(driver, chat0)

    if len(msg)==1: #you received msg
        msg = extract_msg(msg[0])
    elif len(msg)==2: #p2p chat you sent msg
        check_read = msg[0]
        try:
            msg = extract_msg(msg[1].find_element_by_xpath("./*"))
        except:
            msg = msg[1].get_attribute("innerHTML")

    else:
        sender = msg[0]
        msg = extract_msg(msg[2])
        
    
    # if len(msg.find_elements_by_xpath("./*"))==0:
    #     msg = msg.get_attribute("innerHTML")    
    # else:
    #     msg = msg.find_elements_by_xpath("./*")[0]
    #     


    return [dp, name, msg, day, new_msg]

def scroll_page(driver, webelement, scrollPoints):

    try:
                
        
        return True;
    
    except Exception as e:
    
        e.printStackTrace()
        return False
    


def get_chat_list(driver, functions, limit=-1):
    #back scroll up
    chat_pane = driver.execute_script("return document.getElementById('pane-side');")
    driver.execute_script(f"arguments[0].scrollTop = 0;", chat_pane)

    chat_list = driver.find_element_by_xpath(class_names["chat_list"])
    chat_list_temp = chat_list.find_elements_by_xpath("./*")
    pane_height = driver.execute_script("return arguments[0].scrollHeight", chat_list)
    chat_height = driver.execute_script("return arguments[0].scrollHeight", chat_list_temp[0]) #each height of a chat
    scroll_times = math.ceil(pane_height/chat_height)
    chat_elements_count = 16 #chat counts in elements (pane-side)
    count_until_changed_all = chat_elements_count+5
    count_until_changed_all_px = count_until_changed_all*chat_height
    
    # chat_pane = driver.execute_script("return document.getElementById('pane-side');")
    # print(count_until_changed_all_px, chat_height, len(chat_list_temp))
    # driver.execute_script(f"return arguments[0].scrollBy(0,{count_until_changed_all_px});", chat_pane)
    # return []

    functions[0](driver, chat_list_temp[8])
    return 

    results = [[] for i in functions]
    
    for i in range(int(math.ceil(pane_height/count_until_changed_all_px))):
        time.sleep(0.5)
        chat_pane = driver.find_element_by_xpath(class_names["pane_side"])
        chat_list_container = driver.find_element_by_xpath(class_names["chat_list"]) #redifined for refresh
        
        fun_index = 0
        position0 = driver.execute_script("return arguments[0].scrollTop", chat_pane)
        for fun in functions:
            for chat in chat_list.find_elements_by_xpath("./*"):
                try:
                    fun_return = fun(driver, chat)
                except:
                    fun_return = "Error"
                results[fun_index].append(fun_return)
                # print(fun_return)
                position1 = driver.execute_script("return arguments[0].scrollTop", chat_pane)

                #back to start position
                driver.execute_script(f"return arguments[0].scrollTop = {position0};", chat_pane)
                #refresh the chat list
                chat_list_container = driver.find_element_by_xpath(class_names["chat_list"]) #redifined for refresh
                

            fun_index+=1

        
        driver.execute_script(f"return arguments[0].scrollBy(0,{count_until_changed_all_px});", chat_pane)
        
    

    #back scroll up
    chat_pane = driver.find_element_by_xpath(class_names["pane_side"])
    driver.execute_script(f"arguments[0].scrollTop = 0;", chat_pane)

    return results



def get_clicked_info(driver, chat=False):
    
    # chat_list = get_chat_list(driver)
    # for chat in chat_list:

    error = False
    if chat!=False:
        try:
            chat.click()
        except:
            print("error while click")
            error = True
    time.sleep(0.5)
    dp, name, msg, day, new_msg = get_chat_info(driver, chat)
        
    if error:
        return [name, "Error"]
    # print("name:", name, " - ", end="")
    while True:
        try:
            last_seen = driver.find_element_by_xpath(class_names["last_seen"]).get_attribute("innerHTML").lower()
            if last_seen.endswith("you"):
                #group
                return [name, "It's a group"]
            elif "click" in last_seen:
                continue
            elif "Online" == last_seen or last_seen == "online":
                return [name, "Online"]
                # break
            else:
                return [name, f"Unknown({last_seen})"]
        except:
            #print("offline")
            return [name, "Offline"]
            # break

def go_to_chat(driver, name):
    msg_box = driver.find_element_by_xpath(class_names["search_box"])
    msg_container = driver.find_element_by_xpath(class_names["search_container"])
    driver.execute_script("arguments[0].focus();", msg_container)
    # driver.execute_script(f"arguments[0].innerHTML='{bot_msg}'", msg_box)
    msg_box.send_keys(name)
    time.sleep(1)
    msg_box.send_keys(Keys.DOWN)
    msg_box.send_keys(Keys.ESCAPE)
    # search_list = driver.find_element_by_xpath(class_names["chat_list"]).find_elements_by_xpath("./*")
    # search_list[0].click()
    # print(len(search_list))

def wait_until_ready(driver, timeout=5):
    print("Loading...")
    WebDriverWait
    wait = WebDriverWait(driver, timeout)
    waited_element = wait.until(EC.presence_of_element_located((By.XPATH, class_names["chat_list"])))
    print("READY")
    return waited_element

def exp(driver):
    import traceback

    try:
        os.system("clear")
        #chat_list = get_chat_list(driver)
        
        #get_last_seen(driver)


        # print(get_chat_info(chat_list[0]))
        # return 

        # errors = 0
        # for chat in chat_list:
        #     try:
        #         print(get_chat_info(chat))
        #         print("\n")
        #     except:
        #         errors+=1
        
        #chat_info = get_chat_list(driver, [ get_chat_info])
        # for info in chat_info[0]:
        #     print(info)
        #     print("\n")
        # print(chat_info)
        driver.get("https://web.whatsapp.com/")
        wait_until_ready(driver)
        
        
    except:
        traceback.print_exc()
