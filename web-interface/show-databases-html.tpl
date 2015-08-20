%import MySQLdb
%db = MySQLdb.connect(host="localhost", user="root", passwd="toor")
%cur = db.cursor() 
%cur.execute("show databases")
<ul>
%for row in cur.fetchall() :
    %print row[0]
<li>{{row[0]}}</li>
%end