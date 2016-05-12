# coding=utf-8

# coding=utf-8

import sys

from flask import Flask
from flask.ext import restful

from HoboomAPI.Resources.Info.Info import Info
from HoboomAPI.Resources.View.View import View
from Resources.GeneralInfo import GeneralInfo

from HoboomAPI.Resources.Info.Info import StockRecommend
from HoboomAPI.Resources.Info.Info import Announcement
from HoboomAPI.Resources.Info.Info import News
from HoboomAPI.Resources.Info.Info import GreatEvents
from HoboomAPI.Resources.Info.Info import AnalyseReport
from HoboomAPI.Resources.Info.Info import SpecialNotice
from HoboomAPI.Resources.Info.Info import MarketNews
from HoboomAPI.Resources.Info.Info import MarketView
from HoboomAPI.Resources.Info.Info import InvestorRa
from HoboomAPI.Resources.View.View import Report
from HoboomAPI.Resources.View.View import Portfolio
from HoboomAPI.Resources.View.View import Viewpoint
from HoboomAPI.Resources.View.View import Investigate

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