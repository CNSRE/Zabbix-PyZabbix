#!/usr/bin/env python
#coding:utf8

'''
Created on 03.06.2015
'''

import optparse
import sys
import traceback
from getpass import getpass
from core import ZabbixAPI

def get_options():
    usage = "usage: %prog [options]"
    OptionParser = optparse.OptionParser
    parser = OptionParser(usage)

    parser.add_option("-s","--server",action="store",type="string",\
        dest="server",help="(REQUIRED)Zabbix Server URL.")
    parser.add_option("-u", "--username", action="store", type="string",\
        dest="username",help="(REQUIRED)Username (Will prompt if not given).")
    parser.add_option("-p", "--password", action="store", type="string",\
        dest="password",help="(REQUIRED)Password (Will prompt if not given).")
    parser.add_option("-H","--hostname",action="store",type="string",\
        dest="hostname",help="(REQUIRED)hostname for hosts.")
    parser.add_option("-n","--name",action="store",type="string",\
        dest="name",help="(REQUIRED)Name of the interface.")
    parser.add_option("-i","--interface",action="store",type="string",\
        dest="interface",default="",help="(REQUIRED,Default:"")key of the interface.")

    options,args = parser.parse_args()

    if not options.server:
        options.server = raw_input('server http:')

    if not options.username:
        options.username = raw_input('Username:')

    if not options.password:
        options.password = getpass()

    return options, args

def errmsg(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(-1)

if __name__ == "__main__":
    options, args = get_options()

    zapi = ZabbixAPI(options.server,options.username, options.password)

    hostname = options.hostname
    name = options.name
    i = options.interface

    #idc=hostname.rstrip('-summary')

    key_responseTime = i+"-responseTime"
    key_0_200 = i+"-0-200"
    key_200_500 = i+"-200-500"
    key_500_1000 = i+"-500-1000"
    key_1000_2000 = i+"-1000-2000"
    key_2000_999999 = i+"-2000-999999"
    key_httpCode_200 = i+"-HttpCode-200"
    key_httpCode_4xx = i+"-HttpCode-400"
    key_httpCode_5xx = i+"-HttpCode-500"

    print key_responseTime,key_0_200,key_httpCode_200,key_httpCode_4xx,key_httpCode_5xx
   
    #hostid = zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
    hostid = zapi.template.get({"filter":{"host":hostname}})[0]["templateid"]
    i_responseTime = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_responseTime}})[0]["itemid"]
    #i_0_200 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_0_200}})[0]["itemid"]
    #i_200_500 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_200_500}})[0]["itemid"]
    #i_500_1000 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_500_1000}})[0]["itemid"]
    #i_1000_2000  = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_1000_2000}})[0]["itemid"]
    #i_2000_999999 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_2000_999999}})[0]["itemid"]
    i_httpCode_200 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_httpCode_200}})[0]["itemid"]
    i_httpCode_4xx = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_httpCode_4xx}})[0]["itemid"]
    i_httpCode_5xx = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_httpCode_5xx}})[0]["itemid"]

    api = "MAPI - "+name
    api_response_time = "MAPI - "+name+" response time"

    print i_responseTime,i_httpCode_200,i_httpCode_4xx,i_httpCode_5xx
    print api,api_response_time

    zapi.graph.create({"name":api,"width":900,"height": 200,"gitems": [{"itemid": i_httpCode_200,"color": "00DD00","drawtype":1,"yaxisside":0,"sortorder":0},{"itemid": i_httpCode_4xx,"color": "DD00DD","drawtype":1,"yaxisside":0,"sortorder":1},{"itemid": i_httpCode_5xx,"color": "DD0000","drawtype":1,"yaxisside":0,"sortorder":2},{"itemid": i_responseTime,"color": "0000DD","drawtype":0,"yaxisside":1,"sortorder":3}]})
    #zapi.graph.create({"name":api_response_time,"width":900,"height": 200,"gitems": [{"itemid": i_0_200,"color": "33FF33","drawtype":1,"yaxisside":0},{"itemid": i_200_500,"color": "008800","drawtype":1,"yaxisside":0},{"itemid": i_500_1000,"color": "CCCC00","drawtype":1,"yaxisside":0},{"itemid": i_1000_2000,"color": "FF3333","drawtype":1,"yaxisside":0},{"itemid": i_2000_999999,"color": "880000","drawtype":1,"yaxisside":0},{"itemid": i_Total_Requests,"color": "CC00CC","drawtype":0,"yaxisside":0},{"itemid": i_responseTime,"color": "0000BB","drawtype":0,"yaxisside":1}]})
