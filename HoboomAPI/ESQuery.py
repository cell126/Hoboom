# coding=utf-8

# coding=utf-8

import re
import requests
import json
import sys
import re

from flask import Flask
from flask.ext import restful

reload(sys)
sys.setdefaultencoding('utf-8')


class StockRecommend(restful.Resource):
    '''

    '''
    def get(self):
        return {'hello': 'world'}


app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(StockRecommend, '/QueryAPI/v1.0/StockRecommend')

if __name__ == '__main__':
    app.run(debug=True, port=9600)

