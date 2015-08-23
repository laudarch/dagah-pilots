#!/usr/bin/python
version = "0.1.7"
import os
from os import system
import sys
import re
import serial
from time import sleep
import struct
import pexpect
from lib.serial import read_modem
from lib.config import Config
from lib.db import DB, DBException
from dagah import *
import simplejson as json
config = Config('config')

ipaddress = config.get('IPADDRESS')
webserver = config.get('WEBSERVER')
path = sys.argv[1]
key = sys.argv[2]
sqlserver = config.get('MYSQLSERVER')

while True:
    fullpath5 = webserver + path + "/putfunc"
    PUTFILE = open(fullpath5, 'r+')
    line = PUTFILE.readline()
    line = line.strip()
    PUTFILE.close()
    PUTFILE2 = open(fullpath5, 'w')
    PUTFILE2.close()
    if len(line) > 0:
      arsplit = json.loads(line)
      print arsplit
      if arsplit["apikey"] == key :
	 print "key"
	 if arsplit["command"].lower() == "modem":
		print "modem"
		number = arsplit["number"]
		url = arsplit["url"]
		modemkey = arsplit["key"]
		make_modem(number,url,modemkey)
	 elif arsplit["command"].lower() == "report":
		print webserver + path + "/getfunc"
		reporter("get",webserver + path + "/getfunc")
	 elif arsplit["command"].lower() == "phish" :
           if arsplit["type"].lower() == "basic" :
		url = arsplit["url"]
                label = arsplit["label"]
		numbersarray = arsplit["numbers"]
		text = "This is a cool page: "
		print numbersarray
                for x in numbersarray:
			basicphish(url,text,x,None,label)
           elif arsplit["type"].lower() == "harvester":
		url = arsplit["url"]
                label = arsplit["label"]
                numbersarray = arsplit["numbers"]
                text = "This is a cool page: "
                clone = arsplit["clone"]
		page = "/index.html"
		for x in numbersarray:
		     harvesterphish(url,text,x,None,label,clone,page)
           elif arsplit["type"].lower() == "autoagent":
	    	url = arsplit["url"]
                numbersarray = arsplit["numbers"]
                text = "This is a cool app: "
                backdoorapp = arsplit["app"]
		appkey = arsplit["key"]
                for x in numbersarray:
			autoagentphish(url,text,x,None,None,None,backdoorapp,appkey,None,None,None,"sms")	
	 print "Endloop\n"
    sleep(1)
print "broke\n"
