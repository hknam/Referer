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


def open_chrome(driver, page):
    driver.get(page)


def close_chrome(driver):
    driver.quit()


def get_http_link(driver, pageurl):
    url_open = urllib.urlopen(pageurl)
    soup = BeautifulSoup(url_open, 'html.parser')
    main_div = soup.find('div')
    link_list = main_div.findAll('a')

    for link in link_list:
        if str(link['href']).startswith('http://'):
            http_link = link['href']
            driver.get(http_link)
            time.sleep(10)




def input_text_box(driver, classname):
    f=open('inputbox_list.txt', 'r')
    inputbox_list = f.readline()

    for boxname in inputbox_list.split(","):
        boxname = boxname.replace('\n', '')
        try:
            search_box = driver.find_element_by_name(boxname)
            search_box.send_keys('Galaxy Note 7')
            search_box.submit()
            break
        except Exception as e:
            print boxname
            continue

    #link = driver.find_element_by_css_selector('a').get_attribute('href')
    get_http_link(driver, driver.current_url)



    f.close()
    time.sleep(10)

def main():
    page = 'http://www.google.com'
    driver = init_driver()

    open_chrome(driver, page)

    input_text_box(driver, page)



if __name__ == '__main__':
    main()



