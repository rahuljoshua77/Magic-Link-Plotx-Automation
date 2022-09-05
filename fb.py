from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()

opts = webdriver.ChromeOptions()

opts.headless = False
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
#opts.add_argument("window-size=200,100")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--disable-blink-features=AutomationControlled')
prefs = {"profile.default_content_setting_values.notifications" : 2}
opts.add_experimental_option("prefs",prefs)
opts.add_experimental_option('excludeSwitches', ['enable-logging'])


def xpath_type(el,mount):
    return wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_el(el):
    element_all = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))
    return browser.execute_script("arguments[0].click();", element_all)

def task():
    reveal_key = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="By revealing the private key for"]/following-sibling::div[1]'))).text
    
    with open('Revealing_Private_Key.txt','a') as f:
        f.write('{0}\n'.format(reveal_key))
    button_clicks = wait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '(//div[text()="you are agreeing that:"]/following-sibling::div/div/div[1])')))
    for i in button_clicks:
        i.click()
    xpath_el('//div[text()="Reveal Private Key"]')
    pv_key = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="fontMonospace"]'))).text
    with open('Private_Key.txt','a') as f:
        f.write('{0}\n'.format(pv_key))
    with open('result.txt','a') as f:
        f.write('{0}|{1}\n'.format(reveal_key,pv_key))
    browser.quit()
    
def login_email():
    global element
    global browser

    element = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, '//input[@name="email"]')))
    element.send_keys(email)
        
    sleep(0.5)
    element.send_keys(Keys.ENTER) 
    try:
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
    except:
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
    
    element.send_keys(password)
    sleep(0.5)
    element.send_keys(Keys.ENTER)
 
    sleep(5)
    try:
        xpath_el('//button[@type="submit"]')
    except:
        pass

    print(f"[{time.strftime('%d-%m-%y %X')}] [ {email} ] Success Login")
    task()
    
def open_browser(k):
    
    global browser
    global element
    global email
    global password
    k = k.split("|")
    email = k[0]
    password = k[1]

    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
    browser = webdriver.Chrome(options=opts, desired_capabilities=dc)
    browser.get("https://reveal.magic.link/plotx")
    xpath_el('//img[contains(@src,"facebook")]/parent::button')
    
    try:
        login_email()
    except Exception as e:
        print(f"[{time.strftime('%d-%m-%y %X')}] [ {email} ] Failed Login, Error: {e}")
        with open('failed.txt','a') as f:
            f.write('{0}|{1}\n'.format(email,password))
        browser.quit()

if __name__ == '__main__':
    global list_accountsplit
    global url
    print(f"[{time.strftime('%d-%m-%y %X')}] Automation MagicLink")
   
    file_list_akun = "data.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split("\n")
    jumlah = int(input(f"[{time.strftime('%d-%m-%y %X')}] Multi Processing: "))
    #open_browser(list_accountsplit[0])
    with Pool(jumlah) as p:  
        p.map(open_browser, list_accountsplit)
