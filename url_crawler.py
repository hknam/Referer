from selenium import webdriver
import time
import os

def main():
    driver_path = ''
    current_path = os.getcwd().split('/')[1]
    if current_path == 'home':
        driver_path = 'chromedriver/chromedriver_linux'
    elif current_path == 'User':
        driver_path = 'chromedriver/chromedriver_mac'

    driver = webdriver.Chrome(driver_path)

    driver.get('http://www.naver.com')
    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    main()



