# -*- coding: utf-8 -*-
import httplib
import traceback
import urllib

import StringIO, gzip
HTTP_OK = 200
HTTP_AUTHORIZATION_ERROR = 401
class Client:
    domain = 'api.wmcloud.com'
    port = 443
    token = ''
    httpClient = None
    def __init__( self ):
        self.httpClient = httplib.HTTPSConnection(self.domain, self.port)
    def __del__( self ):
        if self.httpClient is not None:
            self.httpClient.close()
    def encodepath(self, path):
        #转换参数的编码
        start=0
        n=len(path)
        re=''
        i=path.find('=',start)
        while i!=-1 :
            re+=path[start:i+1]
            start=i+1
            i=path.find('&',start)
            if(i>=0):
                for j in range(start,i):
                    if(path[j]>'~'):
                        re+=urllib.quote(path[j])
                    else:
                        re+=path[j]
                re+='&'
                start=i+1
            else:
                for j in range(start,n):
                    if(path[j]>'~'):
                        re+=urllib.quote(path[j])
                    else:
                        re+=path[j]
                start=n
            i=path.find('=',start)
        return re
    def init(self, token):
        self.token=token
    def getData(self, path):
        result = None
        path='/data/v1'+path
        path=self.encodepath(path)
        print path
        try:
            #set http header here
            self.httpClient.request('GET', path, headers = {"Authorization": "Bearer " + self.token,
                                                            "Accept-Encoding": "gzip, deflate"})
            #make request
            response = self.httpClient.getresponse()
            #read result
            if response.status == HTTP_OK:
                #parse json into python primitive object
                result = response.read()
            else:
                result = response.read()
            compressedstream = StringIO.StringIO(result)
            gziper = gzip.GzipFile(fileobj=compressedstream)
            result = gziper.read()
            if(path.find('.csv?')==-1):
                result=result.decode('utf-8').encode('GB18030')
            return response.status, result
        except Exception, e:
            #traceback.print_exc()
            raise e
        return -1, result