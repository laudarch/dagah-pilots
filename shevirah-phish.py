#!/usr/bin/python
import os
import sys
import time
import subprocess
import signal
import getopt
from lib.config import Config
from lib.db import DB, DBException
config = Config('config')
def usage():
    print "Shevirah-Phish Usage:"
    print "Options:"
    print "-M <type> of attach mobile modem (app/usb)"
    print "\t-n <phone number> of modem"
    print "\t-u <url on webserver> where modem checks in"
    print "\t-k <key> to control modem"
    print "-P <phishing attack> (basic,harvester,autopwn,autoagent)"
    print "\t-u <url on webserver>"
    print "\t-d <delivery method> (sms/nfc)"
    print "\t-n/-N <number/file of numbers> to attack"
    print "\t-p <page name>"
    print "\t-t <custom text> for SMS"
    print "\t-c <page> to clone for credential harvester"
    print "\t-l <label> for campaign"
    print "-A <API> Start API (REST)"
    print "\t-u <url on webserver> for API"
    print "\t-k <api key>"
    print "-S <poller> to shutdown (api, modem, all)"
    print "-R <reporting function> (get, drop)"
def main(argv):
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "M:A:P:n:u:k:S:c:N:p:t:d:l:R:")
    except getopt.GetoptError:
        usage()
        sys.exit()
    modem = False
    api = False
    phish = False
    stop = False
    report = False
    key = "KEYKEY1"
    url = "/modemtest"
    page = "phish.php"
    campaignlabel = "blank"
    number = None
    numberfile = None
    text = "This is a cool page: "

    for opt, arg in opts:
        if opt == '-M':
		modem = True
	if opt == '-A':
		api = True
	if opt == '-P':
		phish = True
		phishtype = arg
        if opt == '-S':
		stop = True
        if opt == '-R':
                report = True
                reporttype = arg
                poller = arg
	if opt == '-n':
		number = arg
	if opt == '-N':
                numberfile = arg
	if opt == '-u':
		url = arg
                if url[0] != '/':
		  url = "/" + url
        if opt == '-p':
                page = arg
                if page[0] != '/':
                   page = "/" + page
	if opt == '-k':
		key = arg
        if opt == '-d':
                deliverymethod = arg
        if opt == '-t':
                text = arg
        if opt == '-l':
                campaignlabel = arg
    if modem == True:
       
	make_modem(number,url,key)
    if api == True:
	make_api(url,key)
    if stop == True:
	stop_poller(poller)
    if report == True:
         reporter(reporttype)
    if phish == True:
       if phishtype == "basic":
	    basicphish(url,text,number,numberfile,campaignlabel)

def reporter(reporttype):
	if reporttype.lower() == "drop": 
		 db = DB(config=config)
	
                 db.query("DROP TABLE IF EXISTS results")
                 db.query("DROP TABLES IF EXISTS campaigns")
        if reporttype.lower() == "get":
                webserver = config.get('WEBSERVER')
 		db = DB(config=config)
		db.query("create table if not exists results (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, label varchar(1000), path varchar(1000), number varchar(12), timestamp varchar(1000), agent varchar(1000))")
        	row = db.fetchone()[0]
        	db.query("SELECT COUNT(*) from campaigns")
                row = db.fetchone()[0]

        	for i in range(1, row+1):
          		db.query("SELECT path from campaigns where id=%s", (i, ))
           		url = db.fetchone()[0]
                        db.query("SELECT label from campaigns where id=%s", (i, ))
                        label = db.fetchone()[0]
			filename = webserver + url + "/results"
			print label + ":" 
			with open(filename) as f:
                   		lines = f.readlines()
                   		for line in lines:
                        		line = line.strip()
					print line
                                        stringsplit = line.split(" ",2)
                                        timestamp = stringsplit[0]
                                        number = stringsplit[1]
                                        agent = stringsplit[2]
                                        db.query("INSERT INTO results (id,label,path,number,timestamp,agent) VALUES (DEFAULT, %s, %s,%s,%s,%s)", (label , url, number, timestamp, agent))


					
            		


def basicphish(url,text,number,numberfile,campaignlabel):
       webserver = config.get('WEBSERVER')
       ipaddress = config.get('IPADDRESS')
       localpath = webserver + url
       if not os.path.exists(localpath):
            command1  = "mkdir " + localpath
            os.system(command1)
       results = localpath + "/results"
       command8   = "touch " + results
       os.system(command8)
       command9 = "chmod 777 " + results
       os.system(command9)
       campaign_db(campaignlabel,url)
       if number != None:
	     makephishpage(number,url)
             fulllink = "http://" + ipaddress + url + "/" + number + ".php"
             fulltext = text + fulllink
	     sendsms(number,fulltext)
       elif numberfile != None:
	     with open(numberfile) as f:
                   lines = f.readlines()
                   for line in lines:
			line = line.strip()
			makephishpage(line,url)
                        fulllink = "http://" + ipaddress + url + "/" + line + ".php"
                        fulltext = text + fulllink
	                sendsms(line,fulltext)

def sendsms(number,text):
        webserver = config.get('WEBSERVER')
	modem = 1
	db = DB(config=config)
        db.query("SELECT path from modems where id=%s", (modem,))
        path2 = db.fetchone()[0].replace('"', '')
        db.query("SELECT controlkey from modems where id=%s", (modem,))
        key2 = db.fetchone()[0]
        db.query("SELECT type from modems where id=%s", (modem,))
        modemtype2 = db.fetchone()[0]
	control = webserver + path2 + "/getfunc"
        with open(control, 'a') as f:
            command2 = key2 + " " + "SEND" + " " + number + " " + text + "\n"
	    f.write(command2)
        print "Sent SMS to " + number

def makephishpage(number,url):
       webserver = config.get('WEBSERVER')
       filename = "/" + number + ".php"
       localpath = webserver + url
       sploitfile = localpath + filename
       command8   = "touch " + sploitfile
       os.system(command8)
       command9 = "chmod 777 " + sploitfile
       os.system(command9)		
       sploitfiletext = "<?php\necho \"You Got Phished!\";\n$agent = $_SERVER['HTTP_USER_AGENT'];\n$page = " + number + ";\n$time = @date('[d/M/Y:H:i:s]');$thing = $time . \" \" . $page . \" \" . $agent;\n$file = results;\n$current = file_get_contents($file);\n$current .= $thing . \"\\n\";\nfile_put_contents($file, $current);\n?>"
       SPLOITFILE = open(sploitfile, 'w')
       SPLOITFILE.write(sploitfiletext)
       SPLOITFILE.close()
		
def stop_poller(poller):
	if poller == "api" or "all":
	  p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
          out, err = p.communicate()
          for line in out.splitlines():
             if 'apipoller.py' in line:
                pid = int(line.split()[1])
                os.kill(pid, signal.SIGKILL)
        if poller == "modem" or "all":	
		p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
          	out, err = p.communicate()
          	for line in out.splitlines():
             		if 'poller.py' in line:
                		pid = int(line.split()[1])
                		os.kill(pid, signal.SIGKILL)
def make_api(path,key):
            make_apifiles(path)
            startcommand = "python apipoller.py " + path + " " + key + " > log"
            pid = os.fork()
            if pid == 0:
                os.system(startcommand)

def make_apifiles(path):
    webserver = config.get("WEBSERVER")
    fullpath = webserver + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    command11 = "chmod 777 " + fullpath
    os.system(command11) 
    getfuncfile = fullpath + "/getfunc"
    command6 = "touch " + getfuncfile
    os.system(command6)
    command7 = "chmod 777 " + getfuncfile
    os.system(command7)
    putfuncfile = fullpath + "/putfunc"
    command6 = "touch " + putfuncfile
    os.system(command6)
    command7 = "chmod 777 " + putfuncfile
    os.system(command7)
    getfuncupload = fullpath + "/getfuncuploader.php"
    command10 = "touch " + getfuncupload
    os.system(command10)
    command11 = "chmod 777 " + getfuncupload
    os.system(command11)
    getfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('getfunc', 'wb');\nfwrite($file, $base);\n?>";
    GETFUNCUPLOADFILE = open(getfuncupload, 'w')
    GETFUNCUPLOADFILE.write(getfuncuploadtext)
    GETFUNCUPLOADFILE.close()
    putfuncupload = fullpath + "/putfuncuploader.php"
    command10 = "touch " + putfuncupload
    os.system(command10)
    command11 = "chmod 777 " + putfuncupload
    os.system(command11)
    putfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('putfunc', 'wb');\nfwrite($file, $base);\n?>";
    PUTFUNCUPLOADFILE = open(putfuncupload, 'w')
    PUTFUNCUPLOADFILE.write(putfuncuploadtext)
    PUTFUNCUPLOADFILE.close()


def check_apache():
	process = os.popen("ps x | grep apache").read().splitlines()
	if len(process) > 2:
		return 1
	else:
		return 0

def check_mysql():
	process = os.popen("netstat -antp | grep mysql").read().splitlines()
	if len(process) == 1:
		return 1
	else:
		return 0
def make_modem(number,url,key):
	make_files2(url)
        if check_apache()== 0:
		os.system("service apache2 start")
        handshake(url,key)
        modemtype = "app"
        database_add2(number,url,key,modemtype)
        startcommand = "python poller.py " + url + " " + key + " > log"
        pid = os.fork()
        if pid == 0:
                os.system(startcommand) 
def campaign_db(label,url):
    if check_mysql() == 0:
	os.system("service mysql start")
    try:
            db = DB(config=config)
    except DBException as e:
        if e[0] == 2:
                   os.system("mysqladmin -u " + config.get("MYSQLUSER") + " create shevirah -p" + config.get("MYSQLPASS"))

        else:
                raise
    db = DB(config=config)

   
    db.query("create table if not exists campaigns (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, label varchar(1000), path varchar(1000))")
    db.query("INSERT INTO campaigns (id,label,path) VALUES (DEFAULT, %s, %s)", (label , url))


def database_add2(number, path, key, _type):
    if check_mysql() == 0:
	os.system("service mysql start")
    try:
            db = DB(config=config)
    except DBException as e:
        if e[0] == 2:
                   os.system("mysqladmin -u " + config.get("MYSQLUSER") + " create shevirah -p" + config.get("MYSQLPASS"))

        else:
                raise
    db = DB(config=config)

    queryes = [
            "DROP TABLE IF EXISTS modems",
        ]
    queryes.append("create table modems (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, number varchar(12), path varchar(1000), controlkey varchar(7), type varchar(3))")
    for query in queryes:
            db.query(query)
    table = "modems"
	

    db.query("INSERT INTO "+table+" (id,number,path,controlkey,type) VALUES (DEFAULT, %s, %s, %s, %s)", (number,path,key, _type))


def handshake(path, key):
    webserver = config.get("WEBSERVER")
    fullpath = webserver + path + "/connect"
    while True:
        f = open(fullpath, 'r+')
        line = f.readline()
        correctstring = key + " CONNECT"
        if line == correctstring:
            command = "\n" + key + " CONNECTED"
            f.write(command)
            f.close()
            print "CONNECTED!\n"
            break
        else:
            f.close()
            time.sleep(1)

         
def make_files2(path):
    webserver = config.get("WEBSERVER")
    fullpath = webserver + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    command11 = "chmod 777 " + fullpath
    os.system(command11) 
    connectfile = fullpath + "/connect"
    command2 = "touch " + connectfile
    os.system(command2)
    command3 = "chmod 777 " + connectfile
    os.system(command3)
    picturefile = fullpath + "/picture.jpg"
    command4 = "touch " + picturefile
    os.system(command4)
    command5 = "chmod 777 " + picturefile
    os.system(command5)
    textfile = fullpath + "/text.txt"
    command6 = "touch " + textfile
    os.system(command6)
    command7 = "chmod 777 " + textfile
    os.system(command7)
    textfile2 = fullpath + "/text2.txt"
    command77 = "touch " + textfile2
    os.system(command77)
    command7777 = "chmod 777 " + textfile2
    os.system(command7777)
    pictureupload = fullpath + "/pictureupload.php"
    command8 = "touch " + pictureupload
    os.system(command8)
    command9 = "chmod 777 " + pictureupload
    os.system(command9)
    pictureuploadtext = "<?php\n$base=$_REQUEST['picture'];\necho $base;\n$binary=base64_decode($base);\nheader('Content-Type: bitmap; charset=utf-8');\n$file = fopen('picture.jpg', 'wb');\nfwrite($file, $binary);\nfclose($file);\n?>";
    PICFILE = open(pictureupload, 'w')
    PICFILE.write(pictureuploadtext)
    PICFILE.close()
    textupload = fullpath + "/textuploader.php"
    command10 = "touch " + textupload
    os.system(command10)
    command11 = "chmod 777 " + textupload
    os.system(command11)
    textuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('text.txt', 'ab');\nfwrite($file, $base);\n?>";
    TEXTFILE = open(textupload, 'w')
    TEXTFILE.write(textuploadtext)
    TEXTFILE.close()
    text2upload = fullpath + "/text2uploader.php"
    command100 = "touch " + text2upload
    os.system(command100)
    command110 = "chmod 777 " + text2upload
    os.system(command110)    
    text2uploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('text2.txt', 'wb');\nfwrite($file, $base);\n?>";
    TEXT2FILE = open(text2upload, 'w')
    TEXT2FILE.write(text2uploadtext)
    TEXT2FILE.close()
    connectupload = fullpath + "/connectuploader.php"
    command12 = "touch " + connectupload
    os.system(command12)
    command13 = "chmod 777 " + connectupload
    os.system(command13)    
    connectuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('connect','wb');\nfwrite($file, $base);\n?>";
    CONNECTFILE = open(connectupload, "w")
    CONNECTFILE.write(connectuploadtext)
    CONNECTFILE.close()
    getfuncfile = fullpath + "/getfunc"
    command6 = "touch " + getfuncfile
    os.system(command6)
    command7 = "chmod 777 " + getfuncfile
    os.system(command7)
    putfuncfile = fullpath + "/putfunc"
    command6 = "touch " + putfuncfile
    os.system(command6)
    command7 = "chmod 777 " + putfuncfile
    os.system(command7)
    getfuncupload = fullpath + "/getfuncuploader.php"
    command10 = "touch " + getfuncupload
    os.system(command10)
    command11 = "chmod 777 " + getfuncupload
    os.system(command11)
    getfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('getfunc', 'wb');\nfwrite($file, $base);\n?>";
    GETFUNCUPLOADFILE = open(getfuncupload, 'w')
    GETFUNCUPLOADFILE.write(getfuncuploadtext)
    GETFUNCUPLOADFILE.close()
    putfuncupload = fullpath + "/putfuncuploader.php"
    command10 = "touch " + putfuncupload
    os.system(command10)
    command11 = "chmod 777 " + putfuncupload
    os.system(command11)
    putfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('putfunc', 'wb');\nfwrite($file, $base);\n?>";
    PUTFUNCUPLOADFILE = open(putfuncupload, 'w')
    PUTFUNCUPLOADFILE.write(putfuncuploadtext)
    PUTFUNCUPLOADFILE.close()
    appupload = fullpath + "/apkupload.php"
    command12 = "touch " + appupload
    os.system(command12)
    command13 = "chmod 777 " + appupload
    os.system(command13)
    appuploadtext = "<?php\n$file_path = basename( $_FILES['uploadedfile']['name']);\n$f = fopen('text.txt', 'wb');\n$data = $file_path;\nfwrite($f, $data);\nfclose($f);\nif(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $file_path)) {\necho 'success';\n} else{\necho 'fail';\n}\n?>"
    APPUPFILE = open(appupload, 'w')
    APPUPFILE.write(appuploadtext)
    APPUPFILE.close()

if __name__ == '__main__':
    main(sys.argv[1:])

