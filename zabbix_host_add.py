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
    parser.add_option("-g","--groups",action="store",type="string",\
        dest="groups",default="",help="Host groups to add the host to.If you want to use multiple groups,separate them with a ','.")
    parser.add_option("-t","--templates",action="store",type="string",\
	dest="templates",default="0",help="Templates to be linked to the host.If you want to use multiple templates, separate them with a ','. ") 
    parser.add_option("-i","--ip",action="store",type="string",\
	dest="ip",help="(REQUIRED)ip address for hosts.")
    parser.add_option("-n","--name",action="store",type="string",\
	dest="name",help="Visible name of the host.")
    parser.add_option("--proxy",action="store",type="string",\
	dest="proxy",default="",help="name of the proxy that is used to monitor the host.")
    parser.add_option("--status",action="store",type="int",\
        dest="status",default="0",help="""Status and function of the host. 
Possible values are:
0 - (default) monitored host;
1 - unmonitored host.""")
    parser.add_option("-f","--file",dest="filename",\
        metavar="FILE",help="Load values from input file. Specify - for standard input Each line of file contains whitespace delimited: <hostname>4space<ip>4space<groups>4space<templates>")

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
    status = options.status
    ip = options.ip
    name = options.name
    proxy = options.proxy
    file = options.filename
    
    if proxy:
	proxy_id = zapi.proxy.get({"output": "proxyid","selectInterface": "extend","filter":{"host":proxy}})[0]['proxyid']
    else:
	proxy_id = ""

    if file:
        with open(file,"r") as f:
            content = f.readlines()
            for i in content:
                l = i.split("    ")
                hostname = l[0].rstrip()
                ip = l[1].rstrip()
                groups = l[2].rstrip()
                templates = l[3].rstrip()
		groups_id = zapi.hostgroup.get({"output": "groupid","filter": {"name":groups.split(",")}})
		templates_id = zapi.template.get({"output": "templateid","filter": {"host":templates.split(",")}})
                try:
		    print proxy_id
                    if proxy_id:
			print zapi.host.create({"host":hostname,"groups":groups_id,"templates":templates_id,"interfaces":[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":"10050"}],"proxy_hostid":proxy_id,"status":status})
		    else:
			print zapi.host.create({"host":hostname,"groups":groups_id,"templates":templates_id,"interfaces":[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":"10050","status":status}]})
                except Exception as e:
                    print str(e)
    else:
	groups = options.groups
	templates = options.templates
	groups_id = zapi.hostgroup.get({"output": "groupid","filter": {"name":groups.split(",")}})
	templates_id = zapi.template.get({"output": "templateid","filter": {"host":templates.split(",")}})
	try:
	    if proxy_id:
		print zapi.host.create({"host":hostname,"groups":groups_id,"templates":templates_id,"interfaces":[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":"10050"}],"proxy_hostid":proxy_id,"status":status})
	    else:
		print zapi.host.create({"host":hostname,"groups":groups_id,"templates":templates_id,"interfaces":[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":"10050","status":status}]})
	except Exception as e:
	    print str(e)
