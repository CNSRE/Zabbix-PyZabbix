pyzabbix
========

**pyzabbix** is a python module for working with the [Zabbix API](https://www.zabbix.com/documentation/2.2/manual/api).

The Zabbix API is a web based API and is shipped as part of the web frontend. It uses the JSON-RPC 2.0 protocol which means two things:

*   The API consists of a set of separate methods,like "user.login","item.create",etc.
*   Requests and responses between the clients and the API are encoded using the JSON format.

There are some examples using this method：
```
[root@test Zabbix-PyZabbix]# python zabbix_host_delete.py -h
Usage: zabbix_host_delete.py [options]

Options:
  -h, --help            show this help message and exit
  -s SERVER, --server=SERVER
                        (REQUIRED)Zabbix Server URL.
  -u USERNAME, --username=USERNAME
                        (REQUIRED)Username (Will prompt if not given).
  -p PASSWORD, --password=PASSWORD
                        (REQUIRED)Password (Will prompt if not given).
  -H HOSTNAME, --hostname=HOSTNAME
                        (REQUIRED)hostname for hosts.
  -f FILE, --file=FILE  Load values from input file. Specify - for standard
                        input Each line of file contains whitespace delimited:
                        <hostname>
```
