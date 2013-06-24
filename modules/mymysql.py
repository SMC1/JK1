#!/usr/bin/python

import MySQLdb

def connectDB(user='cancer', passwd='cancer', db='ircr1'):

	con = MySQLdb.connect(host="localhost", user=user, passwd=passwd, db=db)

	con.autocommit = True
	cursor = con.cursor()

	return (con,cursor)

def dictSelect(sql,cursor):

	cursor.execute(sql)
	results = cursor.fetchall()

	colNameT = zip(*cursor.description)[0]

	dictL = []

	for row in results:
		dictL.append(dict(zip(colNameT,row)))

	return dictL
