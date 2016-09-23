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
		    hostid=zapi.host.get({"filter":{"host":hostname},"output":"hostid"})[0]["hostid"]
                except Exception as e:
                    print "can not get hostid for host:{0}".format(hostname)
                    continue
		print hostname,'\t',hostid
		try:
		    result = zapi.host.delete([hostid])
		    print result
		except Exception as e:
		    print str(e)
    else:
        hostid=zapi.host.get({"filter":{"host":hostname},"output":"hostid"})[0]["hostid"]
        print hostname,'\t',hostid
	try:
	    result = zapi.host.delete([hostid])
	    print result
	except Exception as e:
	    print str(e)
