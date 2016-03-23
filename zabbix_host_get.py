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
    parser.add_option("-f","--file",dest="filename",\
        metavar="FILE",help="Load values from input file. Specify - for standard input Each line of file contains whitespace delimited: <hostname>")

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
    file = options.filename

    if file:
        with open(file,"r") as f:
            host_list = f.readlines()
        for hostname in host_list:
        hostname = hostname.rstrip()
                try:
                    hostinfo = zapi.host.get({"filter":{"host":hostname},"output":"hostid", "selectGroups": "extend", "selectParentTemplates": ["templateid","name"]})[0]
                    hostid = hostinfo["hostid"]
                    host_group_list = []
                    host_template_list = []
                    for l in hostinfo["groups"]:
                        host_group_list.append(l["name"])
                    for t in hostinfo["parentTemplates"]:
                        host_template_list.append(t["name"])
                    #print "host %s exist, hostid : %s, group: %s, template: %s " % (hostname, hostid, host_group_list, host_template_list)
                    print "host %s exist, hostid : %s, group: %s" % (hostname, hostid, host_group_list)
                except:
                    print "host not exist: %s" %hostname
    else:
        try:
            hostinfo = zapi.host.get({"filter":{"host":hostname},"output":"hostid", "selectGroups": "extend", "selectParentTemplates": ["templateid","name"]})[0]
            hostid = hostinfo["hostid"]
            host_group_list = []
            host_template_list = []
            for l in hostinfo["groups"]:
                host_group_list.append(l["name"])
            for t in hostinfo["parentTemplates"]:
                host_template_list.append(t["name"])
            print "host %s exist, hostid : %s, group: %s, template: %s " % (hostname, hostid, host_group_list, host_template_list)
        except:
            print "host not exist: %s" %hostname
