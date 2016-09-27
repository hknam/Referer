from selenium import webdriver
import time
import os
import subprocess
import sys
from scapy.all import *




def input_text_box(driver, page, inputbox_list, result, error_list, query):
    print 'page : ', page
    driver.get(page)
    browser_url = ''
    for boxname in inputbox_list.split(","):
        boxname = boxname.replace('\n', '')
        try:
            search_box = driver.find_element_by_name(boxname)
            search_box.clear()
            search_box.send_keys(query)
            search_box.submit()

            page = page.replace('\n', '')
            browser_url = str(driver.current_url)
            result.write(page+','+browser_url+'\n')

            links = driver.find_elements_by_xpath('//*[@href]')

            for link in links:
                href = link.get_attribute('href')
                src_page=page.split('.')[1]
                if href.startswith('http://'):
                    if href.find(src_page) < 0:
                        print 'click link address : ', href
                        link.click()
                        driver.implicitly_wait(10)
                        time.sleep(1)
                        break

        except Exception as e:
        # print boxname
            continue

def run(target, p_list, query):
    try:
        pkt = rdpcap(target)
    except MemoryError:
        print "Sorry - Memory Error"
        return
    except scapy.error.Scapy_Exception:
        print 'Not a pcap capture file (bad magic)'
        return
    numPkt = len(pkt)

    print "Analyzing : " + target
    print "Total Packets: %d\n" % numPkt\

    for packet in pkt:
        layer = packet.payload
        p_dict = dict()
        while layer:
            layerName = layer.name
            if layerName == "IP":
                p_dict['srcip'] = layer.src
                p_dict['desip'] = layer.dst
            if layerName == "TCP":
                p_dict['sport'] = layer.sport
                p_dict['dport'] = layer.dport
                p_dict['seq'] = layer.seq
                p_dict['ack'] = layer.ack
                p_dict['flags'] = layer.flags

            if layerName == "Raw":
                result = processHTTP(layer.load, query)
                for k,v in result.items():
                    p_dict[k] = v
            layer = layer.payload
            if p_dict.has_key('http'):
                p_list.append(p_dict)

def processHTTP(data, query):
    info = dict()
    headers = str(data).splitlines()
    for header in headers:
        if header.startswith('GET'):
            info['http']='request'
            info['method']=header.split()[0]
            info['uri']=header.split()[1]
            if str(info['uri']).find(query) > 0:
                print '=================='
                print 'GET URI'
                print str(info['uri'])
                print '=================='+'\n'

        if header.startswith('POST'):
            info['http']='request'
            info['method']=header.split()[0]
            info['uri']=header.split()[1]
        '''
        if header.startswith('HTTP'):
            info['http']='response'
            info['status']=header.split()[1]
        '''
        if header.startswith('HOST') : info['host'] = header.split(':')[1]
        #if header.startswith('User-Agent') : info['user-agent'] = header.split(':',1)[1]
        if header.startswith('Referer') :
            info['referer'] = header.split(':',1)[1]
            if str(info['referer']).find(query) > 0:
                print '=================='
                print 'Referer'
                print str(info['referer']).strip()
                print '==================' + '\n'

                break

    return info




def main():
    driver_path = ''
    p_list = []

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

    inputbox_file = open('inputbox_list.txt', 'r')
    page_list = open('country/South Korea.txt', 'r')


    error_list = open('error_list_'+browser+'.txt', 'w')
    result = open('result_'+browser+'.txt', 'w')


    inputbox_list = inputbox_file.readline()
    query = 'iphone7'

    while True:
        page = page_list.readline()
        if not page:
            break

        file_name = 'pcapfile/'+browser+'/'+page.split('.')[0]+'_'+browser+'.pcap'
        tcpdump_command = 'sudo tcpdump -i any -s 0 tcp port 80 -c 300 -w '+file_name

        subprocess.Popen(tcpdump_command, shell=True, stdin=subprocess.PIPE)

        page = 'http://www.'+page.lower()
        input_text_box(driver, page, inputbox_list, result, error_list, query)

        #run(file_name, p_list, query)

    page_list.close()


    result.close()
    error_list.close()


if __name__ == '__main__':
    main()



