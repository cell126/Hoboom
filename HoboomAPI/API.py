# coding=utf-8

# coding=utf-8

import sys

from flask import Flask
from flask.ext import restful

from Resources.StockRecommend import StockRecommend
from Resources.GeneralInfo import GeneralInfo

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
api = restful.Api(app)

api.add_resource(StockRecommend, '/HoboomAPI/v1.0/StockRecommend/<string:code>')
api.add_resource(GeneralInfo, '/HoboomAPI/v1.0/GenaralInfo')

if __name__ == '__main__':
    app.run(debug=True, port=9600, host='0.0.0.0')