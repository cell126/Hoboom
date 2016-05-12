# coding=utf-8

import sys

import BaseResource

reload(sys)
sys.setdefaultencoding('utf-8')


class GeneralInfo(BaseResource.BaseResource):
    def __init__(self):
        self.shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]
        self.url = 'http://139.196.200.24:9200/hoboominfo,hoboomview/_search'
