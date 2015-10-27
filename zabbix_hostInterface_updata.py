#!/usr/bin/env python
#coding:utf8

'''
Created on 27.10.2015
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
    parser.add_option("--ip",action="store",type="string",\
        dest="ip",default="",help="""(REQUIRED)IP address used by the interface. 
Can be empty if the connection is made via DNS.""")
    parser.add_option("--dns",action="store",type="string",\
	dest="dns",default="",help="""(REQUIRED)DNS name used by the interface. 
Can be empty if the connection is made via IP. """)
    parser.add_option("--main",action="store",type="int",\
	dest="main",default="1",help="""(REQUIRED,Default=1)Whether the interface is used as default on the host. Only one interface of some type can be set as default on a host.
Possible values are:
0 - not default;
1 - default.""")
    parser.add_option("--port",action="store",type="string",\
	dest="port",default="10050",help="""(REQUIRED,Default=10050)Port number used by the interface. Can contain user macros.""")
    parser.add_option("--type",action="store",type="int",\
	dest="type",default="1",help="""(REQUIRED,Default=1)Interface type. 
Possible values are:
1 - agent;
2 - SNMP;
3 - IPMI;
4 - JMX. """)
    parser.add_option("--useip",action="store",type="int",\
	dest="useip",default="1",help="""(REQUIRED,Default=1)Whether the connection should be made via IP. 
Possible values are:
0 - connect using host DNS name;
1 - connect using host IP address.""")
    parser.add_option("-f","--file",dest="filename",\
        metavar="FILE",help="""Load values from input file. 
Specify - for standard input Each line of file contains whitespace delimited: 
<hostname>4space<ip>""")

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

    zapi = ZabbixAPI(options.server, options.username, options.password)

    hostname = options.hostname
    ip = options.ip
    main = options.main
    port = options.port
    type = options.type
    useip = options.useip
    dns = options.dns
    file = options.filename

    if file:
        with open(file,"r") as f:
            content = f.readlines()
            for i in content:
                l = i.split("    ")
                n = len(l)
                hostname = l[0].rstrip()
                ip = l[1].rstrip()
                hostid=zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
		interfaceid = zapi.hostinterface.get({"hostids":hostid, "output":"interfaceid"})[0]["interfaceid"]
                print n,'\t',hostname,'\t',interfaceid
                try:
                    msg = zapi.hostinterface.update({"interfaceid":interfaceid, "ip":ip})
		    print msg
                except Exception as e:
                    print str(e)
    else:
        hostid = zapi.host.get({"host":hostname, "output":"hostid"})[0]["hostid"]
	interfaceid = zapi.hostinterface.get({"hostids":hostid, "output":"interfaceid"})[0]["interfaceid"] 
        print hostname,'\t',hostid,'\t',interfaceid
    try:
        msg = zapi.hostinterface.update({"interfaceid":interfaceid, "ip":ip, "main":main, "port":port, "useip":useip, "dns":dns})
	print msg
    except Exception as e:
        print str(e)
