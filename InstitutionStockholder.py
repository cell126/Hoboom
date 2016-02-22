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


class DFCFInsitutionStockholder:
    def GetDate(self):
        url = 'http://data.eastmoney.com/zlsj/'
        html = requests.get(url)
        pattern = '//*[@id="Div3"]/div[2]/select/option'
        selector = etree.HTML(html.text)
        dates = selector.xpath(pattern)
        result = []
        for item in dates:
            date = item.xpath('text()')
            result.append(date)
        return result

    def Parse(self, html, date, code, fileName):
        selector = etree.HTML(html.text)
        self.GetInsitutionStockholder(selector, date, code, fileName)

    def GetInsitutionStockholder(self, selector, date, code, fileName):
        fileStock = open(fileName, "a")
        trPattern = '//*[@id="dt_2"]/tbody/tr'
        trs = selector.xpath(trPattern)
        patterns = []
        for i in range(1, 8):
             patterns.append('td[%d]'%i)

        for tr in trs:
            fileStock.write("东方财富网,%s,%s"%(code, date))
            for i in range(0, len(patterns)):
                trSelector = tr.xpath(patterns[i])
                if(trSelector != None and len(trSelector) > 0):
                    st = trSelector[0].xpath('string()')
                    if(st != None):
                        st = st.replace('\n','').replace('\t','').replace(',',';').replace('\r','').strip()
                        if(len(st)>20):
                            continue
                        fileStock.write(",%s"%st)
            fileStock.write("\n")
        fileStock.close()

    def Spider(self, url, date, code, fileName):
        html = requests.get(url)
        if html != None :
            return self.Parse(html, date, code, fileName)



if __name__ == '__main__':
    codes = Stocks.StockList.GetStockCodes()
    #codes = ['000001']
    url = "http://data.eastmoney.com/zlsj/detail/%s-0-%s.html"
    fileName = u"d://机构占比_东方财富网.csv"

    startTime = time.time()

    ths = DFCFInsitutionStockholder()
    dates = ths.GetDate()
    for code in codes:
        date = dates[0]
        ths.Spider(url%(date[0], code), date[0], code, fileName)
        print("%s %s:OK"%(code, date[0]))

    endTime = time.time()
    print("单线程时间%.2f秒"%(endTime - startTime))