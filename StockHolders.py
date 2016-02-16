# coding=utf-8

import re
from lxml import etree
import requests
import time
from multiprocessing.dummy import Pool as ThreadPool
import json
import sys
import re

import Stocks

reload(sys)
sys.setdefaultencoding('utf-8')

class StockHolders:
    def __init__(self):
        self.Code = None
        self.Date = None
        self.Data = None

    def GetCode(self):
        return self.Code

    def SetCode(self, code):
        pattern = r'^\d{6}$'
        re.search(pattern, code)
        if(code != None) :
            self.Code = code

    Code = property(GetCode, SetCode)

    def GetData(self):
        return self.Data

    def SetData(self, data):
        if(data != None and len(data) == 10 and isinstance(data, list)):
            for each in data:
                if(len(each) != 5 or isinstance(each, list)):
                    return
            self.Data = data

    Data = property(GetData, SetData)




class TongHuaShun:
    def GetDate(self, selector):
        pattern = "//div[@id='bd_0']//div[@class='m_tab mt15']//a"
        dates = selector.xpath(pattern)
        results = {}
        for item in dates:
            tag  = item.xpath("@targ")
            date = item.xpath("text()")
            results.setdefault(date[0], tag[0])
        return results


    def GetTopStockholder(self, selector, dates):
        trPattern = "//div[@id='ther_1']/table[@class='m_table m_hl ggintro']/tbody/tr"
        trs = selector.xpath(trPattern)
        patterns = [ 'th']
        for i in range(1, 6):
            patterns.append('td[%d]'%i)

        stockHolders = []
        for tr in trs :
            data = []
            for i in range(0, len(patterns)) :
                trSelector = tr.xpath(patterns[i])
                if(trSelector != None and len(trSelector) > 0):
                    str = trSelector[0].xpath('string()')
                    if(str != None):
                        str = str.encode('utf-8').replace('\n','').replace(' ','').replace('\t','')
                        data.append(str)
            stockHolders.append(data)
        print(stockHolders)


    def Parse(self, html):
        selector = etree.HTML(html.text)
        dates = self.GetDate(selector)
        self.GetTopStockholder(selector, None)

    def Spider(self, url):
        html = requests.get(url)
        if html != None :
            self.Parse(html)


if __name__ == '__main__':
    codes = Stocks.StockList.GetStockCodes()
    url = "http://stockpage.10jqka.com.cn/%s/holder/#tenholder"
    urls = []

    print(codes)
    for code in codes:
        urls.append(url%code)
    print(urls)

    ths = TongHuaShun()
    startTime = time.time()
    for item in urls :
        ths.Spider(item)
    endTime = time.time()
    print("单线程时间%.2f秒"%(endTime - startTime))

'''
    ths = TongHuaShun()

    startTime = time.time()
    pool = ThreadPool(4)
    result = pool.map(ths.Spider, urls)
    pool.close()
    pool.join()
    endTime = time.time()

    print("多线程时间%.2f秒"%(endTime - startTime))
'''





