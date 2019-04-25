# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys

""" 
类说明:下载80网小说
Parameters: 无 
Returns: 无 
Modify: 2017-09-13 
"""


class downloader(object):
    def __init__(self):
        self.target = ''
        self.bookName = ''
        self.titleNames = []  # 存放章节名
        self.titleUrls = []  # 存放章节链接
        self.titleNums = 0  # 章节数

    """ 
    函数说明:获取下载链接 
    Parameters: 无 
    Returns: 无 
    Modify: 2017-09-13 
    """

    def get_download_url(self):
        req = requests.get(url=self.target)
        req.encoding = 'utf-8'
        html = req.text
        div_bf = BeautifulSoup(html, 'html.parser')
        titlename = div_bf.find('div', id='titlename')
        h1 = titlename.find('h1')
        self.bookName = (h1.string).replace('全文阅读', '.txt')
        div = div_bf.find('div', id='yulan')
        a = div.find_all('a')
        self.titleNums = len(a)
        for each in a:
            self.titleNames.append(each.string)
            self.titleUrls.append(each.get('href'))

    """ 
    函数说明:获取章节内容 
    Parameters: target - 下载连接(string) 
    Returns: texts - 章节内容(string) 
    Modify: 2017-09-13 
    """

    def get_contents(self, target):
        req = requests.get(url=target)
        req.encoding = 'utf-8'
        html = req.text
        bf = BeautifulSoup(html, 'html.parser')
        texts = bf.find_all('div', id='content')
        brTexts = ''
        if (texts.__len__() > 0):
            # texts = texts[0].text.replace('\xa0' * 8, '\n\n')
            con_l = texts[0].find('br')
            for tagTexts in texts[0]:
                if (type(tagTexts) != type(con_l)):
                    brTexts += tagTexts
        return brTexts

    """ 
    函数说明:将爬取的文章内容写入文件 
    Parameters: name - 章节名称(string) 
    path - 当前路径下,小说保存名称(string) 
    text - 章节内容(string) 
    Returns: 无 
    Modify: 2017-09-13 
    """

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write('\n' + name + '\n')
            f.writelines(text)
            # f.write('\n\n')


if __name__ == "__main__":

    dl = downloader()
    dl.target = input(u'请输入链接：')
    dl.get_download_url()
    print('开始下载：')
    for i in range(dl.titleNums):
        dl.writer(dl.titleNames[i], dl.bookName, dl.get_contents(dl.titleUrls[i]))
        sys.stdout.write(" 已下载:%.3f%%" % float(i / dl.titleNums * 100) + '\r')
        sys.stdout.flush()
    print('下载完成')
