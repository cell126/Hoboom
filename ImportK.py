# coding=utf-8

import xlrd
import threading
import re
import csv
import os

def ProcessKDataFile(fileName, csvfileName):
    postfix = "(\d{6}).\w{2}"
    data = xlrd.open_workbook(fileName, on_demand=True)
    table = data.sheets()[0]

    codeCell = {"row":1, "col":1}
    dataCell = {"row":0, "col":5}

    nrows = table.nrows
    ncols = table.ncols

    fileObject = file(csvfileName, 'ab')
    fileStock = csv.writer(fileObject)

    while True:
        dataCell["row"] = codeCell["row"] - 1
        cell = table.cell(codeCell["row"], codeCell["col"]).value
        if(cell == None):
            break

        code = re.findall(postfix, cell)
        if(code != None):
            code = code[0]
            print code
        else:
            break

        j = 0

        while True:
            row = []
            data = table.cell(dataCell["row"], dataCell["col"] + j).value
            date = "%s-%s-%s" % xlrd.xldate_as_tuple(data, 0)[:3]

            row.append(code)
            row.append(date)

            #fileStock.write("%s,%s" % (code, date))
            for i in range(1, 10):
                data = table.cell(dataCell["row"] + i, dataCell["col"] + j).value
                if(data != ''):
                    row.append(round(data, 4))

            if(len(row) == 11):
                fileStock.writerow(row)

            j += 1
            if(dataCell["col"] + j >= ncols):
                break
        codeCell["row"] += 11
        print "%s/%s" % (codeCell["row"]-2, nrows)
        if codeCell["row"] >= nrows:
            break
    fileObject.close()


if __name__ == '__main__':
    root = r"E:\BaiduYunDownload\虎犇\K线数据"
    root = unicode(root , "utf8")
    excelPattern = "^\S+(.xlsx)"
    csvfileName = r"d:\K%d.txt"
    fileName = r"d:\1.xlsx"

    #fileName = unicode(fileName, "utf8")
    #ProcessKDataFile(fileName, csvfileName)

    threads = []
    for pathes, dirs, files in os.walk(root):
        for f in files:
            fileName =  (r"%s\%s") % (pathes, f)
            if(re.match(excelPattern, fileName) != None):
                print("Process %s" % fileName)
                ProcessKDataFile(fileName, csvfileName)
    print "Finish"



