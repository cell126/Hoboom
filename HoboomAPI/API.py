# coding=utf-8

# coding=utf-8

import sys

from flask import Flask
from flask.ext import restful

from Resources.Info import AnalyseReport
from Resources.Info import Announcement
from Resources.Info import GreatEvents
from Resources.Info import Info
from Resources.Info import InvestorRa
from Resources.Info import MarketNews
from Resources.Info import MarketView
from Resources.Info import News
from Resources.Info import SpecialNotice
from Resources.Info import StockRecommend
from Resources.View import Investigate
from Resources.View import Portfolio
from Resources.View import Report
from Resources.View import View
from Resources.View import Viewpoint
from Resources.GeneralInfo import GeneralInfo

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
api = restful.Api(app)

api.add_resource(GeneralInfo, '/HoboomAPI/v1.0/GenaralInfo')
api.add_resource(Info, '/HoboomAPI/v1.0/GenaralInfo/Info')
api.add_resource(View, '/HoboomAPI/v1.0/GenaralInfo/View')

api.add_resource(StockRecommend,    '/HoboomAPI/v1.0/GenaralInfo/StockRecommend/<string:id>')
api.add_resource(Announcement,      '/HoboomAPI/v1.0/GenaralInfo/Announcement/<string:id>')
api.add_resource(News,              '/HoboomAPI/v1.0/GenaralInfo/News/<string:id>')
api.add_resource(GreatEvents,       '/HoboomAPI/v1.0/GenaralInfo/GreatEvents/<string:id>')
api.add_resource(AnalyseReport,     '/HoboomAPI/v1.0/GenaralInfo/AnalyseReport/<string:id>')
api.add_resource(SpecialNotice,     '/HoboomAPI/v1.0/GenaralInfo/SpecialNotice/<string:id>')
api.add_resource(MarketNews,        '/HoboomAPI/v1.0/GenaralInfo/MarketNews/<string:id>')
api.add_resource(MarketView,        '/HoboomAPI/v1.0/GenaralInfo/MarketView/<string:id>')
api.add_resource(InvestorRa,        '/HoboomAPI/v1.0/GenaralInfo/InvestorRa/<string:id>')

api.add_resource(Report,            '/HoboomAPI/v1.0/GenaralInfo/Report/<string:id>')
api.add_resource(Portfolio,         '/HoboomAPI/v1.0/GenaralInfo/Portfolio/<string:id>')
api.add_resource(Viewpoint,         '/HoboomAPI/v1.0/GenaralInfo/Viewpoint/<string:id>')
api.add_resource(Investigate,       '/HoboomAPI/v1.0/GenaralInfo/Investigate/<string:id>')


if __name__ == '__main__':
    app.run(debug=True, port=9600, host='0.0.0.0')