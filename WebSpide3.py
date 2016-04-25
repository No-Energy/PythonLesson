#coding=utf-8
import urllib.request
import re
from multiprocessing import Pool
import time
import os


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
    picname = os.path.join('/Users/No_Energy/Documents/File', ('%s.jpg' % picname))
    #os.path.join连接两个文件名地址，就比os.path.join("D:\","test.txt")结果是D:\test.txt,需要存在目录
    urllib.request.urlretrieve(imgurl, picname)
    end = time.time()
    print('down %s.jpg successful,use %.2f s' % (picname, (end - start)))


if __name__=='__main__':
    html = getHtml("http://tieba.baidu.com/p/2460150866")
    urls = getImg(html)
    pool = Pool(4)
    pool.map(downImg, urls)

