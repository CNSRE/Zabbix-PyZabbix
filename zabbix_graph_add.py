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
    parser.add_option("--pool",action="store",type="string",\
        dest="pool",default="core-pool",help="(REQUIRED,Default:"")the interface pool.")

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
    pool = options.pool

    idc=hostname.rstrip('-summary')

    key_responseTime = i+"-responseTime"
    key_0_200 = i+"-0-200"
    key_200_500 = i+"-200-500"
    key_500_1000 = i+"-500-1000"
    key_1000_2000 = i+"-1000-2000"
    key_2000_999999 = i+"-2000-999999"
    key_Total_Requests = i+"-Total-Requests"
    key_retMsg_FAIL = i+"-retMsg-FAIL"
    key_retMsg_SUCC = i+"-retMsg-SUCC"

    print key_responseTime,key_0_200,key_Total_Requests
   
    hostid = zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
    i_responseTime = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_responseTime}})[0]["itemid"]
    i_0_200 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_0_200}})[0]["itemid"]
    i_200_500 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_200_500}})[0]["itemid"]
    i_500_1000 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_500_1000}})[0]["itemid"]
    i_1000_2000  = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_1000_2000}})[0]["itemid"]
    i_2000_999999 = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_2000_999999}})[0]["itemid"]
    i_Total_Requests = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_Total_Requests}})[0]["itemid"]
    i_retMsg_FAIL = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_retMsg_FAIL}})[0]["itemid"]
    i_retMsg_SUCC = zapi.item.get({"output": "extend","hostids": hostid,"search":{"key_": key_retMsg_SUCC}})[0]["itemid"]

    api = "API ("+pool+") -- "+name
    api_response_time = "API ("+pool+") -- "+name+" response time"
    api_response_time_pie = "API ("+pool+") -- "+name+" response time (pie)"
    api_succ_rate_pie = "API ("+pool+") -- "+name+" succ rate (pie)"

    print i_responseTime,i_0_200,i_200_500,i_500_1000,i_1000_2000,i_2000_999999,i_Total_Requests,i_retMsg_SUCC,i_retMsg_FAIL
    print api,api_response_time,api_response_time_pie,api_succ_rate_pie

    zapi.graph.create({"name":api,"width":900,"height": 200,"gitems": [{"itemid": i_retMsg_FAIL,"color": "CC0000","drawtype":1,"yaxisside":0},{"itemid": i_retMsg_SUCC,"color": "00EE00","drawtype":1,"yaxisside":0},{"itemid": i_Total_Requests,"color": "C800C8","drawtype":0,"yaxisside":0},{"itemid": i_responseTime,"color": "0000BB","drawtype":0,"yaxisside":1}]})
    zapi.graph.create({"name":api_response_time,"width":900,"height": 200,"gitems": [{"itemid": i_0_200,"color": "33FF33","drawtype":1,"yaxisside":0},{"itemid": i_200_500,"color": "008800","drawtype":1,"yaxisside":0},{"itemid": i_500_1000,"color": "CCCC00","drawtype":1,"yaxisside":0},{"itemid": i_1000_2000,"color": "FF3333","drawtype":1,"yaxisside":0},{"itemid": i_2000_999999,"color": "880000","drawtype":1,"yaxisside":0},{"itemid": i_Total_Requests,"color": "CC00CC","drawtype":0,"yaxisside":0},{"itemid": i_responseTime,"color": "0000BB","drawtype":0,"yaxisside":1}]})
    zapi.graph.create({"name":api_response_time_pie,"width":900,"height": 300,"graphtype":2,"gitems": [{"itemid": i_0_200,"color": "33FF33"},{"itemid": i_200_500,"color": "008800"},{"itemid": i_500_1000,"color": "CCCC00"},{"itemid": i_1000_2000,"color": "FF3333"},{"itemid": i_2000_999999,"color": "880000"}]})
    zapi.graph.create({"name":api_succ_rate_pie,"width":900,"height": 300,"graphtype":2,"gitems": [{"itemid": i_retMsg_FAIL,"color": "C80000"},{"itemid": i_retMsg_SUCC,"color": "00EE00"}]})
