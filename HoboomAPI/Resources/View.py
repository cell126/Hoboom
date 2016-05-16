# coding=utf-8

import sys

from BaseResource import BaseResource
from TypeResource import TypeWithDelete

reload(sys)
sys.setdefaultencoding('utf-8')

class View(BaseResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time", "Scope", "Count", "State"]
        self.url = 'http://139.196.200.24:9200/hoboomview/_search'

class Report(TypeWithDelete):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time", "Scope", "Count", "State"]
        self.url = self.url % ("view", "Report")

class Portfolio(TypeWithDelete):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time", "Scope", "Count", "State"]
        self.url = self.url % ("view", "Portfolio")

class Viewpoint(TypeWithDelete):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time", "Scope", "Count", "State"]
        self.url = self.url % ("view", "Viewpoint")

class Investigate(TypeWithDelete):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time", "Scope", "Count", "State"]
        self.url = self.url % ("view", "Investigate")
