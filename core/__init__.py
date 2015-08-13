#!/bin/bin/env python
#coding:utf-8

import json 
import urllib2

class ZabbixAPI(object):

    def __init__(self,url,user,password,headers = {"Content-Type":"application/json"}):
        self.request_data = {
            "jsonrpc":"2.0",
            "method":"user.login",
            "params":"null",
            "id": 1,
        }
        self.url = url + "/api_jsonrpc.php"
        self.headers = headers
        self.login(user,password)

    def login(self,user,password):
        method = "user.login"
        params = {"user":user,"password":password}
        auth = self.deal_request(method=method,params=params)
        self.request_data["auth"] = auth

    def deal_request(self,method,params):
        self.request_data["method"] = method
        self.request_data["params"] = params
	request = urllib2.Request(url=self.url,data=json.dumps(self.request_data),headers=self.headers)
	try:
	    response = urllib2.urlopen(request)
	    #return json.loads(response.read())["result"]
	    s = json.loads(response.read())
	    return s["result"]
	except Exception as e:
	    print "Error: ",s

    def __getattr__(self,name):
        return ZabbixObj(name,self)

class ZabbixObj(object):

    def __init__(self,method_fomer,ZabbixAPI):
        self.method_fomer = method_fomer
        self.ZabbixAPI = ZabbixAPI

    def __getattr__(self, name):
        def func(params):
            method = self.method_fomer+"."+name
            params = params
            return  self.ZabbixAPI.deal_request(method=method,params=params)
        return func
