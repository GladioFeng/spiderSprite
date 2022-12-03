#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 爬虫基础模块
# 可自定义的参数: default_download_dir(无头浏览器默认下载路径)
default_download_dir = "/home/fzr/Downloads"

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys


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
