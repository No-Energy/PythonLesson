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
    post_id_list = comment_data['response']
    if len(post_id_list) > 0:
        post_data_list = comment_data['parentPosts']

        post_id_list = {}
        for postId in post_data_list:
            post_data = post_data_list[postId]
            # 判断，去除原评论，子评论通过children节点获取,先获取所有父节点，按时间排序
            if len(post_data['parents']) == 0:
                post_id_list.setdefault(postId, post_data['created_at'])
        # 选择值是所有的items，使用lambda方法对item中的第二个值排序
        sort_post_id_list = sorted(post_id_list.items(), key=lambda d: d[1])

        # 按排序结果输出评论，由于排序结果返回已经将字典转化为列(数组)的结构，所以需要在数组值后取前一位
        for sort_post_id in sort_post_id_list:
            post_data = post_data_list[sort_post_id[0]]
            message = post_data['message'].replace('<br />', '')
            likes = post_data['likes']
            name = post_data['author']['name']
            print('>' + name + ':' + message + ' 推(' + str(likes) + ')')
            if "children" in post_data:
                # 第一级子评论
                _get_children_comment(1, post_data['children'])
    else:
        print("no comment")


def _get_children_comment(children_index, children_data):
    children_index += 1
    for post_data in children_data:
        message = post_data['message'].replace('<br />', '')
        likes = post_data['likes']
        name = post_data['author']['name']
        print('>' * children_index + name + ':' + message + ' 推(' + str(likes) + ')')
        if not ("children" in post_data):
            continue
        else:
            # 使用递归，依次返回一个主评论的值
            _get_children_comment(children_index, post_data['children'])
    # 节点下所有评论遍历结束，返回
    return


if __name__=='__main__':
    #with open("config.json", 'r') as jsonFile:
    #   jsonData = json.loads(jsonFile)
    for index in range(1, 10):
        url = 'http://cn.engadget.com/page/' + str(index) + '/'
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

