#coding=utf-8
import urllib.request
import re
from multiprocessing import Pool
import time

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('utf-8')


def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    return imglist

def downImg(imgurl):
    start = time.time()
    picname = str(start).replace('.', '')[-11:]
    urllib.request.urlretrieve(imgurl, '%s.jpg' % picname)
    end = time.time()
    print('down %s.jpg successful,use %.2f s' % (picname, (end - start)))


if __name__=='__main__':
    html = getHtml("http://tieba.baidu.com/p/2460150866")
    urls = getImg(html)
    pool = Pool(4)
    pool.map(downImg, urls)

