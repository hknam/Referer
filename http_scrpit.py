from selenium import webdriver
import time
import os
import urllib
from bs4 import BeautifulSoup

def init_driver():
    driver_path = ''
    current_path = os.getcwd().split('/')[1]

    if current_path == 'home':
        driver_path = 'chromedriver/chromedriver_linux'
    elif current_path == 'Users':
        driver_path = 'chromedriver/chromedriver_mac'

    driver = webdriver.Chrome(driver_path)
    return driver





def input_text_box(driver, page):
    driver.get(page)

    time.sleep(3)
    input_file=open('inputbox_list.txt', 'r')
    error_file = open('error_list.txt', 'w')


    inputbox_list = input_file.readline()

    print '====', page, '===='

    for boxname in inputbox_list.split(","):
        boxname = boxname.replace('\n', '')
        try:
            search_box = driver.find_element_by_name(boxname)
            search_box.send_keys('Galaxy Note 7')
            search_box.submit()
            time.sleep(5)
            links = driver.find_elements_by_xpath('//*[@href]')

            for link in links:
                href = link.get_attribute('href')
                if href.startswith('http://'):
                    print href

        except Exception as e:
            print boxname
            continue


    input_file.close()
    error_file.close()
    time.sleep(3)

def main():
    driver_path = ''
    current_path = os.getcwd().split('/')[1]

    if current_path == 'home':
        driver_path = 'chromedriver/chromedriver_linux'
    elif current_path == 'Users':
        driver_path = 'chromedriver/chromedriver_mac'

    driver = webdriver.Chrome(driver_path)

    f=open('country/South Korea.txt', 'r')

    while True:
        page = f.readline()
        if not page:
            break
        os.system('sudo tcpdump -i enp0s31f6 -s pcapfile/'+page.split('.')[0]+'.pcap')
        page = 'http://www.'+page.lower()
        input_text_box(driver, page)

    f.close()

if __name__ == '__main__':
    main()



