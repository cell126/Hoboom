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

class DFCFStockholderNumber:
    def Parse(self, html, code, fileName):
        selector = etree.HTML(html.text)
        data = self.GetStockholderNumber(selector)
        if(data != None):
            self.WriteCSV(data, code, fileName)

    def GetStockholderNumber(self, selector):
        trPattern = '//*[@id="Table0"]//tr'
        trs = selector.xpath(trPattern)
        data = [None] * len(trs)
        for i in range(0, len(trs)):
            if (i == 0):
                pattern = 'th[@class="tips-dataL"]'
            else:
                pattern = 'td'
            tr = trs[i]
            tds = tr.xpath(pattern)
            data[i] = [None] * len(tds)
            for j in range(0, len(tds)):
                    st = tds[j].xpath('string()')
                    if(st != None):
                        st = st.replace('\n','').replace('\t','').replace(',','').replace('\r','').replace(u'万','').strip()
                        if(i == 0):
                            st = "20" + st
                        data[i][j] = st
        return map(list, zip(*data))

    def WriteCSV(self, data, code, fileName):
        with open(fileName, "a") as fileStock:
            for item in data:
                fileStock.write("%s,%s"%("东方财富网", code))
                for field in item:
                    fileStock.write(",%s"%field)
                fileStock.write("\n")
            fileStock.flush()



    def Spider(self, url, code, fileName):
        html = requests.get(url)
        if html != None :
            return self.Parse(html, code, fileName)

if __name__ == '__main__':
    #codes = Stocks.StockList.GetStockCodes()
    codes = ['000004']
    url = "http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=%s"

    fileName = u"d://股东变化_东方财富网.csv"

    startTime = time.time()

    ths = DFCFStockholderNumber()
    for code in codes:
        pre = ""
        if re.match(r'^60\d{4}$', code):
            pre = "sh"
        else:
            pre = "sz"
        ths.Spider(url%(pre + code), code, fileName)
        print("%s:OK"%code)

    endTime = time.time()
    print("单线程时间%.2f秒"%(endTime - startTime))