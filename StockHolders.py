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
    def GetDate(self, selector, type="流通股"):
        pattern = ""
        if type == "流通股":
            pattern = "//div[@id='flowholder']//div[@class='m_tab mt15']//a"
        else:
            pattern = "//div[@id='tenholder']//div[@class='m_tab mt15']//a"
        dates = selector.xpath(pattern)
        results = {}
        for item in dates:
            tag  = item.xpath("@targ")
            date = item.xpath("text()")
            results.setdefault(date[0], tag[0])
        return results

    def GetTopStockholder(self, selector, dates, fileName, type="流通股"):
        trPattern = '//*[@id="in_squote"]/div/h1/a[1]/text()'
        codeStr = selector.xpath(trPattern)
        if len(codeStr) != 2:
            return False
        fileStock = open(fileName, "a")
        for date in dates.keys():
            if type == "流通股" :
                trPattern = "//div[@id='flowholder']//div[@id='%s']/table[@class='m_table m_hl ggintro']/tbody/tr"%dates[date]
            else:
                trPattern = "//div[@id='tenholder']//div[@id='%s']/table[@class='m_table m_hl ggintro']/tbody/tr"%dates[date]

            trs = selector.xpath(trPattern)
            patterns = [ 'th']

            for i in range(0, 6):
                patterns.append('td[%d]'%i)

            stockHolders = []
            no = 1
            for tr in trs:
                if no > 10:
                    break
                fileStock.write("同花顺")
                fileStock.write(",%s"%code)
                fileStock.write(",%s"%date)
                fileStock.write(",%d"%no)
                no += 1
                data = []
                for i in range(0, len(patterns)):
                    trSelector = tr.xpath(patterns[i])
                    if(trSelector != None and len(trSelector) > 0):
                        st = trSelector[0].xpath('string()')
                        if(st != None):
                            st = st.replace('\n','').replace('\t','').replace(',',';').replace('\r','').strip()
                            data.append(st)
                            fileStock.write(",%s"%st)
                fileStock.write("\n")
                stockHolders.append(data)
        fileStock.close()
        return True



    def Parse(self, html, fileName, type="流通股"):
        selector = etree.HTML(html.text)
        dates = self.GetDate(selector, type)
        return self.GetTopStockholder(selector, dates, fileName, type)

    def Spider(self, url, fileName, type="流通股"):
        html = requests.get(url)
        if html != None :
            return self.Parse(html, fileName, type)



if __name__ == '__main__':
    codes = Stocks.StockList.GetStockCodes()
    #codes = ['603800']
    url = "http://stockpage.10jqka.com.cn/%s/holder/#tenholder"
    floatingStock = ("流通股", "d://TopFloatingStockHolder.csv")
    stock = ("非流通股", "d://TopStockholder.csv")

    ths = TongHuaShun()
    startTime = time.time()
    type = stock
    for code in codes:
        if ths.Spider(url%code, type[1], type[0]) == True:
            print("%s:OK"%code)
        else:
            print("%s:NG"%code)

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





