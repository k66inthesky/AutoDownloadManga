#Author: Lana Chen
#Update: May 26th, 2020
#Description: Automatically download series of a manga from www.manhuaren.com . 

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
#import urllib.request
from PIL import Image
from fake_useragent import UserAgent
from io import BytesIO
URL_MANHUAREN='https://www.manhuaren.com/'

#SETTING!!!( Set for yourself )
#You should change URL_HOME to become which manga.
#If you don't change the CHAPTER_NO, by default MAX_CHAPTER will be the length of current chapter number.But be careful: if you set CHAPTER_NO too big, the webdriver won't find and the compile error will happen!
URL_HOME="https://www.manhuaren.com/manhua-guimiezhiren/?from=/manhua-list/"
CHAPTER_NO=0

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL_HOME)
soup=BeautifulSoup(driver.page_source)

l_url,l_title=[],[]
a_class=soup.find_all("a", {"class": "chapteritem"})
for href in a_class:
    url=href.get('href')
    title=href.get('title')
    if title!='':
        l_url.append(url)
        l_title.append(title)
#print(l_url,l_title,"====")


#If you don't change the CHAPTER_NO, by default MAX_CHAPTER will be the length of current chapter number.But be careful: if you set CHAPTER_NO too big, the webdriver won't find and the compile error will happen!
if CHAPTER_NO == 0:
    MAX_CHAPTER=len(l_url)
else:
    MAX_CHAPTER=CHAPTER_NO


for i in range(MAX_CHAPTER):
    chapter = MAX_CHAPTER-i

    url=URL_MANHUAREN+str(l_url[i])
    response = driver.get(url)
    soup_=BeautifulSoup(driver.page_source)
    if soup_ != None:
        driver.get(url)
        img_class=soup_.find_all("img", {"class": "lazy"})
        #print(img_class)
        j=0
        for img in img_class:
            j+=1
            img_url=img.get('data-src')
            '''headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/83.0.4103.61 Safari/537.36'}'''
            ua = UserAgent()
            headers=ua.chrome
            
            response = requests.get(img_url,headers)
            img = Image.open(BytesIO(response.content))
            
            store_path='./Kimetsu_no_Yaiba/'+str(chapter)+'_'+str(j)+'_'+'.png'
            img = img.save(store_path ) 

    del response

