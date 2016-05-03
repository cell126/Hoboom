# coding=utf-8

import re
from lxml import etree
import requests
import time
from multiprocessing.dummy import Pool as ThreadPool
import json
import sys
import re
import os
import copy

import Stocks

reload(sys)
sys.setdefaultencoding('utf-8')

class THSBlockTrade:
    def __init__(self):
        self.Url = "http://data.10jqka.com.cn/market/dzjy/op/code/code/%s/ajax/1/page/%d/"


    def Spider(self, code, fileName):
        html = requests.get(self.Url%(code,1))

        if (html != None):
            pageNumber = self.GetPageNumber(html)
            if(pageNumber != None):
                pageNumber = int(pageNumber)
                for i in range(1, pageNumber + 1):
                    html = requests.get(self.Url%(code,i))
                    if(html != None):
                        data = self.Parse(html)
                        if(data != None):
                            self.WriteCSV(data, code, fileName)


    def Parse(self, html):
        selector = etree.HTML(html.text)
        data = self.GetBlockTrade(selector)
        return data

    def GetPageNumber(self, html):
        pageNumber = None
        pattern = '/html/body/div[2]/span'
        selector = etree.HTML(html.text)
        tr = selector.xpath(pattern)
        if(len(tr)>0):
            st = tr[0].xpath('string()')
            if(st != None):
                st = st.split('/')
                if(len(st) > 1):
                    pageNumber = st[1]
        return pageNumber

    def GetBlockTrade(self, selector):
        trPattern = '/html/body/table/tbody/tr'
        trs = selector.xpath(trPattern)
        patterns = []
        for i in range(2, 10):
             patterns.append('td[%d]'%i)

        data = []
        dataRow = []

        lastRow = None

        for tr in trs:
            row = []
            for i in range(0, len(patterns)):
                trSelector = tr.xpath(patterns[i])
                if(trSelector != None and len(trSelector) > 0):
                    st = trSelector[0].xpath('string()')
                    if(st != None):
                        st = st.replace('\n','').replace('\t','').replace(',','').replace('\r','').strip()
                        row.append(st)
            if(row in dataRow):
                tradeNo = 2
            else:
                tradeNo = 1
            lastRow = copy.deepcopy(row)
            dataRow.append(lastRow)
            row.append(tradeNo)
            data.append(row)
        return data

    def WriteCSV(self, data, code, fileName):
        with open(fileName, "a") as fileStock:
            for row in data:
                fileStock.write("%s,%s"%("同花顺", code))
                for item in row:
                    fileStock.write(",%s"%item)
                fileStock.write("\n")
            fileStock.flush()


if __name__ == '__main__':
    #codes = Stocks.StockList.GetStockCodes()
    codes = ['000425']

    fileName = u"d://大宗交易_同花顺.csv"

    if os.path.exists(fileName):
        os.remove(fileName)

    startTime = time.time()

    ths = THSBlockTrade()
    for code in codes:
        ths.Spider(code, fileName)
        print("%s:OK"%code)

    endTime = time.time()
    print("单线程时间%.2f秒"%(endTime - startTime))