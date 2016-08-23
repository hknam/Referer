from selenium import webdriver
import time
import os
import urllib
from bs4 import BeautifulSoup
import subprocess
import sys
import json




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
            search_box.send_keys('iphone7')
            search_box.submit()

            page = page.replace('\n', '')
            browser_url = str(driver.current_url)
            result.write(page+','+browser_url+'\n')

            links = driver.find_elements_by_xpath('//*[@href]')

            for link in links:
                href = link.get_attribute('href')
                if href.startswith('http://'):
                    print href
                    driver.get(href)

        except Exception as e:
        # print boxname
            try:
                search_box = driver.find_element_by_id(boxname)
            except Exception as e:
                continue


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

    inputbox_file = open('inputbox_list.txt', 'r')
    f = open('country/South Korea.txt', 'r')


    error_list = open('error_list_'+browser+'.txt', 'w')
    result = open('result_'+browser+'.txt', 'w')


    inputbox_list = inputbox_file.readline()


    while True:

        page = f.readline()
        if not page:
            break

        file_name = 'pcapfile/'+browser+'/'+page.split('.')[0]+'_'+browser+'.pcap'
        tcpdump_command = 'sudo tcpdump -i any -s 0 tcp port 80 -c 2000 -w '+file_name

        subprocess.Popen(tcpdump_command, shell=True, stdin=subprocess.PIPE)

        page = 'http://www.'+page.lower()
        input_text_box(driver, page, inputbox_list, result, error_list)


        time.sleep(1)


    inputbox_file.close()
    f.close()


    result.close()
    error_list.close()


if __name__ == '__main__':
    main()



