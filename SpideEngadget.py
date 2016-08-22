#coding=utf-8
import urllib.request #自带库，2.#版本引用 urllib即可
import re #正则库


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('utf-8')


def getContentList(html):
    #reg = r'/">(.*?)</a></h2>'
    htmlReg = r'<h2 (.*?)</a></h2>'
    htmlRe = re.compile(htmlReg)
    contentList = re.findall(htmlRe, html)
    for contentOriginal in contentList:
        index = contentOriginal.rfind('/">') + 3
        content = contentOriginal[index:]
        print(content)

if __name__=='__main__':
    html = getHtml("http://cn.engadget.com")

    getContentList(html)
    print('all')
