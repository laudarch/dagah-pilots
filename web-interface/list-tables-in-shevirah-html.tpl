%import MySQLdb
%db = MySQLdb.connect(host="localhost", user="root", passwd="toor")
%cur = db.cursor() 
%cur.execute("USE shevirah")
%cur.execute("SHOW TABLES")
%tables = cur.fetchall()
<ul>
%for row in tables :
<li>{{row[0]}}</li>
%end