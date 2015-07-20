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
    parser.add_option("-d","--description",action="store",type="string",\
        dest="description",help="(REQUIRED)Name of the trigger.")
    parser.add_option("-e","--expression",action="store",type="string",\
        dest="expression",help="(REQUIRED)Reduced trigger expression.")
    parser.add_option("-l","--priority",action="store",type="string",\
        dest="priority",default="0",help="""(REQUIRED)Severity of the trigger. 
Possible values are: 
0 - (default) not classified; 
1 - information; 
2 - warning; 
3 - average; 
4 - high; 
5 - disaster.""")
    parser.add_option("-f","--file",dest="filename",\
        metavar="FILE",help="Load values from input file. Specify - for standard input Each line of file contains whitespace delimited: <description>4space<expression>")

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

    description = options.description
    expression = options.expression
    priority = options.priority
    filename = options.filename


    if filename:
        with open(filename,"r") as f:
            content = f.readlines()
            for i in content:
                l = i.split("    ")
		description = l[0].rstrip()
	        expression = l[1].rstrip()
		print description,'\t',expression
		try:
                    zapi.trigger.create({"description":description,"expression":expression,"priority":priority})
		except Exception as e:
		    print str(e)
    else:
	try:
            zapi.trigger.create({"description":description,"expression":expression,"priority":priority})
        except Exception as e:
	    print str(e)
