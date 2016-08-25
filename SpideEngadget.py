#coding=utf-8
import urllib.request #自带库，2.#版本引用 urllib即可
import re #正则库
import json #json库

def getFullContent(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')

    print("get")

if __name__=='__main__':
    with open("config.json", 'r') as jsonFile:
        jsonData = json.load(jsonFile)



    url = "http://cn.engadget.com"
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    #htmlReg = r'<h2 (.*?)</a>'
    #htmlRe = re.compile(htmlReg)
    #contentList = re.findall(htmlRe, html)
    contentList = re.findall(r'<h2 class="h2" itemprop="headline">(.*?)</h2>', html)
    for contentOriginal in contentList:
        # index = contentOriginal.rfind('/">') + 3
        content = re.search(r'/">(.*)</a>', contentOriginal).group(1)
        contentUrl = re.search(r'href="(.*)">', contentOriginal).group(1)
        print('Text:%s Url:%s' % (content, contentUrl))
        getFullContent(contentUrl)
    print('all')

