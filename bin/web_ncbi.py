#!/usr/bin/env python3
# FIXME: 按照之前的筛选方法，存在大量的非特定物种，需要在右上角再进行一次filter
# -*- coding: utf-8 -*-

import sys
import re
import random
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui

# --------------------------------------------------------------> default variable <---------------------------------------------------------------- #
# 可自定义的参数: default_download_dir(无头浏览器默认下载路径)
default_download_dir = ".tmpdir"
specials = 'Oryza_sativa'
log = './log'
out = f'{default_download_dir}/combine_file'

help = f'''
options: 
    -i: [str] -- specials name; e.g. Oryza_sativa; default parament is Oryza_sativa
    -l: [str] -- log file; default is ./log
    -o: [str] -- output file; default is {default_download_dir}/combine_file
    -d: [dir] -- temporary directory for storing downloaded files; defult is .tmpdir
'''
version = '''
version 0.2
'''

for x in range(len(sys.argv)):
    if sys.argv[x]=='-i':
        specials=sys.argv[x+1]
    elif sys.argv[x]=='-l':
        log = sys.argv[x+1]
    elif sys.argv[x]=='-o':
        out = sys.argv[x+1]
    elif sys.argv[x]=='-d':
        default_download_dir = sys.argv[x+1]
    elif sys.argv[x]=='-v':
        print(version)
        sys.exit()
    elif sys.argv[x]=='-h' or sys.argv[x]=='-help':
        print(help)
        sys.exit()
# ==============================================================> variable end <================================================================ #

# --------------------------------------------------------------> basic function <---------------------------------------------------------------- #
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

def try_elem_send(wait, value, by_method, send_content, driver):

    """Description
    用于向输入框发送内容
    @param wait: WebDriverWait object
    @param by_method: xpath or id...
    @param value: find_element value parament
    @param send_content: send content
    @param driver: webdriver object

    @return: bool
    """
    try:
        wait.until(lambda browser:browser.find_element(by = by_method, value = value))
        elem_name = driver.find_element(by=by_method, value = value)
        elem_name.send_keys(send_content)
        time.sleep(random.randint(1,3))
        return True
    except Exception as error:
        print(f'error is {error}')
        try:
            elem_name = driver.find_element(by=by_method, value = value)
            elem_name.send_keys(send_content)
            time.sleep(random.randint(8,10))
            return True
        except Exception as error1:
            print(f'error1 is {error1}')
            print('pass this record')
            return False


def try_elem_click(wait, value, by_method, driver):

    """Description
    用于点击按钮
    @param wait: WebDriverWait object
    @param by_method: xpath or id...
    @param value: find_element value parament
    @param driver: webdriver object

    @return: bool
    """
    try:
        wait.until(lambda browser:browser.find_element(by = by_method, value = value))
        elem_name = driver.find_element(by=by_method, value = value)
        driver.execute_script("arguments[0].click();", elem_name)
        time.sleep(random.randint(1,3))
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

def driverBuild(enable_headless):
     
    """Description

    @param enable_headless: y | n

    @return: prepared webdriver object
    """

    chrome_options = Options()
    # headless browse
    if enable_headless == 'y':
        chrome_options.add_argument('--headless')
    elif enable_headless == 'n':
        pass
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": default_download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
    chrome_options.add_argument('--disable-software-rasterizer')

    # 模拟用户行为
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options = chrome_options)
    enable_download_headless(driver, default_download_dir)
    return driver


def checkbox(by_method, input_value, div_value, driver, biosample, wait):
    if driver.find_element(by=by_method, value=input_value).is_selected():
        return True
        pass
    else:
        if try_elem_click(wait, div_value, by_method, driver):
            return True
            pass
        else:
            print(f'{biosample} count a error in checkbox part')
            return False
# --------------------------------------------------------------> End <---------------------------------------------------------------- #
# 检查是否存在临时目录
cmd = f'[ -e {default_download_dir} ] || mkdir {default_download_dir}'
subprocess.run(cmd, shell=True)
# 检测之前未删除干净的下载文件
cmd = f'[ ! -e {default_download_dir}/SraRunTable.txt ] || rm {default_download_dir}/SraRunTable.txt'
subprocess.run(cmd, shell=True)

url = 'https://www.ncbi.nlm.nih.gov/'

driver = driverBuild('y')
wait_time = 60
wait = ui.WebDriverWait(driver, wait_time)
driver.get(url)


# enter ncbi home page
try_elem_send(wait, 'term', 'id', specials, driver)
# search specials
try_elem_click(wait, 'search', 'id', driver)
# select data
try_elem_click(wait, '//*[@id="search_db_gds"]/span[1]', 'xpath', driver)
try_elem_click(wait, '//*[@id="_studyTypeGds"]/li/ul/li[3]/a', 'xpath', driver)
try_elem_click(wait, '//*[@id="expProfByArrGds"]', 'xpath', driver)
try_elem_click(wait, '//*[@id="metProfByArrGds"]', 'xpath', driver)
try_elem_click(wait, '//*[@id="nonCodRnaProfByHigThrSeqGds"]', 'xpath', driver)
try_elem_click(wait, '//*[@id="studyTypeGds_apply"]', 'xpath', driver)
try_elem_click(wait, '//*[@id="_studyTypeGds"]/li/ul/li[1]/a', 'xpath', driver)

# 使用Top Organisms 再进行一次筛选.
try_elem_click(wait, '//*[@id="taxonomy-subset-container"]/dl[2]/dd/div[1]/div[1]/span/a', 'xpath', driver)
time.sleep(random.randint(100,140))

# 6. expand record to 500
try_elem_click(wait, '//*[@id="EntrezSystem2.PEntrez.Gds.Gds_ResultsPanel.Gds_DisplayBar.Display"]', 'xpath', driver)
try_elem_click(wait, '//*[@id="ps500"]', 'xpath', driver)

# get total_info
total_info = driver.find_element(by = 'xpath', value = '//*[@id="maincontent"]/div/div[3]/div/h3')
string = total_info.text
print(string)
#  try:
    #  matchObj = re.match("Items: 1 to (\d*) of (\d*)", string)
    #  total_record = matchObj.group(2)
#  except AttributeError:
    #  matchObj = re.match("Items: (\d*)", string)
    #  total_record = matchObj.group(1)

matchObj = re.match("Items: (\d*)", string)
total_record = matchObj.group(1)

print(f'total_record is {total_record}')

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
    time.sleep(random.randint(0,2))

fo = open(log, 'w')
# 8. download the resource
count = 0
for i in url_pool:
    count += 1
    driver.get(i)
    # 使用文本内容进行搜索的时候, 需要在前面带*才能正确执行,原因未知
    if try_elem_click(wait, "//*[text()='SRA Run Selector']", 'xpath', driver):
        pass
    else:
        fo.write(f'{count} record has no SRA Run selector, unfinished\n')
        continue
    if try_elem_click(wait, 't-rit-all', 'id', driver):
        pass
    else:
        fo.write(f'{count} record has no record which can download from SRA Run selector, unfinished\n')
        continue
    time.sleep(random.randint(2,4))
    cmd = f'cat {default_download_dir}/SraRunTable.txt >> {out}'
    subprocess.run(cmd, shell=True)
    time.sleep(random.randint(1,3))
    print(f'{count} record download finished')
    fo.write(f'{count} record downlaod finished' + "\n")
    print(f'current url is {i}')
fo.close()

driver.quit()
cmd = f'[ ! -e {default_download_dir}/SraRunTable.txt ] || rm {default_download_dir}/SraRunTable.txt'
subprocess.run(cmd, shell=True)
