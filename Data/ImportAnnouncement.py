# coding=utf-8

import re
from lxml import etree
import requests
import time
from multiprocessing.dummy import Pool as ThreadPool
import json
import MySQLdb
import sys
import re

import Stocks

reload(sys)
sys.setdefaultencoding('utf-8')

class Announcement:
    Code    = None
    Title   = None
    Cate    = None
    Date    = None
    Content = None

    def __init__(self, code, title, date, cate, content):
        self.Code    = code
        self.Title   = title
        self.Cate    = cate
        self.Date    = date
        self.Content = content

    def Imoprt(self):
        result = True
        try:
            conn   = MySQLdb.connect(host="localhost",user="root",passwd="8888888",db="hoboom",charset="utf8")
            cursor = conn.cursor()
            sql    = "insert into hb_data_公告 values(%s,%s,%s,%s,%s)"
            param  = (self.Code, self.Title, self.Date, self.Cate, self.Content)
            result = cursor.execute(sql, param)
        except Exception:
            result = False
        finally:
            cursor.close()
            conn.commit()
            conn.close()
            return result

    def Print(self):
        print "============================"
        print "公司代码 : %s\n标    题 : %s\n日    期 : %s\n公告类型 : %s\n公告内容 : %s" % (self.Code, self.Title, self.Date, self.Cate, self.Content)
        print "============================"


class ImportAnnouncement:
    def GetStockAnnouncement(self, stockCode, startDate="2000-1-1"):
        url = r'http://data.eastmoney.com/notice/%s.html'
        preFix = r'http://data.eastmoney.com'
        startDate = time.strptime(startDate, "%Y-%m-%d")

        url = url%stockCode
        print url
        try:
            html = requests.get(url)
        finally:
            if(html != None):
                selector = etree.HTML(html.text)
                pattern = r"//div[@class='snBox']/div[@class='cont']/ul"
                ulSelector = selector.xpath(pattern)
                if(ulSelector != None and len(ulSelector)>0):
                    ptr = ulSelector[0]
                    titles = ptr.xpath("//li/span[@class='title']/a/@title")
                    cates = ptr.xpath("//li/span[@class='cate']/text()")
                    dates = ptr.xpath("//li/span[@class='date']/text()")
                    hrefs = ptr.xpath("//li/span[@class='title']/a/@href")

                    for i in range(0, len(titles)):
                        title = titles[i]
                        cate  = cates[i]
                        date  = dates[i]
                        href  = hrefs[i]
                        if(i>3):
                            break

                        if( float(time.mktime(time.strptime(date, "%Y-%m-%d"))) < float(time.mktime(startDate))):
                            continue

                        try:
                            content = requests.get(preFix + hrefs[i])
                        except Exception:
                            pass
                        finally:
                            if(content != None and content.text != None):
                                selector = etree.HTML(content.text)
                                patternPre = r'//pre/text()'
                                pre = selector.xpath(patternPre)
                                if(pre != None and len(pre)>0):
                                    content = pre[0].strip()
                                    anno = Announcement(stockCode, title, date, cate, content)
                                    #anno.Print()
                                    time.sleep(1)
                                    if(anno.Imoprt() == False):
                                        return

def Process(stockCode):
    obj = ImportAnnouncement()
    obj.GetStockAnnouncement(stockCode)


if __name__ == '__main__':
    codes = Stocks.StockList.GetStockCodes()
    #codes = ['300245','300379','300231','002235','002281']

    for code in codes:
        iCode = int(code)
        if(iCode <= 600997):
            continue
        else:
            Process(code)

'''
    pool = ThreadPool(processes=4)

    for code in codes:
        print code
        result = pool.apply_async(Process, args = (code, ))
    pool.close()
    pool.join()
    if(result.successful()):
        print 'OK'
'''
