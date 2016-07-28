from bs4 import BeautifulSoup
import urllib
import time
import random

def crawl_global():
    f=open('alexa_global.txt', 'w')
    for pageCount in range(0, 20):
        page_url = 'http://www.alexa.com/topsites/global;'+str(pageCount)
        url_open = urllib.urlopen(page_url)
        soup = BeautifulSoup(url_open, 'html.parser')

        p_list = soup.findAll('p', attrs={'class':'desc-paragraph'})

        for p in p_list:
            print p.text.strip()
            f.write(p.text.strip()+'\n')
        time.sleep(random.randrange(2,4))
    f.close()

def crawl_country():
    f=open('alexa_korea.txt', 'w')
    for pageCount in range(0, 20):
        page_url = 'http://www.alexa.com/topsites/countries;'+str(pageCount)+'/KR'
        url_open = urllib.urlopen(page_url)
        soup = BeautifulSoup(url_open, 'html.parser')

        p_list = soup.findAll('p', attrs={'class':'desc-paragraph'})

        for p in p_list:
            print p.text.strip()
            f.write(p.text.strip()+'\n')
        time.sleep(random.randrange(2,4))
    f.close()


def crawl_country_category():
    #f=open('alexa_country_category.txt', 'w')

    page_url = 'http://www.alexa.com/topsites/countries'
    url_open = urllib.urlopen(page_url)
    soup = BeautifulSoup(url_open, 'html.parser')
    category_top = soup.find('div', attrs={'class':'categories top'})
    ul_list = category_top.findAll('ul', attrs={'ul':'countries span3'})
    for ul in ul_list:
        li = ul.findAll('li')
        print li







def main():
    #crawl_global()
    crawl_country_category()

if __name__ == '__main__':
    main()
