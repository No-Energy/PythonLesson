# coding=utf-8
import urllib.request  # 自带库，2.#版本引用 urllib即可
import re  # 正则库
import json  # json库
import os  # 系统库

# 是否下载图片
is_get_img = True


def down_img(path, img_url):
    pic_name = img_url[img_url.rindex('/') + 1:]
    file_pic_name = path + pic_name
    # os.path.join连接两个文件名地址，就比os.path.join("D:\","test.txt")结果是D:\test.txt,需要存在目录
    urllib.request.urlretrieve(img_url, file_pic_name)
    print('down %s.jpg successful' % pic_name)


def _get_children_comment(children_index, children_data, comment_data_list):
    children_index += 1
    for post_data in children_data:
        message = post_data['message']#.replace('<br />', '')
        likes = post_data['likes']
        name = post_data['author']['name']
        comment_data_list.append('>' * children_index + name + ':  ')
        comment_data_list.append('>' * children_index + message + ' 推(' + str(likes) + ') \n')
        # print('>' * children_index + name + ':  ')
        # print('>' * children_index + message + ' 推(' + str(likes) + ') \n')
        if not ("children" in post_data):
            continue
        else:
            # 使用递归，依次返回一个主评论的值
            _get_children_comment(children_index, post_data['children'], comment_data_list)
    # 节点下所有评论遍历结束，返回
    return


def _get_full_content(get_url):
    # 读取内容页
    content_page = urllib.request.urlopen(get_url)
    content_html = content_page.read().decode('utf-8')

    # 正则获取标题
    # re搜寻返回结果使用group读取，默认0是匹配原文，1是匹配第一个括号内结果，类推
    title = re.search(r'<title>(.*)</title>', content_html).group(1)
    print('# Text:%s Url:%s' % (title, get_url))

    # get content by re
    content = re.search(r'<div class="copy post-body(.*)<!-- /.post-body -->', content_html, re.DOTALL).group(0)

    # get image url by re
    image_url_list = []
    if is_get_img:
        image_url_list = re.findall(r'<img alt="" src="(.*[jpg|jpeg|gif|png|bmp])"', content)

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
    post_data_list = comment_data['parentPosts']

    post_id_list = {}
    for postId in post_data_list:
        post_data = post_data_list[postId]
        # 判断，去除原评论，子评论通过children节点获取,先获取所有父节点，按时间排序
        if len(post_data['parents']) == 0:
            post_id_list.setdefault(postId, post_data['created_at'])
    # 选择值是所有的items，使用lambda方法对item中的第二个值排序
    sort_post_id_list = sorted(post_id_list.items(), key=lambda d: d[1])

    comment_data_list = ['\n']
    # 按排序结果输出评论，由于排序结果返回已经将字典转化为列(数组)的结构，所以需要在数组值后取前一位
    for sort_post_id in sort_post_id_list:
        post_data = post_data_list[sort_post_id[0]]
        message = post_data['message']#.replace('<br />', '')
        likes = post_data['likes']
        name = post_data['author']['name']
        comment_data_list.append('>' + name + ':  ')
        comment_data_list.append('>' + message + ' 推(' + str(likes) + ') \n')
        # print('>' + name + ':  ')
        # print('>' + message + ' 推(' + str(likes) + ') \n')
        if "children" in post_data:
            # 第一级子评论
            _get_children_comment(1, post_data['children'], comment_data_list)

    # output full content
    # 输出内容
    title_path = get_url.replace('http://cn.engadget.com', '')
    path = os.getcwd() + title_path
    if len(json_data['path']) > 0:
        path = json_data['path']
    # 检查是否存在路径，若不存在则建立路径
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = path + 'index.html'
    # open with utf-8 coding if gbk can't convert special code
    f = open(file_path, 'w', encoding='utf-8')
    f.write(content + ''.join(comment_data_list))
    f.close()
    print('ok')

    for img_url in image_url_list:
        down_img(path, img_url)

if __name__=='__main__':
    try:
        json_file = open("config.json")
        json_data = json.loads(json_file.read(), 'r')  # r只读;w可写,创建;a追加,创建;w+可读,可写,创建;a+可读,追加,创建
        json_file.close()
    except IOError:
        print("config file error")
    pages = json_data['pages'] + 1
    is_get_img = json_data['get_img']

    for index in range(1, pages):
        url = 'http://cn.engadget.com/page/' + str(index) + '/'
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
        # html_reg = r'<h2 (.*?)</a>'
        # 先对正则表达式建立pattern，方便之后可以重复使用
        # 因为直接送入表达式也会默认生成pattern，且能提高效率，这边只使用一次，无必要
        # html_re = re.compile(htmlReg)
        # content_List = re.findall(htmlRe, html)
        content_url_list = re.findall(r'<a itemprop="url" href="(.*)">', html)
        for content_url in content_url_list:
            _get_full_content(content_url)
    print('all')