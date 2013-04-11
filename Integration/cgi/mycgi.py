import MySQLdb

db2dsetN = {'ircr1':'AVATAR GBM', 'tcga1':'TCGA GBM', 'ccle1':'CCLE'}

def connectDB(user='cancer', passwd='cancer', db='ircr1'):

	con = MySQLdb.connect(host="localhost", user=user, passwd=passwd, db=db)

	con.autocommit = True
	cursor = con.cursor()

	return (con,cursor)
