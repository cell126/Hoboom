# coding=utf8

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

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


class Report:
    '''

    '''
    def __init__(self, type, title, date, organization, author):
        self.Type   = type
        self.Title  = title
        self.Date   = date
        self.Organization = organization
        self.Author = author


class QQReport:
    def __init__(self):
        self.Url = "http://message.finance.qq.com/report/get_report_search.php?n=%s&seq=%s&format=json"


    def Spider(self, path):
        n = 50;
        maxPage = 100
        html = requests.get(self.Url%code)
        if html != None :
            return self.Parse(html, path)


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

