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
import time

import Stocks

reload(sys)
sys.setdefaultencoding('utf-8')

class THSBillboard:
    def __init__(self):
        self.Url = "http://data.10jqka.com.cn/market/lhbcjmx/code/%s"

    def Spider(self, code, fileName):
        html = requests.get(self.Url%code)
        bDate = time.strptime('2016-01-01','%Y-%m-%d')
        if (html != None):
            dates = self.GetDates(html)
            if(dates != None):
                for date in dates:
                    dDate = time.strptime(date,'%Y-%m-%d')
                    '''
                    if(dDate < bDate):
                        continue
                    '''
                    url = self.Url%code + "/date/%s/ajax/1"%date
                    html = requests.get(url)
                    if(html != None):
                        data = self.Parse(html, date)
                        if(data != None):
                            self.WriteCSV(data, code, fileName)


    def Parse(self, html, date):
        selector = etree.HTML(html.text)
        data = self.GetBlockTrade(selector, date)
        return data


    def GetDates(self, html):
        dates = []
        selector = etree.HTML(html.text)
        pattern = '/html/body/div[2]/div[5]/div/select/option'
        trSelector = selector.xpath(pattern)

        for item in trSelector:
            if(trSelector != None and len(trSelector) > 0):
                st = item.xpath('string()')
                if(st != None):
                    dates.append(st)
        return dates


    def GetBlockTrade(self, selector, date):
        divPatterns = "//div[@class='lhb_rank_list']"
        divSelector = selector.xpath(divPatterns)

        pattern = u"】(.*?)$"

        data = []
        for item in divSelector:
            partSelector = item.xpath("div[@class='jj_ggcjmx_title']")
            title = partSelector[0].xpath('string()').replace('\n','').replace('\t','').replace(',','').replace('\r','').strip()
            titleType = re.findall(pattern, title)[0]
            trPattern = 'table/tbody/tr'
            trs = item.xpath(trPattern)
            noOne = 0
            for i in range(0, len(trs)):
                row = []
                tdSelectors = trs[i].xpath("td")
                if(len(tdSelectors) == 1):
                    continue
                j = 0
                row.append(date)
                row.append(titleType)
                for j in range(0, len(tdSelectors)):
                    st = tdSelectors[j].xpath('string()')
                    if(st != None):
                        st = st.replace('\n','').replace('\t','').replace(',','').replace('\r','').replace(' ','').strip()
                    if(j==0):
                        if(st == '1'):
                            noOne = noOne + 1
                        if(noOne == 2):
                            st = '-' + st
                    if(j == 1):
                        strs = re.findall("\d+(.*?)$", st)
                        if(len(strs) > 0):
                            st = strs[0]
                    row.append(st)
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
    codes = Stocks.StockList.GetStockCodes()
    #codes = ['000058']

    fileName = u"d://股价异动_同花顺.csv"

    if os.path.exists(fileName):
        os.remove(fileName)

    startTime = time.time()

    ths = THSBillboard()
    for code in codes:
        ths.Spider(code, fileName)
        print("%s:OK"%code)

    endTime = time.time()
    print("单线程时间%.2f秒"%(endTime - startTime))