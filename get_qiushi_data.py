# -*- encoding:utf-8 -*-
__author__ = 'JuneChou'
__date__ = '2017/9/26 17:06'

import requests
import json
from lxml import etree
from bs4 import BeautifulSoup

class QiuShi():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }
        self.mainurl = 'https://www.qiushibaike.com'

    def getUserUrl(self, url):
        html = requests.get(url, self.headers).content

        # 利用xpath查找页面所有帖子所在的位置
        xml_obj = etree.HTML(html)
        results = xml_obj.xpath('//div[contains(@id,"qiushi_tag")]')


        items = []
        for site in results:
            item = {}

            imgUrl = site.xpath('./div[@class="author clearfix"]/a/img/@src')
            if imgUrl != []:
                imgUrl = imgUrl[0].encode('utf-8')
            else:
                imgUrl = '该用户已匿名，无法查看头像地址'

            username = site.xpath('.//img/@alt')[0].encode('utf-8')

            content = site.xpath('.//div[@class="content"]/span')[0].text.strip().encode('utf-8')

            likeNums = site.xpath('.//i')[0].text.encode('utf-8')

            commentNums = site.xpath('.//i')[1].text.encode('utf-8')

            item['imgUrl'] = imgUrl
            item['username'] = username
            item['content'] = content
            item['likeNums'] = likeNums
            item['commentNums'] = commentNums

            items.append(item)

        self.saveJson(items)

    def saveJson(self, list):
        json_obj = json.dumps(list, ensure_ascii=False)
        with open('qiubai.json', 'w') as f:
            f.write(json_obj)


if __name__ == '__main__':
    page = 1
    fullUrl = 'https://www.qiushibaike.com/8hr/page/' + str(page)

    myQiuShi = QiuShi()
    myQiuShi.getUserUrl(fullUrl)