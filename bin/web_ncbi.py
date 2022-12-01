# -*- coding: utf-8 -*-

# --------------------------------------------------------------> default variable <---------------------------------------------------------------- #
default_download_dir = "/home/fzr/Downloads"
specials = 'Oryza_sativa'
log = './log'
out = f'{default_download_dir}/combine_file'

help = f'''
options: 
    -i: specials name; e.g. Oryza_sativa; default parament is Oryza_sativa
    -l: log file; default is ./log
    -o: output file; default is {default_download_dir}/combine_file
'''
version = '''
'''
# ==============================================================> variable end <================================================================ #
import sys

if len(sys.argv)==1:
    print(f'Please type python {__file__} -h for help.')
    sys.exit()

for x in range(len(sys.argv)):
    if sys.argv[x]=='-i':
        specials=sys.argv[x+1]
    elif sys.argv[x]=='-l':
        log = sys.argv[x+1]
    elif sys.argv[x]=='-o':
        out = sys.argv[x+1]
    elif sys.argv[x]=='-v':
        print(version)
        sys.exit()
    elif sys.argv[x]=='-h' or sys.argv[x]=='-help':
        print(help)
        sys.exit()


import re
import time
import subprocess
import random
from web_basic_function import driverBuild, try_elem_click, try_elem_send
from selenium.webdriver.support import ui

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
# get total_info
total_info = driver.find_element(by = 'xpath', value = '//*[@id="maincontent"]/div/div[3]/div[1]/h3')
string = total_info.text
try:
    matchObj = re.match("Items: 1 to (\d*) of (\d*)", string)
    total_record = matchObj.group(2)
except AttributeError:
    matchObj = re.match("Items: (\d*)", string)
    total_record = matchObj.group(1)
print(f'total_record is {total_record}')

# 6. expand record to 500
try_elem_click(wait, '//*[@id="EntrezSystem2.PEntrez.Gds.Gds_ResultsPanel.Gds_DisplayBar.Display"]', 'xpath', driver)
try_elem_click(wait, '//*[@id="ps500"]', 'xpath', driver)

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