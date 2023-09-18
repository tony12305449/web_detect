import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import platform
import re
import os

'''
在此程式碼都是用來檢測系統是否安裝chrome的相關套件包刮webdriver以及chrome版本
'''


def check_chrome_service():

    global webdriver_path
    result=''
    system = platform.system()
    bits = platform.architecture()[0]
    if system=='Linux' and bits=='64bit':

        result = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
        if "Google Chrome" in result.stdout:
            pass
        else:
            subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
            subprocess.run(["apt", "install", "./google-chrome-stable_current_amd64.deb"])
            time.sleep(3)
            result = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)

        try:
            webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            return ''
        except:
            
            if len(find_driver())==0:
                version=''
                pattern = r'(\d+\.\d+\.\d+\.\d+)'
                match = re.search(pattern, result.stdout)
                if match:
                    version = match.group(1).strip()
                try:    
                    subprocess.run(["wget", "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/"+version+"/linux64/chromedriver-linux64.zip","--no-check-certificate","-O","chromedriver.zip"])
                    subprocess.run(["unzip","chromedriver.zip","-d","chromedriver"])
                    subprocess.run(["rm","-rf","chromedriver.zip"])
                    return find_driver()[0]
                except:
                    print("If any error please visit this web to check webdriver's file status -> https://googlechromelabs.github.io/chrome-for-testing/#stable")
                    exit()
            else:
                return find_driver()[0]
    else :
        print("Not supports")
        exit()

def find_driver():
    chromedriver_files=[]
    for root, dirs, files in os.walk("./"):
        for file in files:
            if file.startswith('chromedriver') and not os.path.splitext(file)[1]:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    chromedriver_files.append(file_path)
    return chromedriver_files