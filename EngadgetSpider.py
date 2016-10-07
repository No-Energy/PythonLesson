# coding=utf-8
import urllib.request  # 自带库，2.#版本引用 urllib即可
import re  # 正则库
import json  # json库
import os  # 系统库
from multiprocessing import Pool  # 线程池
import multiprocessing  # 多进程
import threading  # 线程
import time
import sys


def _down_img(_path, _img_url):
    pic_name = _img_url[_img_url.rindex('/') + 1:]
    file_pic_name = _path + pic_name
    # os.path.join连接两个文件名地址，就比os.path.join("D:\","test.txt")结果是D:\test.txt,需要存在目录
    if not os.path.exists(file_pic_name):
        urllib.request.urlretrieve(_img_url, file_pic_name)
    # print('down %s successful' % pic_name)
    return


def _get_children_comment(_children_index, _children_data, _comment_data_list):
    _children_index += 1
    for post_data in _children_data:
        message = post_data['message']  # .replace('<br />', '')
        likes = post_data['likes']
        name = post_data['author']['name']
        _comment_data_list.append('>' * _children_index + name + ':  ')
        _comment_data_list.append('>' * _children_index + message + ' 推(' + str(likes) + ') \n')
        # print('>' * children_index + name + ':  ')
        # print('>' * children_index + message + ' 推(' + str(likes) + ') \n')
        if not ("children" in post_data):
            continue
        else:
            # 使用递归，依次返回一个主评论的值
            _get_children_comment(_children_index, post_data['children'], _comment_data_list)
    # 节点下所有评论遍历结束，返回
    return


def _get_full_content(get_url, _config_data, _page_id, content_id):
    # 根据地址网址创建本地路径
    title_path = get_url.replace('http://cn.engadget.com', '')
    path = _config_data['path'] + title_path
    image_path = path + 'image/'
    # 检查是否存在路径，若不存在则建立路径, image_path 包含了 path 地址
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    # 读取内容页
    content_page = urllib.request.urlopen(get_url)
    content_html = content_page.read().decode('utf-8')

    # 正则获取标题
    # re搜寻返回结果使用group读取，默认0是匹配原文，1是匹配第一个括号内结果，类推
    title = re.search(r'<title>(.*)</title>', content_html).group(1)

    # 设置正文内容
    # 设置标题
    content = '<h1 class="h1" itemprop="headline">' + title + '</h1>'
    # 设置内容
    content += re.search(r'<div class="copy post-body(.*)<!-- /.post-body -->', content_html, re.DOTALL).group(0)

    # 获取页面内图集地址
    gallery_html_list = re.findall(r'<div class="post-gallery">.*</script>', content, re.DOTALL)
    for gallery_html in gallery_html_list:
        content = content.replace(gallery_html, '/gallery.html')

    # 获取页面内图片网址
    if _config_data['get_img']:
        image_url_list = re.findall(r'src="(.*[jpg|jpeg|gif|png|bmp])"', content)
        # 遍历图片网址下载
        for img_url in image_url_list:
            # 碰到有些地址直接填写类似 //cdn.com/a.jpg
            if img_url.count('http') == 0:
                _down_img(image_path, 'http:' + img_url)
            else:
                _down_img(image_path, img_url)
            # 下载后替换正文内网络地址，更改为本地地址
            file_img_path = image_path + img_url[img_url.rindex('/') + 1:]
            content = re.sub(img_url, file_img_path, content)

    # 匹配获取页面的POST ID
    post_id = re.search(r'var postID = \'(.*)\';', content_html).group(1)
    # 将地址中的:和/转换伪url编码,由于默认quote方法不编码/,所以传入safe=''
    # switchUrl = url.replace(':', '%3A').replace('/', '%2F')
    switch_url = urllib.request.quote(get_url, safe='')
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
        message = post_data['message']  # .replace('<br />', '')
        likes = post_data['likes']
        name = post_data['author']['name']
        comment_data_list.append('>' + name + ':  ')
        comment_data_list.append('>' + message + ' 推(' + str(likes) + ') \n')
        # print('>' + name + ':  ')
        # print('>' + message + ' 推(' + str(likes) + ') \n')
        if "children" in post_data:
            # 第一级子评论
            _get_children_comment(1, post_data['children'], comment_data_list)

    # 输出内容
    file_path = path + 'index.html'
    # open with utf-8 coding if gbk can't convert special code
    f = open(file_path, 'w', encoding='utf-8')
    f.write(content + ''.join(comment_data_list))
    f.close()
    # print('# Text:%s Url:%s' % (title, get_url))
    # print('page: ' + str(page_id) + ' content: ' + str(content_id) + ' ok')
    print('#page: %s content: %s Title: %s' % (_page_id, content_id, title))
    sys.exit(0)


def _get_data_process(_page_url, _page_id, _config):
    page = urllib.request.urlopen(_page_url)
    html = page.read().decode('utf-8')
    del page
    # html_reg = r'<h2 (.*?)</a>'
    # 先对正则表达式建立pattern，方便之后可以重复使用
    # 因为直接送入表达式也会默认生成pattern，且能提高效率，这边只使用一次，无必要
    # html_re = re.compile(htmlReg)
    # content_List = re.findall(htmlRe, html)
    content_url_list = re.findall(r'<a itemprop="url" href="(.*)">', html)
    del html

    content_id = 1
    pool_list = []
    for content_url in content_url_list:
        content_p = multiprocessing.Process(target=_get_full_content, args=(content_url, _config, _page_id, content_id))
        content_p.daemon = True
        content_p.start()
        # content_p.join()
        # del content_p
        pool_list.append(content_p)
        content_id += 1

    for pool in pool_list:
        pool.join()

    # content_id = 1
    # pool = Pool(processes=4)
    # for content_url in content_url_list:
    #     pool.apply(func=_get_full_content, args=(content_url, _config, _page_id, content_id))
    #     content_id += 1
    # pool.close()
    # pool.join()

    # pool.map(_get_full_content, content_url_list)

    print('------page: ' + str(_page_id) + ' ok------')
    sys.exit(0)

    # for content_url in content_url_list:
    #    _get_full_content(content_url)


if __name__ == '__main__':
    pages = 0
    config = {}
    try:
        json_file = open("config.json")
        json_data = json.loads(json_file.read(), 'r')  # r只读;w可写,创建;a追加,创建;w+可读,可写,创建;a+可读,追加,创建
        json_file.close()
        pages = json_data['pages'] + 1
        if len(json_data['path']) > 0:
            config.setdefault('path', json_data['path'])
        else:
            config.setdefault('path', os.getcwd())
        config.setdefault('get_img', json_data['get_img'])
    except IOError:
        print("config file error")

    process_list = []
    for page_id in range(1, pages):
        page_url = 'http://cn.engadget.com/page/' + str(page_id) + '/'
        p = multiprocessing.Process(target=_get_data_process, args=(page_url, page_id, config))
        p.start()
        # del p
        process_list.append(p)

    for process in process_list:
        process.join()

    print('all page down')
