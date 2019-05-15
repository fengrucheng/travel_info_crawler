import multiprocessing as mp
import time
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import re
import os

base_url = "http://www.travelroute.in/"  ##website of a travel agency


def crawl(url): #get url
    response = urlopen(url)
    return response.read().decode()


def parse(html): #parse html from url 
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {'href': re.compile(
        "http://www.travelroute.in/product/.*")})  ##use RE  get the webistes that contain travel  products
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    url = soup.find('meta', {'property': "og:url"})['content']
    return title, page_urls, url


unseen = set([base_url, ])
seen = set()
count = 1
pagelist = []  ##store all  pages of product


def travel(): ##get all pages of products in this domine
    fd = open("page.txt", 'a', encoding='UTF-8')
    pool = mp.Pool(8) ##set multiprocess pool, 8 process
    while len(unseen) != 0:  # still get some url to visit

        crawl_jobs = [pool.apply_async(crawl, args=(url,)) for url in unseen]
        htmls = [j.get() for j in crawl_jobs] ##put task into 'pool' and get html by crawl()

        parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
        results = [j.get() for j in parse_jobs] ##put task into 'pool' and get content by parse()

        seen.update(unseen)  # seen the crawled
        unseen.clear()  # nothing unseen
        pagelist=[]
        for title, page_urls, url in results:
            print(title, url)
            pagelist.append(url)
            fd.write(url+',') ##wrtie products pages in a txt in current folder
            unseen.update(page_urls - seen)  # get new url to crawl
    fd.close()
    print('Got all products from this website')

def getinfo():
    text_file = open("page.txt", "r")
    lines = text_file.readlines()
    print(lines)
    text_file.close()
    infopage = ""
    for word in lines: #transfer txt into list
        infopage += word
    infopage = infopage.split(',') 
    fd = open("result.txt", 'a', encoding='UTF-8')
    for i in range(1, len(infopage)-1):
        html = urlopen(infopage[i]).read()
        soup = BeautifulSoup(html, features='lxml')
        title = soup.find(name="h1", attrs={'itemprop': "name"})  ##name of title
        fd.write(title.text)
        print('Wrting....:',title.text)
        soup_text = soup.find('div', id="tab-description")  ##found the div that contains destaination  Description
        fd.write(soup_text.text) ##all description text
    fd.close()
    print('done')

if __name__=='__main__':
    travel()
    getinfo()
