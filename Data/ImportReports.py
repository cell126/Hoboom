# coding=utf8

import dbf
import sys
import MySQLdb
import json
from elasticsearch import Elasticsearch

reload(sys)
sys.setdefaultencoding('utf-8')

class Report:
    ID      = None
    Time    = None
    Media   = None
    Writer  = None
    Author  = None
    Infotitle = None
    Content   = None
    InfoLevel = None
    Data = None

    def __init__(self, id, time, media, writer, author, infoTitle, content, infoLevel):
        self.ID = id
        self.Time = time
        self.Media = media
        self.Writer = writer
        self.Author = author
        self.Infotitle = infoTitle
        self.Content = content
        self.InfoLevel = infoLevel

        self.Data = {}
        self.Data["id"] = self.ID
        self.Data["time"] = self.Time
        self.Data["media"] = self.Media
        self.Data["writer"] = self.Writer
        self.Data["author"] = self.Author
        self.Data["infotitle"] = self.Infotitle
        self.Data["content"] = self.Content
        self.Data["infolevel"] = self.InfoLevel

    def toString(self):
        return ("%s, %s, %s") % (self.ID, self.Time, self.Infotitle)

    def toJson(self):
        return json.dumps(self.Data)


conn = MySQLdb.connect(host="localhost",user="root",passwd="8888888",db="hoboom",charset="gbk")
cursor = conn.cursor()

es = Elasticsearch()

n = cursor.execute("select * from lc_analysereport")
print "Processing..."
all = cursor.fetchall()
for row in all:
    report = Report(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    es.create(index="hoboom", doc_type="report", id=report.ID, body=report.Data)

cursor.close()
print "Finish"


