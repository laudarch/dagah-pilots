%import MySQLdb
%db = MySQLdb.connect(host="localhost", user="root", passwd="toor")
%cur = db.cursor() 
%cur.execute("USE shevirah")
%cur.execute("SELECT * FROM agents")
%rows = cur.fetchall()
<ul>
%for row in rows :
<li>{{row}}</li>
%end
</ul>