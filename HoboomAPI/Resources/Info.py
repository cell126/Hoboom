# coding=utf-8

import sys

from BaseResource import BaseResource
from TypeResource import TypeResource

reload(sys)
sys.setdefaultencoding('utf-8')


class Info(BaseResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = 'http://139.196.200.24:9200/hoboominfo/_search'


class StockRecommend(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "StockRecommend")

class Announcement(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "Announcement")

class News(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "News")

class GreatEvents(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "GreatEvents")

class AnalyseReport(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "AnalyseReport")

class SpecialNotice(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "SpecialNotice")

class MarketNews(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "MarketNews")

class MarketView(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "MarketView")

class InvestorRa(TypeResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = self.url % ("info", "InvestorRa")
