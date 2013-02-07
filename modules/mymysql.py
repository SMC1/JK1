#!/usr/bin/python

import MySQLdb


	
mysqlCommand = 'mysql -h canna -u jinkuk --password=privid -D jinkuk '

 
def connectDB():

	con = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db="ircr1")

	con.autocommit = True
	cursor = con.cursor()

	return (con,cursor)
