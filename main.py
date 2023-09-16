import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import json
from bs4 import BeautifulSoup
import g4f


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


if __name__ == '__main__':

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('http://192.168.0.1/')
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    head_tag = soup.find('head')
    if head_tag:
        head_tag.clear()

    new_html = str(soup)
    res = Ask_GPT("請找出輸入帳號和密碼欄位的ID(若沒有帳號欄位或是帳號欄位隱藏則僅顯示密碼)，若都無則回應無\n請使用(username:，password:)格式回應\n" + new_html)
    print(res)
    res2 = Ask_GPT("請找出登入的按鈕ID\n請使用(ID:)格式回應\n" + new_html)
    print(res2)

    # request_payload = driver.execute_script('return JSON.stringify(performance.getEntries()[0].request.postData);')
    # print(request_payload)
    # time.sleep(5)

    driver.quit()
