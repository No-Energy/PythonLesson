# coding=utf-8
import urllib.request  # 自带库，2.#版本引用 urllib即可
import re  # 正则库
import json  # json库

def getFullContent(title, url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')

    # 匹配获取页面的POST ID
    postId = re.search(r'var postID = \'(.*)\';', html).group(1)
    # 将地址中的:和/转换伪url编码,由于默认quote方法不编码/,所以传入safe=''
    # switchUrl = url.replace(':', '%3A').replace('/', '%2F')
    switchUrl = urllib.request.quote(url, safe='')
    # 将标题全文转换伪url编码,使用urllib库里自带quote方法
    switchTitle = urllib.request.quote(title, safe='')
    commentUrl = 'http://engadget.duoshuo.com/api/threads/listPosts.json?thread_key='\
                 + postId + '&url=' + switchUrl + '&title=' + switchTitle + \
                 '&require=site%2Cvisitor%2Cnonce%2Clang%2Cunread%2Clog%2CextraCss' \
                 '&site_ims=1472015826&lang_ims=1472015826&referer=http%3A%2F%2Fcn.engadget.com%2F&v=16.6.16'
    commentPage = urllib.request.urlopen(commentUrl)
    commentJson = commentPage.read().decode('utf-8')
    commentData = json.loads(commentJson)



    print("get")

if __name__=='__main__':
    #with open("config.json", 'r') as jsonFile:
     #   jsonData = json.load(jsonFile)

    url = 'http://cn.engadget.com'
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    # htmlReg = r'<h2 (.*?)</a>'
    # htmlRe = re.compile(htmlReg)
    # contentList = re.findall(htmlRe, html)
    contentList = re.findall(r'<h2 class="h2" itemprop="headline">(.*?)</h2>', html)
    for contentOriginal in contentList:
        # index = contentOriginal.rfind('/">') + 3
        content = re.search(r'/">(.*)</a>', contentOriginal).group(1)
        contentUrl = re.search(r'href="(.*)">', contentOriginal).group(1)
        print('Text:%s Url:%s' % (content, contentUrl))
        getFullContent(content, contentUrl)
    print('all')

