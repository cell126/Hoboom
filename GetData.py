# -*- coding: utf-8 -*-

import json
import csv

from DataAPI import Client


if __name__ == "__main__":
    try:
        client = Client()
        client.init('cc1a105d82a1ddc121bc07180bf9c9f4e92fbac5bb0b90b8a0027672047bfe8a')
        url1='/api/market/getMktBlockd.json?field=&beginDate=&endDate=&secID=&ticker=&assetClass=&tradeDate=20160303'
        code, result = client.getData(url1)
        if code==200:
            #print result
            data = json.dumps(result)

            print data

            #csvFile = csv.writer("d:\\thefile.csv", "w")



            if data["retMsg"] == "Success":
                for item in data:
                    print item

                file_object = open('D:\\thefile.csv', 'w')
                file_object.write(result)
                file_object.close()
        else:
            print code
            print result

    except Exception, e:
        #traceback.print_exc()
        pass