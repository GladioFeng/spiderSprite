#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FIXME: 厚礼蟹, 无头浏览虽然能够下载文件但是不会重新命名,每次都会把上一次下载的内容覆盖掉,我只能下载完一次,然后把这个文件的内容传到我自己设定的一个新文件里面
# FIXME: 如果一个record报错之后,会把上次的record的内容再复制一份到combine_file.txt中
import re
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support import ui
import subprocess

def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

def try_elem_send(wait, value, by_method, specials ):

    """Description

    @param wait: WebDriverWait object
    @param by_method: xpath or id...
    @param value: find_element value parament
    @param specials: send content

    @return: none
    """
    try:
        wait.until(lambda browser:browser.find_element(by = by_method, value = value))
        elem_name = driver.find_element(by=by_method, value = value)
        elem_name.send_keys(specials)
        time.sleep(random.randint(0,2))
        return True
    except Exception as error:
        print(f'error is {error}')
        try:
            elem_name = driver.find_element(by=by_method, value = value)
            elem_name.send_keys(specials)
            time.sleep(random.randint(8,10))
            return True
        except Exception as error1:
            print(f'error1 is {error1}')
            print('pass this record')
            return False


def try_elem_click(wait, value, by_method):

    """Description

    @param wait: WebDriverWait object
    @param by_method: xpath or id...
    @param value: find_element value parament

    @return: none
    """
    try:
        wait.until(lambda browser:browser.find_element(by = by_method, value = value))
        elem_name = driver.find_element(by=by_method, value = value)
        driver.execute_script("arguments[0].click();", elem_name)
        time.sleep(random.randint(0,2))
        return True
    except Exception as error:
        print(f'error is {error}')
        try:
            elem_name = driver.find_element(by=by_method, value = value)
            driver.execute_script("arguments[0].click();", elem_name)
            time.sleep(random.randint(8,10))
            return True
        except Exception as error1:
            print('pass this record')
            print(f'erro1 is {error1}')
            return False

# 1. construction web url 
url = "https://www.ncbi.nlm.nih.gov/"
specials = 'oryza sativa'

# 2. open browser
chrome_options = Options()
# headless browse
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "/home/ecs-user/Downloads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-software-rasterizer')

# 模拟用户行为
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options = chrome_options)
enable_download_headless(driver, "/home/ecs-user/Downloads")
driver.get(url)

wait_time = 60

# 3. ncbi 主页搜索

# 点击按钮
# button.click() or driver.execute_script("arguments[0].click();", button)
# 推荐使用driver.execute_script("arguments[0].click();", button)
wait = ui.WebDriverWait(driver, wait_time)
try_elem_send(wait, 'term', 'id', specials)
try_elem_click(wait, 'search', 'id')

# 4. 筛选数据
try_elem_click(wait, '//*[@id="search_db_gds"]/span[1]', 'xpath')
try_elem_click(wait, '//*[@id="_studyTypeGds"]/li/ul/li[3]/a', 'xpath')
try_elem_click(wait, '//*[@id="expProfByArrGds"]', 'xpath')
try_elem_click(wait, '//*[@id="metProfByArrGds"]', 'xpath')
try_elem_click(wait, '//*[@id="nonCodRnaProfByHigThrSeqGds"]', 'xpath')
try_elem_click(wait, '//*[@id="studyTypeGds_apply"]', 'xpath')
try_elem_click(wait, '//*[@id="_studyTypeGds"]/li/ul/li[1]/a', 'xpath')


# 5. get total record number
total_info = driver.find_element(by = 'xpath', value = '//*[@id="maincontent"]/div/div[3]/div[1]/h3')
string = total_info.text
matchObj = re.match("Items: 1 to (\d*) of (\d*)", string)
total_record = matchObj.group(2)
print(f'total_record is {total_record}')

# 6. expand record to 500
try_elem_click(wait, '//*[@id="EntrezSystem2.PEntrez.Gds.Gds_ResultsPanel.Gds_DisplayBar.Display"]', 'xpath')
try_elem_click(wait, '//*[@id="ps500"]', 'xpath')

# 7. get all record's url
url_pool = []
print(total_record)
tmp_list = list(range(1, int(total_record) + 1))
print(tmp_list)


for i in tmp_list:
    xpath_value = r'//*[@id="maincontent"]/div/div[5]/div[' + str(i) + ']/div[2]/div/p/a'
    print(xpath_value)
    record = driver.find_element(by = 'xpath', value=xpath_value)
    href_link = record.get_attribute('href')
    print('href is ', href_link)
    url_pool.append(href_link)
    #  time.sleep(random.randint(1,2))

fo = open('./log', 'w')
# 8. download the resource
count = 0
for i in url_pool:
    count += 1
    driver.get(i)
    # 使用文本内容进行搜索的时候, 需要在前面带*才能正确执行,原因未知
    if try_elem_click(wait, "//*[text()='SRA Run Selector']", 'xpath'):
        pass
    else:
        fo.write(f'{count} record has no SRA Run selector, unfinished')
        continue
    if try_elem_click(wait, 't-rit-all', 'id'):
        pass
    else:
        fo.write(f'{count} record has no record which can download from SRA Run selector, unfinished')
        continue
    time.sleep(random.randint(2,4))
    cmd = 'cat /home/ecs-user/Downloads/SraRunTable.txt >> /home/ecs-user/Downloads/combine_file.txt'
    subprocess.run(cmd, shell=True)
    time.sleep(random.randint(1,3))
    print(f'{count} record download finished')
    fo.write(f'{count} record downlaod finished' + "\n")
    print(f'current url is {i}')
fo.close()


