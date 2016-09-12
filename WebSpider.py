#coding=utf-8
from multiprocessing import Pool  # 线程池
import requests  # 第三方库，类似于urllib.request，是Python较好用的http client
import bs4  # 第三方库，BeautifulSoup
import time


root_url = 'http://wufazhuce.com'


def get_url(num):
    return root_url + '/one/' + str(num)


def get_urls(num):
    urls = map(get_url, range(100,100+num))
    return urls


def get_data(url):
  dataList = ''
  response = requests.get(url)
  if response.status_code != 200:
    return 'noValue'
  soup = bs4.BeautifulSoup(response.text,"html.parser")
  dataList += soup.title.string[4:7]
  for meta in soup.select('meta'):
    if meta.get('name') == 'description':
      dataList += meta.get('content')
  dataList += soup.find_all('img')[1]['src']
  return dataList


if __name__=='__main__':
  pool = Pool(4)
  dataList = []
  urls = get_urls(10)
  start = time.time()
  dataList = pool.map(get_data, urls)
  end = time.time()
  # write = str(repr(dataList).decode('unicode-escape'))
  write=str(dataList)
  print('use: %.2f s' % (end - start))
  print(write)
  f = open("/Users/No_Energy/Documents/data.txt", "w")  # open for writing, the file will be created if the file doesn't exist
  f.write(write) # write text to file
  f.close() # close the file
