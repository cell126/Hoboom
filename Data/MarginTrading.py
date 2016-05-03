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

class DFCFMarginTrading:
    def __init__(self):
        self.Url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=MTE&mkt=2&code=%s&st=0&sr=1&p=1&ps=10000"


    def Spider(self, code, fileName):
        html = requests.get(self.Url%code)
        if html != None :
            return self.Parse(html, code, fileName)


    def Parse(self, html, code, fileName):
        data = self.GetMarginTrading(code, html)
        if(data != None):
            self.WriteCSV(data, code, fileName)


    def GetMarginTrading(self, code, html):
        pattern = '"%s,(.*?)"'%code
        dataList = re.findall(pattern, html.text)
        return dataList

    def WriteCSV(self, data, code, fileName):
        with open(fileName, "a") as fileStock:
            for item in data:
                fileStock.write("%s,%s"%("东方财富网", code))
                fileStock.write(",%s"%item)
                fileStock.write("\n")
            fileStock.flush()


if __name__ == '__main__':
    #codes = Stocks.StockList.GetStockCodes()
    codes = ['000001', '000002']

    fileName = u"d://融资融券_东方财富网.csv"

    startTime = time.time()

    ths = DFCFMarginTrading()
    for code in codes:
        ths.Spider(code, fileName)
        print("%s:OK"%code)

    endTime = time.time()
    print("单线程时间%.2f秒"%(endTime - startTime))