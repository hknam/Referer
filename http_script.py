from selenium import webdriver
import time
import os
import urllib
from bs4 import BeautifulSoup
import subprocess
import sys



def init_driver():
    driver_path = ''
    current_path = os.getcwd().split('/')[1]

    if current_path == 'home':
        driver_path = 'chromedriver/chromedriver_linux'
    elif current_path == 'Users':
        driver_path = 'chromedriver/chromedriver_mac'

    driver = webdriver.Chrome(driver_path)
    return driver





def input_text_box(driver, page, inputbox_list, result, error_list):
    driver.get(page)
    browser_url = ''
    for boxname in inputbox_list.split(","):
        boxname = boxname.replace('\n', '')
        try:
            search_box = driver.find_element_by_name(boxname)
            search_box.clear()
            search_box.send_keys('Galaxy Note 7')
            search_box.submit()

            browser_url = driver.current_url
            result.write(page+','+browser_url+'\n')
            print browser_url
            '''
            links = driver.find_elements_by_xpath('//*[@href]')

            for link in links:
                href = link.get_attribute('href')
                if href.startswith('http://'):
                    print href
            '''
        except Exception as e:
            #print boxname
            continue

    if not browser_url:
        print 'error : ', page
        error_list.write(page)

def main():
    driver_path = ''
    current_path = os.getcwd().split('/')[1]

    if current_path == 'home':
        chrome_driver_path = 'chromedriver/chromedriver_linux'
    elif current_path == 'Users':
        chrome_driver_path = 'chromedriver/chromedriver_mac'
    else:
        chrome_driver_path = 'chromedriver/chromedriver.exe'
        ie_drver_path = 'chromedriver/IEDriverServer.exe'
        edge_driver_path = 'chromedriver/MicrosoftWebDriver.exe'


    if len(sys.argv) < 2:
        print 'Need [chrome/firefox/safari/IE/Edge]'
        sys.exit(1)

    browser = sys.argv[1]

    if browser == 'chrome':
        driver = webdriver.Chrome(chrome_driver_path)
    elif browser == 'firefox':
        driver = webdriver.Firefox()
    elif browser == 'safari':
        driver = webdriver.Safari()
    elif browser == 'IE':
        driver = webdriver.Ie(ie_drver_path)
    elif browser == 'Edge':
        driver = webdriver.Edge(edge_driver_path)
    else:
        print 'Webdriver open error'
        sys.exit(1)

    #driver = webdriver.Chrome(driver_path)
    #driver = webdriver.Firefox()
    f=open('country/South Korea.txt', 'r')
    inputbox_file = open('inputbox_list.txt', 'r')
    error_list = open('error_list.txt', 'w')
    result = open('result.txt', 'w')
    inputbox_list = inputbox_file.readline()

    while True:

        page = f.readline()
        if not page:
            break

        file_name = 'pcapfile/'+page.split('.')[0]+'.pcap'
        tcpdump_command = 'sudo tcpdump -i any -s 0 -w '+file_name

        tcpdump_process = subprocess.Popen(tcpdump_command, shell=True, stdin=subprocess.PIPE)

        page = 'http://www.'+page.lower()
        input_text_box(driver, page, inputbox_list, result, error_list)

        tcpdump_process.terminate()
        time.sleep(1)

    f.close()
    inputbox_file.close()
    result.close()
    error_list.close()


if __name__ == '__main__':
    main()



