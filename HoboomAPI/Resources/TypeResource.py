# coding=utf-8

import sys
import requests

from flask.ext.restful import abort
from flask import Flask
from flask.ext import restful
from flask import abort

from flask import request
from flask import json, jsonify
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.restful import fields, marshal_with

reload(sys)
sys.setdefaultencoding('utf-8')

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


class TypeResource(restful.Resource):
    shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time", "Scope", "Count", "State"]
    url = 'http://139.196.200.24:9200/hoboom%s/%s/'

    @marshal_with(general_fields, envelope='result')
    def get(self, id):
        url = self.url + id
        return self.__processRequest(url)

    def __processRequest(self, url):
        html = requests.get(url)

        if(html != None and html.content != None):
            result = json.loads(html.content)
            return result
        else:
            return abort(400)

class TypeWithDelete(TypeResource):
    shortSource = ["Media", "Writer", "Author", "InfoTitle", "Time", "Scope", "Count", "State"]
    url = 'http://139.196.200.24:9200/hoboom%s/%s/'

    def delete(self, id):
        url = self.url + id
        return self.__processDelete(url)

    def __processDelete(self, url):
        html = requests.delete(url)

        if(html != None and html.content != None):
            result = json.loads(html.content)
            if(result != None and result[u"found"] == True):
                return jsonify({'result': {"found": True}})
            else:
                 return jsonify({'result': {"found": False}})
        else:
            return abort(400)

