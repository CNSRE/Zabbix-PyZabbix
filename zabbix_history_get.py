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
import time

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
    parser.add_option("-H","--hostid",action="store",type="string",\
        dest="hostid",help="(REQUIRED)Return only items that belong to the given hosts.")
    parser.add_option("-G","--groupid",action="store",type="string",\
        dest="groupid",help="(REQUIRED)Return only items that are used in the given graphs.")
    parser.add_option("-P","--graphid",action="store",type="string",\
        dest="graphid",help="(REQUIRED)Return only items that are used in the given graphs.")
    parser.add_option("-f","--time_from",action="store",type="string",\
        dest="time_from",help="(REQUIRED,time format:YYYY-MM-DD HH:MM:SS)Return only values that have been received after or at the given time.")
    parser.add_option("-t","--time_till",action="store",type="string",\
        dest="time_till",help="(REQUIRED,time format:YYYY-MM-DD HH:MM:SS)Return only values that have been received before or at the given time.")

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

    hostid = options.hostid
    groupid = options.groupid
    graphid = options.graphid
    time_from = int(time.mktime(time.strptime(options.time_from,'%Y-%m-%d %H:%M:%S')))
    time_till = int(time.mktime(time.strptime(options.time_till,'%Y-%m-%d %H:%M:%S')))

    item = zapi.item.get({"output": ["itemid", "name"],"hostids":hostid, "graphids":graphid, "groupids":groupid})
    print item
    for key in item:
        print key['name']
        print zapi.history.get({"output":["value", "clock"], "history":0, "itemids":key['itemid'], "sortfield":"clock", "sortorder": "DESC", "time_from":time_from, "time_till":time_till})
