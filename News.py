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
import chardet

reload(sys)
sys.setdefaultencoding('utf-8')


class ZZNews:
    def __init__(self):
        self.Url = "http://www.cs.com.cn/gppd/zzkpd/01/index_%d.html"

    def Spider(self, fileName):
        newsList = self.GetNewsList()

    def GetNewsList(self):
        pattern = "/html/body/div[7]/div[3]/div[1]/ul/li"
        for i in range(1, 10):
            html = requests.get(self.Url%i)
            if(html != None):
                selector = etree.HTML(html.text)
                liSelectors = selector.xpath(pattern)
                print(len(liSelectors))
                for j in range(1, len(liSelectors) + 1):
                    patternTime = "/html/body/div[7]/div[3]/div[1]/ul/li[%d]//span"%j
                    timeSelector = selector.xpath(patternTime)
                    time = timeSelector[0].xpath("string()")
                    if(time != None):
                        time = time.replace('\n','').replace('\t','').replace(',','').replace('\r','').replace(' ','').replace('(','').replace(')','').strip()
                        date = re.findall('^(\d{2}-\d{2})', time)[0]
                        time = re.findall('^\d{2}-\d{2}(.*?)$', time)[0]
                    patternTitle = "/html/body/div[7]/div[3]/div[1]/ul/li[%d]//a"%j
                    titleSelector = selector.xpath(patternTitle)
                    title = titleSelector[0].xpath("string()")
                    if(title != None):
                        print (date, time, title)


    def WriteCSV(self, data, code, fileName):
        with open(fileName, "a") as fileStock:
            for row in data:
                fileStock.write("%s"%"中证")
                for item in row:
                    fileStock.write(",%s"%item)
                fileStock.write("\n")
            fileStock.flush()



if __name__ == '__main__':
    fileName = u"d://中证看盘_中证.csv"

    if os.path.exists(fileName):
        os.remove(fileName)

    startTime = time.time()

    ths = ZZNews()
    ths.Spider(fileName)

    endTime = time.time()
    print("单线程时间%.2f秒"%(endTime - startTime))