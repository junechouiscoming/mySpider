# -*- encoding:utf-8 -*-
__author__ = 'JuneChou'
__date__ = '2017/9/26 17:06'

import requests
import json, jsonpath
from lxml import etree

class QiuShi():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }
        self.mainurl = 'https://www.qiushibaike.com'

    def getUserUrl(self, url):
        html = requests.get(url, self.headers).content

        # 利用xpath查找用户的链接
        xml_obj = etree.HTML(html)
        userLinkList = xml_obj.xpath('//span[@class="stats-comments"]/a/@href')
        # print userLinkList
        for userLink in userLinkList:
            userFullUrl = self.mainurl + userLink
            self.getUserData(userFullUrl)

    def getUserData(self, url):
        html = requests.get(url, self.headers).content

        xml_obj = etree.HTML(html)

        likeUserLinkList = xml_obj.xpath('//div[@class="like-icon"]/a/@href')
        commentUserLinkList = xml_obj.xpath('//div[@class="comments-list clearfix"]//div[@class="avatars"]/a/@href')
        print commentUserLinkList

    def saveJson(self):
        pass


if __name__ == '__main__':
    page = 1
    fullUrl = 'https://www.qiushibaike.com/8hr/page/' + str(page)

    myQiuShi = QiuShi()
    myQiuShi.getUserUrl(fullUrl)