# coding=utf-8

import os
import re
import csv
import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def Process(root, csvfileName):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="8888888",db="hoboom",charset="gbk")
    cursor = conn.cursor()

    pdfPattern = "^\S+(.pdf)"

    fileObject = file(csvfileName, 'ab')

    for pathes, dirs, files in os.walk(root):
        for f in files:
            if(re.match(pdfPattern, f) != None):
                fullName =  (r"%s\%s") % (pathes, f)
                titlePattern = "(.*?)_(.*?)_(.*?)_(.*?)\((.*?)\)(.*?)_(.*?).pdf"
                result = re.findall(titlePattern, f)
                result = list(result[0])
                for i in range(len(result)):
                    print result[i]
                    fileObject.write("%s,"%result[i])
                fileObject.write("%s\n"%fullName)
                fileObject.flush()
    fileObject.close()

if __name__ == '__main__':
    root = r"E:\BaiduYunDownload\虎犇\深度报告"
    root = unicode(root, "utf8")
    csvfileName = r"d:\深度报告文件列表.txt"
    csvfileName = unicode(csvfileName, "utf8")

    Process(root, csvfileName)
