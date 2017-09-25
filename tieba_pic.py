# -*- coding: utf-8 -*-
# Author: JuneChou

import requests
from urllib import urlencode
from lxml import etree


class Spider():

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
        self.url = 'http://tieba.baidu.com'
        self.picName = 1

    def loadPage(self, url, startPage, endPage):
        resHtml = requests.get(url, self.headers).content

        # 将html页面解析成HTML文档
        selector = etree.HTML(resHtml)
        all_links = selector.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        for link in all_links:
            fullLink = self.url + link
            print '正在获取来自%s的图片' % fullLink
            self.loadImage(fullLink)

    def loadImage(self, link):
        resHtml = requests.get(link, self.headers).content
        selector = etree.HTML(resHtml)
        all_image_links = selector.xpath('//div[@class="d_post_content j_d_post_content "]//img[@class="BDE_Image"]/@src')
        for image_link in all_image_links:
            print '正在下载%s' % image_link
            self.saveImage(image_link)

    def saveImage(self, link):
        filename = './images/' + str(self.picName) + '.jpg'
        with open(filename, 'wb') as f:
            images = requests.get(link, headers=self.headers).content
            f.write(images)
            print '正在将图片另存为%s' % str(self.picName) + '.jpg'
            self.picName += 1


if __name__ == '__main__':
    mySpider = Spider()

    kw = raw_input('请输入贴吧名：')
    startPage = int(raw_input('请输入起始页：'))
    endPage = int(raw_input('请输入结束页：'))
    url = 'https://tieba.baidu.com/f?'
    key = urlencode({'kw': kw})

    for page in range(1, 2):
        pn = (page - 1) * 50
        pn = urlencode({'pn': pn})
        fullUrl = url + key + '&' + pn
        mySpider.loadPage(fullUrl ,startPage, endPage)