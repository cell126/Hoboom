# coding=utf-8

import sys

import requests
import copy

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
parser.add_argument('from', type=int, help='from 参数必须是整数', location=['args', 'json'])
parser.add_argument('size', type=int, help='size 参数必须是整数', location=['args', 'json'])
parser.add_argument('abstract', type=bool, help='abstract 参数必须是布尔值', location=['args', 'json'])
parser.add_argument('secuCodes', type=str, action='append', location=['json'])
parser.add_argument('query', type=dict, location=['json'])


general_fields = view_fields = {
    'type'      :   fields.String(attribute='_type'),
    'id'        :   fields.String(attribute='_id'),
    'media'    :    fields.String(attribute='_source.Media'),
    'writer'    :   fields.String(attribute='_source.Writer'),
    'author'    :   fields.String(attribute='_source.Author'),
    'title'     :   fields.String(attribute='_source.InfoTitle'),
    'content'   :   fields.String(attribute='_source.Content'),
    'time'      :   fields.String(attribute='_source.Time'),
    'scope'      :   fields.String(attribute='_source.Scope'),
    'count'      :   fields.String(attribute='_source.Count'),
    'state'      :   fields.String(attribute='_source.State')
}


class BaseResource(restful.Resource):
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
    codeQuery = {
                    #"filter": {
                        "terms": {
                            "SecuCode": ""
                        }
                    #}
                }
    keywordQuery = {
                        #"must": {
                            "multi_match": {
                                "query":    "",
                                "operator" : "and",
                                "fields":   ["InfoTitle", "Content", "Media", "Writer", "Author"]
                            }
                        #}
                    }


    shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time"]

    url = 'http://139.196.200.24:9200/hoboominfo,hoboomview/_search'

    @marshal_with(general_fields, envelope='result')
    def get(self):
        try:
            esQuery = copy.deepcopy(self.query)
            args = parser.parse_args()
            print args

            srcfrom, srcSize = self.__processFromSize(args["from"], args["size"])
            esQuery["from"], esQuery["size"] = srcfrom, srcSize

            if(args["abstract"]):
                esQuery["_source"] = self.shortSource

            data = json.dumps(esQuery)

            result = self.__processRequest(data)
            return result
        except Exception as e:
            return abort(400)


    @marshal_with(general_fields, envelope='result')
    def post(self):
        try:
            esQuery = copy.deepcopy(self.query)
            args = parser.parse_args()
            print args

            srcfrom, srcSize = self.__processFromSize(args["from"], args["size"])
            esQuery["from"], esQuery["size"] = srcfrom, srcSize

            query = {}
            query.setdefault("bool", [])

            if(args["secuCodes"] != None):
                codeQuery = copy.deepcopy(self.codeQuery)
                esQuery["query"] = { "bool": { "filter": ""}}
                esQuery["query"]["bool"]["filter"] = codeQuery
                esQuery["query"]["bool"]["filter"]["terms"]["SecuCode"] = args["secuCodes"]


            if(args["query"] != None):
                keywordQuery = copy.deepcopy(self.keywordQuery)
                if(not esQuery.has_key("query")):
                    esQuery["query"] = { "bool": { "must": ""}}
                esQuery["query"]["bool"]["must"] = keywordQuery
                if(args["query"].has_key("keyword")):
                    esQuery["query"]["bool"]["must"]["multi_match"]["query"] = args["query"]["keyword"]
                    if(args["query"].has_key("fields") and set(args["query"]["fields"]).issubset(keywordQuery["multi_match"]["fields"])):
                        print set(args["query"]["fields"]).issubset(keywordQuery["multi_match"]["fields"])
                        esQuery["query"]["bool"]["must"]["multi_match"]["fields"] = args["query"]["fields"]


            if(args["abstract"]):
                esQuery["_source"] = self.shortSource


            data = json.dumps(esQuery)
            print data

            result = self.__processRequest(data)
            return result
        except Exception as e:
            return abort(400)


    def __processFromSize(self, srcFrom, srcSize):
        if( srcFrom != None and srcSize != None):
            size = srcSize
            if(size >= 50):
                size = 50
            return srcFrom, size
        else:
            return 0, 10


    def __processRequest(self, data):
        html = requests.post(self.url, data=data, timeout=20)

        if(html != None and html.content != None):
            result = json.loads(html.content)
            if(result["hits"]["hits"] != None):
                result = result["hits"]["hits"]
            return result
        else:
            return abort(400)
