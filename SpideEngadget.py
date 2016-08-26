# coding=utf-8
import urllib.request  # 自带库，2.#版本引用 urllib即可
import re  # 正则库
import json  # json库


def _get_full_content(title, get_url):
    content_page = urllib.request.urlopen(get_url)
    content_html = content_page.read().decode('utf-8')

    # 匹配获取页面的POST ID
    post_id = re.search(r'var postID = \'(.*)\';', content_html).group(1)
    # 将地址中的:和/转换伪url编码,由于默认quote方法不编码/,所以传入safe=''
    # switchUrl = url.replace(':', '%3A').replace('/', '%2F')
    switch_url = urllib.request.quote(url, safe='')
    # 将标题全文转换伪url编码,使用urllib库里自带quote方法
    switch_title = urllib.request.quote(title, safe='')
    comment_url = 'http://engadget.duoshuo.com/api/threads/listPosts.json?thread_key='\
                 + post_id + '&url=' + switch_url + '&title=' + switch_title + \
                 '&require=site%2Cvisitor%2Cnonce%2Clang%2Cunread%2Clog%2CextraCss' \
                 '&site_ims=1472015826&lang_ims=1472015826&referer=http%3A%2F%2Fcn.engadget.com%2F&v=16.6.16'
    comment_page = urllib.request.urlopen(comment_url)
    comment_json = comment_page.read().decode('utf-8')
    comment_data = json.loads(comment_json)
    print(comment_data)

if __name__=='__main__':
    # with open("config.json", 'r') as jsonFile:
    #   jsonData = json.load(jsonFile)

    url = 'http://cn.engadget.com'
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    # html_reg = r'<h2 (.*?)</a>'
    # 先对正则表达式建立pattern，方便之后可以重复使用
    # 因为直接送入表达式也会默认生成pattern，且能提高效率，这边只使用一次，无必要
    # html_re = re.compile(htmlReg)
    # content_List = re.findall(htmlRe, html)
    content_list = re.findall(r'<h2 class="h2" itemprop="headline">(.*?)</h2>', html)
    for content_original in content_list:
        # index = contentOriginal.rfind('/">') + 3
        content = re.search(r'/">(.*)</a>', content_original).group(1)
        content_url = re.search(r'href="(.*)">', content_original).group(1)
        print('Text:%s Url:%s' % (content, content_url))
        _get_full_content(content, content_url)
    print('all')

