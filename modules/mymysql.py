#!/usr/bin/python

import MySQLdb


	
mysqlCommand = 'mysql -h canna -u jinkuk --password=privid -D jinkuk'

 
def connectDB(user='cancer', passwd='cancer', db='ircr1'):

	con = MySQLdb.connect(host="localhost", user, passwd, db)

	con.autocommit = True
	cursor = con.cursor()

	return (con,cursor)
