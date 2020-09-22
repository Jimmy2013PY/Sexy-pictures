import requests
import os
import time
import urllib.request
import threading
import random
from bs4 import BeautifulSoup
import re


def download_page(url):
    '''
    用于下载页面
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    return r.text

def url_open(url):
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}
    req = urllib.request.Request(url,headers=headers)    
    proxies = ['117.185.16.226:80', '61.135.185.111:80', '112.80.248.75:80', '123.125.114.21:80', '117.185.17.144:80', '117.185.17.17:80', '117.185.16.253:80']
    proxy = random.choice(proxies)
    proxy_support = urllib.request.ProxyHandler({'http':proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(req)
    html = response.read()
    return html


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)
        
def get_img(model_name, pic_name, img_name, img_addr):
    with open('MM/{}/{}/{}'.format(model_name, pic_name, img_name), 'wb') as f:
        img = url_open(img_addr)
        f.write(img)
        time.sleep(0.5)


def main():
    create_dir('MM')
    queue = [i for i in range(0, 1)]   # 构造 url 链接 页码。

    while len(queue) > 0:


        cur_page = queue.pop(0)
        if cur_page == 0:
            url = 'https://www.erosberry.com/models?from=88'
        else:
            url = 'https://www.erosberry.com/models?from=()'.format(cur_page+44)
                                   

        print('正在下载第{}页'.format(cur_page+1))
        time.sleep(1)
          
        soup = BeautifulSoup(download_page(url), 'html.parser')
        
        model_list = soup.find_all('div', class_='thumb')
        
        print('第{}页图片模特目录文件:'.format(cur_page+1), model_list)
        
        
        for i in model_list:
                    
            model_link = "https://www.erosberry.com" + i.a.get('href')
            print(model_link)
            model_name = model_link.split('/')[-1].split('.')[0]
            
            print(model_name)

            if not os.path.exists('MM/{}'.format(model_name)):
                create_dir('MM/{}'.format(model_name))            

          
            soup = BeautifulSoup(download_page(model_link), 'html.parser')
            
            pic_list = soup.find_all('div', class_="container")
            s1 = soup.find_all('span')
            pic_filename = [span.get_text() for span in s1]
            print(pic_filename)
            
            print('第{}页图片<<{}>>模特图片目录:'.format(cur_page+1,model_name), pic_list)
            
            
            for j in pic_list:
                 if len(pic_filename) > 0:               
                    pic_name = pic_filename.pop(0)
                    print(pic_name)
                    pic_link = "https://www.erosberry.com" + j.a.get('href')
                    print(pic_link)
                    
                    if not os.path.exists('MM/{}/{}'.format(model_name, pic_name)):
                        create_dir('MM/{}/{}'.format(model_name, pic_name))            
                                          
                        print('正在下载第{}页<<{}>>模特<<{}>>文件图片'.format(cur_page+1, model_name, pic_name))
                        print("======================================================================") 
                        if len(pic_name) != 0:
                            soup = BeautifulSoup(download_page(pic_link), 'html.parser')
                        
                            img_list = soup.find_all(href=re.compile(r"\d.html"))
                            print(img_list)

                            for k in img_list:
                                img_link = "https://www.erosberry.com" + k.get('href')
                                
                                        
                                soup = BeautifulSoup(download_page(img_link), 'html.parser')
                        
                                img_position = soup.find('a', class_='photo').find_all('img')
                                for l in img_position:
                                    img_addr = "https:" + l.get('src')
                                    
                                    img_name = img_addr.split('/')[-1]
                                    
                            
                                    if not os.path.exists('MM/{}/{}/{}'.format(model_name, pic_name, img_name)):
                                        print("文件不存在，正在下载")
                                        print("文件链接:", img_link)
                                        print("文件名:", img_name)
                                        thread_number = []
                                        for thread in thread_number:
                                            if not thread_test.is_alive():
                                                thread_test.remove(thread_number)
                                        while len(thread_number) < 5:
                                            thread_test = threading.Thread(target=get_img, args=(model_name, pic_name, img_name, img_addr))
                                            thread_test.setDaemon(True)
                                            thread_test.start()
                                            thread_number.append(thread_test)
                                  
                        print('第{}页<<{}>>模特<<{}>>文件图片下载完成'.format(cur_page+1, model_name, pic_name))
                        print("======================================================================")    
                

if __name__ == '__main__':
    main()
