# coding=utf-8

import re
from lxml import etree
import requests
from multiprocessing.dummy import Pool as ThreadPool
import sys
import re
import chardet

import Stocks

reload(sys)
sys.setdefaultencoding('utf-8')



class Brief:
    def GetBrief(self, stockCode=""):
        szPrefix = "szmb"
        shPrefix = "shmb"
        zxPrefix = "szsme"
        cyPrefix = "szcn"
        if(stockCode[0] == '6'):
            prefix = shPrefix
        elif(stockCode[0:3] == '002'):
            prefix = zxPrefix
        elif(stockCode[0:3] == '300'):
            prefix = cyPrefix
        else:
            prefix = szPrefix
        url = "http://www.cninfo.com.cn/information/brief/%s%s.html" %(prefix, stockCode)
        html = requests.get(url)
        print url
        if(html != None):
            selector = etree.HTML(html.content)
            pattern = r'//div[@class="clear"]/table//tr'
            trSelector = selector.xpath(pattern)
            webCode = chardet.detect(html.content)
            row = []
            strPattern = ur"(.*?)：(.*?)$"
            if(trSelector != None):
                for i in range(0, len(trSelector)):
                    st = trSelector[i].xpath('string()').replace('\n','').replace('\t','').replace(',','').replace('\r','').replace(u'万','').strip()
                    result = re.findall(strPattern, st)
                    if(len(result[0]) <= 1):
                        row.append("")
                    else:
                        row.append(result[0][1].strip())
            self.WriteCSV(row, stockCode, ur"d:\公司概况.txt")

    def WriteCSV(self, data, code, fileName):
        with open(fileName, "a") as fileStock:
            fileStock.write("%s"%(code))
            for item in data:
                fileStock.write(",%s"%item)
            fileStock.write("\n")
            fileStock.flush()



if __name__ == '__main__':
    codes = Stocks.StockList.GetStockCodes()
    #codes = ['002235']

    obj = Brief()

    for code in codes:
        print code
'''
        iCode = int(code)
        if(iCode < 2795):
            continue
        else:
            obj.GetBrief(code)
'''