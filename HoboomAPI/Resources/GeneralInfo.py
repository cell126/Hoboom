# coding=utf-8

import sys

import requests
from flask import Flask
from flask.ext import restful
from flask import abort

from flask import request ;
from flask import json, jsonify;
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.restful import fields, marshal_with

reload(sys)
sys.setdefaultencoding('utf-8')

parser = reqparse.RequestParser()
parser.add_argument('from', type=int, help='from 参数必须是整数', location='args')
parser.add_argument('size', type=int, help='size 参数必须是整数', location='args')

generalInfo_fields = {
    'type'      :   fields.String(attribute='_type'),
    'id'        :   fields.String(attribute='_id'),
    'media'    :   fields.String(attribute='_source.Media'),
    'writer'    :   fields.String(attribute='_source.Writer'),
    'author'    :   fields.String(attribute='_source.Author'),
    'title'     :   fields.String(attribute='_source.InfoTitle'),
    'content'   :   fields.String(attribute='_source.Content'),
    'time'      :   fields.String(attribute='_source.Time')
}

class GeneralInfo(restful.Resource):
    '''

    '''
    query = {
                "from": 0, "size": 10,
                "sort": [
                    {
                        "Time": {
                            "order": "desc"
                        }
                    }
                ]
            }

    url = 'http://139.196.200.24:9200/hoboominfo_v1_0/_search'

    @marshal_with(generalInfo_fields, envelope='results')
    def get(self):
        query = self.query
        args = parser.parse_args()
        print args

        if( args["from"] != None and args["size"] != None):
            size = args["size"]
            if(args["size"] >= 100):
                size = 100
            query["from"] = args["from"]
            query["size"] = size

        data = json.dumps(self.query)
        print data
        html = requests.post(self.url, data=data)

        if(html != None and html.content != None):
            result = json.loads(html.content)
            if(result["hits"]["hits"] != None):
                result = result["hits"]["hits"]
            return result
        else:
            return abort(400)
