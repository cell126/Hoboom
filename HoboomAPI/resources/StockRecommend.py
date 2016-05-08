# coding=utf-8

import re
import requests
import json
import sys
import re

from flask import Flask
from flask.ext import restful
from flask import abort

reload(sys)
sys.setdefaultencoding('utf-8')

class StockRecommend(restful.Resource):
    '''

    '''
    query = {
                "from": 0, "size": 10,
                "query": {
                    "term": {
                        "SecuCode": {
                            "value": "000002"
                        }
                    }
                },
                "sort": [
                    {
                        "Time": {
                            "order": "desc"
                        }
                    }
                ]
            }

    url = 'http://139.196.200.24:9200/hoboominfo_v1_0/_search'

    def get(self, code):
        self.query["query"]["term"]["SecuCode"]["value"] = code
        data = json.dumps(self.query)
        print data
        html = requests.post(self.url, data=data)

        if(html != None and html.content != None):
            print html.content
            return html.content
        else:
            return abort(400)