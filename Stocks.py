# coding=utf-8

import requests
import json
import re
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

class StockList:
    Url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(Code)&sr=1&p=1&ps=5000&js=var%20xsBXbefL={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=48516726"

    @staticmethod
    def GetStocks():
        stocks = {}
        html = requests.get(StockList.Url)
        if html != None :
            stocksText = re.findall("data:\[(.*?)\]", html.text)[0]
            stocksList = re.findall(r'"[0-9],(.*?)"', stocksText)
            n = 0
            for item in stocksList :
                stock = re.split(',', item)
                stockCode = stock[0]
                if(re.match('^2\d{5}$', stockCode) != None or re.match('^9\d{5}$', stockCode) != None) :
                    continue
                stockName = stock[1]
                stocks[stockCode] = stockName
            return sorted(stocks.items())

    @staticmethod
    def GetStockCodes():
        StockCodes = []
        html = requests.get(StockList.Url)
        if html != None :
            stocksText = re.findall("data:\[(.*?)\]", html.text)[0]
            stocks = re.findall(r'"[0-9],(.*?)"', stocksText)
            for item in stocks :
                stocks = re.split(',', item)
                stockCode = stocks[0]
                if(re.match('^2\d{5}$', stockCode) != None or re.match('^9\d{5}$', stockCode) != None) :
                    continue
                StockCodes.append(stockCode)
            return StockCodes


if __name__ == '__main__':
    stockList = StockList.GetStocks()
    print(stockList)
    stockCodes = StockList.GetStockCodes()
    print(stockCodes)