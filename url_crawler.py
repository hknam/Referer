from selenium import webdriver
import time
import os
import urllib

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

    f.close()
    time.sleep(10)

def main():
    page = 'http://www.yahoo.com'
    driver = init_driver()

    open_chrome(driver, page)

    input_text_box(driver, page)



if __name__ == '__main__':
    main()



