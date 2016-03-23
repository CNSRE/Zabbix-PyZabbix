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
    parser.add_option("-t","--templates",action="store",type="string",\
        dest="templates",default="",help="Host template to be updated.If you want to use multiple groups,separate them with a ','.")
    parser.add_option("-f","--file",dest="filename",\
        metavar="FILE",help="Load values from input file. Specify - for standard input Each line of file contains whitespace delimited: <hostname>4space<templates>")

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

def get_list(lists, key):
    l = []
    for i in lists:
        l.append(i[key]) 
    return l

if __name__ == "__main__":
    options, args = get_options()

    zapi = ZabbixAPI(options.server,options.username, options.password)

    file = options.filename

    if file:
        with open(file,"r") as f:
            content = f.readlines()
            for i in content:
                l = i.split("    ")
                hostname = l[0].rstrip()
                hostid=zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
                templates = l[1].rstrip()
                templates_id = zapi.template.get({"output": "templateid","filter": {"host":templates.split(",")}})
                templateids = get_list(templates_id, "templateid")
                try:
                    print zapi.template.massremove({"templateids":templateids,"hostids":hostid})
                except Exception as e:
                    print str(e)
    else:
	templates = options.templates
        hostname = options.hostname
        templates_id = zapi.template.get({"output": "templateid","filter": {"host":templates.split(",")}})
        templateids = get_list(templates_id, "templateid")
        hostid = zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
	try:
            print zapi.template.massremove({"templateids":templateids,"templateids_clear":templateids,"hostids":hostid})
	except Exception as e:
	    print str(e)
