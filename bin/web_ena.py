#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support import ui
import subprocess
from web_basic_function import driverBuild, try_elem_click, try_elem_send, checkbox

help = '''
downloaded file will be stored in /home/fzr/Downloads
options:
    -i: biosample list file, one line one record
'''

if len(sys.argv)==1:
    print(f'Please type python {__file__} -h for help.')
    sys.exit()

for i in range(1, len(sys.argv)):
    if sys.argv[i] == '-i':
        inp = sys.argv[i+1]
    elif sys.argv[i] == '-h':
        print(help)
        sys.exit()

url = "https://www.ebi.ac.uk/ena/browser/search"

driver = driverBuild('y')

wait_time = 60
wait = ui.WebDriverWait(driver, wait_time)
biosamples = []
with open(inp, 'r') as fn:
    for line in fn:
        l = line.strip()
        biosamples.append(l)

print(biosamples)

for biosample in biosamples:
    driver.get(url)

    if try_elem_send(wait, '//*[@id="topSearchDiv"]/div[2]/form/div/div[1]/input', 'xpath', biosample, driver):
        pass
    else:
        print(f'{biosample} count a error in input biosample part')
        continue
    print(f'{biosample} Running smoothly ...')
    if try_elem_click(wait, '//*[@id="topSearchDiv"]/div[2]/form/div/div[2]/button', 'xpath', driver):
        pass
    else:
        print(f'{biosample} count a error in click search buttorn')
        continue
    # show column selection
    if try_elem_click(wait, '//*[@id="mat-expansion-panel-header-0"]/span[1]/mat-panel-description/span', 'xpath', driver):
        pass
    else:
        print(f'{biosample} count a error in expand cloumn selection')
        continue
    # fill checkbox
    checkbox_list = ['9', '10', '14', '20', '22', '23', '24', '33']
    for i in checkbox_list:
        if checkbox('xpath',f'//*[@id="mat-checkbox-{i}-input"]', f'//*[@id="mat-checkbox-{i}"]/label/div', driver, biosample, wait):
            pass
        else:
            continue
    if checkbox('xpath',f'//*[@id="mat-checkbox-{i}-input"]', f'//*[@id="mat-checkbox-{i}"]/label/div', driver, biosample, wait):
        pass
    else:
        continue
    # download json file
    if try_elem_click(wait, '//*[@id="view-content-col"]/div[4]/div/div[2]/app-read-file-links/div/div[2]/div[1]/a[1]', 'xpath', driver):
        pass
    else:
        print(f'{biosample} count a error in download json file')
        continue

driver.quit()
