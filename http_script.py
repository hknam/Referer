from selenium import webdriver
import time
import os
import urllib
from bs4 import BeautifulSoup
import subprocess

def init_driver():
    driver_path = ''
    current_path = os.getcwd().split('/')[1]

    if current_path == 'home':
        driver_path = 'chromedriver/chromedriver_linux'
    elif current_path == 'Users':
        driver_path = 'chromedriver/chromedriver_mac'

    driver = webdriver.Chrome(driver_path)
    return driver





def input_text_box(driver, page, inputbox_list):
    driver.get(page)


    for boxname in inputbox_list.split(","):
        boxname = boxname.replace('\n', '')
        try:
            search_box = driver.find_element_by_name(boxname)
            search_box.send_keys('Galaxy Note 7')
            search_box.submit()
            #time.sleep(1)

            #print search_box
            print page
            print str(driver.current_url)
            print '======='
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


def main():
    driver_path = ''
    current_path = os.getcwd().split('/')[1]

    if current_path == 'home':
        driver_path = 'chromedriver/chromedriver_linux'
    elif current_path == 'Users':
        driver_path = 'chromedriver/chromedriver_mac'

    driver = webdriver.Chrome(driver_path)
    #driver = webdriver.Firefox()
    f=open('country/South Korea.txt', 'r')
    input_file = open('inputbox_list.txt', 'r')
    inputbox_list = input_file.readline()

    while True:
        page = f.readline()
        if not page:
            break


        file_name = 'pcapfile/'+page.split('.')[0]+'.pcap'
        tcpdump_command = 'sudo tcpdump -i any -s 0 -w '+file_name

        tcpdump_process = subprocess.Popen(tcpdump_command, shell=True, stdin=subprocess.PIPE)

        page = 'http://www.'+page.lower()
        input_text_box(driver, page, inputbox_list)

        #tcpdump_process.terminate()
        tcpdump_process.kill()

    f.close()
    input_file.close()


if __name__ == '__main__':
    main()



