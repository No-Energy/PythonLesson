#coding=utf-8
import urllib.request #自带库，2.#版本引用 urllib即可
import re #正则库


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('utf-8')


def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    x = 0
    for imgurl in imglist:
        urllib.request.urlretrieve(imgurl, '%s.jpg' % x)
        print('success download %s.jpg' % x)
        x += 1



html = getHtml("http://tieba.baidu.com/p/2460150866")

print(getImg(html))
