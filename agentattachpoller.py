#!/usr/bin/python
import time
import os
from lib.config import Config
from lib.db import DB, DBException
config = Config('config')
webserver = config.get("WEBSERVER")
db = DB(config=config)
db.query("SELECT COUNT(*) from agents")
row = db.fetchone()[0]
print row 
Matrix = [[0 for x in range(4)] for x in range(row)] 
for i in range(1, row+1):
      db.query("SELECT number from agents where id=%s", (i, ))
      mynumber = db.fetchone()[0]
      db.query("SELECT path from agents where id=%s", (i, ))
      mypath = db.fetchone()[0]
      db.query("SELECT controlkey from agents where id=%s", (i, ))
      mykey = db.fetchone()[0]
      db.query("SELECT deliverymethod from agents where id=%s", (i, ))
      mymethod = db.fetchone()[0]
      Matrix[i-1][0] = mynumber
      Matrix[i-1][1] = mykey
      Matrix[i-1][2] = mypath
      Matrix[i-1][3] = mymethod
print Matrix
print len(Matrix)
while len(Matrix) > 0:
	for x in range(0,len(Matrix)):
		 method = Matrix[x][3]
		 path = Matrix[x][2]
		 key = Matrix[x][1]
		 if method.lower() == "http" :
                	command = key + " ATTA WEB"
                	control = webserver + path + "/control"
                	f = open(control, 'w')
                	f.write(command)
                	f.close()
	time.sleep(60)
	for x in range(0,len(Matrix)):
                 method = Matrix[x][3]
                 path = Matrix[x][2]
		 number = Matrix[x][0]
		 key = Matrix[x][1]
		 print method
                 if method.lower() == "http" :
			text = webserver + path + "/text.txt"
                	f = open(text, 'r+')
                	line = f.readline()
			print line
                	lines = line.split(',')
                	try:
                        	phonenumber = lines[1]
                	except IndexError:
                        	phonenumber = ''
			print "phone"
			print phonenumber
			if phonenumber == number : 
				Matrix.pop(x)
				query2 = "SELECT id from agents where number=" + number
                		db.query(query2)
                		id = db.fetchone()[0]
                		startcommand = "python agentpoll.py " + path + " " + key + " " + str(id) + " > log2";
				pid = os.fork()
				if pid == 0:
		                        os.system(startcommand)

			f.close()
                	f = open(text, 'w')
                	f.write("")
                	f.close()
			print Matrix
		
