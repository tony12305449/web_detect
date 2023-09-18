import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import json
from bs4 import BeautifulSoup
import g4f
import subprocess
import platform
import re
from check_chrome_service import check_chrome_service
from browsermobproxy import Server


webdriver_path=''
  


def get_web_page(ip='192.168.0.1'): 
    
    '''
    default ip address is 192.168.0.1
    '''
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if webdriver_path=='':
        driver = webdriver.Chrome(options=chrome_options)
    else:
        path=Service(webdriver_path)
        driver = webdriver.Chrome(service=path,options=chrome_options)
    driver.get(f'http://{ip}/')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if soup == '':
        return None
    head_tag = soup.find('head')
    if head_tag:
        head_tag.clear()
    
    new_html = str(soup)


    driver.quit()
    return new_html

def Ask_GPT(message):

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.DeepAi,
        messages=[{"role": "user", "content": message}],
        stream=True,
    )
    messages = ''
    for message in response:
        messages += message
        # print(message)
    return messages

def web_vuln(ip,username='',password='',click_login=''):
    
    server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy")
    server.start()
    proxy = server.create_proxy()
    proxy.new_har("new_har", options={'captureContent': True})
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy.proxy}')
    
    chrome_options.add_argument("--headless")
    if webdriver_path=='':
        driver = webdriver.Chrome(options=chrome_options)
    else:
        path=Service(webdriver_path)
        driver = webdriver.Chrome(service=path,options=chrome_options)
    driver.get(f'http://{ip}/')
    if username !='':
        usernames=driver.find_element(by=By.ID,value=username)
        usernames.send_keys("admin")
    else:
        print(username)
        print(password) 
        usernames=driver.find_element(by=By.ID,value=username)
        usernames.send_keys("admin")
        passwords=driver.find_element(by=By.ID,value=password)
        passwords.send_keys("password")
    button_element = driver.find_element(by=By.XPATH,value=click_login)
    button_element.click()
    har = proxy.har

    for entry in har['log']['entries']:
        request = entry['request']
        if request['method'] == 'POST':
            request_url = request['url']
            request_host = [header['value'] for header in request['headers'] if header['name'].lower() == 'host'][0]
            request_content_length = [header['value'] for header in request['headers'] if header['name'].lower() == 'content-length'][0]
            request_headers = '\n'.join([f"{header['name']}: {header['value']}" for header in request['headers']])
            request_body = request['postData']['text']
            post_request_info = f"POST {request_url} HTTP/1.1\n"
            post_request_info += f"Host: {request_host}\n"
            post_request_info += f"Content-Length: {request_content_length}\n"
            post_request_info += request_headers + '\n\n'
            post_request_info += request_body
            

            print(post_request_info)
            
            print("\n")
    proxy.close()
    server.stop()
    driver.quit()
if __name__ == '__main__':


    testing = "192.168.6.7"

    webdriver_path = check_chrome_service()
    html = get_web_page(testing) 
    if html=='':
        print("該網頁為空")
    else:
        # 在此步驟如果執行失敗，請到lib庫中找到
        username=''
        password=''
        resp = Ask_GPT("請找出輸入帳號和密碼欄位的ID(若沒有帳號欄位或是帳號欄位隱藏則僅顯示密碼)，若無則回應''\n請使用(username:,password:)格式回應\n" + html)
        click_login = Ask_GPT("請找出登入的按鈕Xpath\n請使用(Xpath:)格式回應\n" + html)
        match_user = re.search(r"username:(.*?),\s*password:(.*?)\)", resp)
        if match_user:
            username = match_user.group(1).strip()
            password = match_user.group(2).strip()
        else :
            match = re.search(r"(?:password|passwd|p):(.*?)\)", resp)
            password = match.group(1).strip()
        match_login =click_login[1:-1].replace("(Xpath:)","").replace("Xpath:)","").replace("Xpath:","")
        print(match_login)
        web_vuln(testing,username,password,match_login)
        '''
        try:
            web_vuln(testing,username,password,match_login)
        except:
            這裡我在想要不要加多次詢問GPT，因為可能回答錯誤之類的? (三次上限?)
            print("?")
            pass
        ''' 
        #res2 = Ask_GPT("請找出登入的按鈕ID\n請使用(ID:)格式回應\n" + html)
        #print(res2)
        
    #request_payload = driver.execute_script('return JSON.stringify(performance.getEntries()[0].request.postData);')
    #print(request_payload)
    #time.sleep(5)


