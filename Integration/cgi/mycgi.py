import MySQLdb


def db2dsetN(tbl):
	(con, cursor) = connectDB(db='common')
	cursor.execute('SELECT db_text FROM ircr_db_info WHERE db_name="%s"' % tbl)
	results = cursor.fetchone()

	return(results[0])

def connectDB(user='cancer', passwd='cancer', db='ircr1'):

	con = MySQLdb.connect(host="localhost", user=user, passwd=passwd, db=db)

	con.autocommit = True
	cursor = con.cursor()

	return (con,cursor)

def dbOptions(dbN):
	(con, cursor) = connectDB(db='common')
	cursor.execute('SELECT * FROM ircr_db_info')
	results = cursor.fetchall()

	for (db_name, db_text) in results:
		selected = ''
		if dbN == db_name:
			selected = 'selected'
		print "<option value='%s' name='dbN' %s>%s</option>" % (db_name, selected, db_text)

def getDBL():
	(con, cursor) = connectDB(db='common')
	cursor.execute('SELECT * FROM ircr_db_info')
	results = cursor.fetchall()

	dbL = []
	for (db_name, db_text) in results:
		if db_name not in ['ircr1','tcga1','ccle1','CancerSCAN']:
			dbL.append(db_name)
	return(dbL)

def compose_fusion_table(cursor, dbN, geneN, sId, flag):

	if flag == 'off':
		cursor.execute("select gene_sym1, gene_sym2, ftype, loc1, loc2, nPos, nReads, nReads_w1, nReads_w2 from splice_fusion_AF where (find_in_set('%s',gene_sym1) or find_in_set('%s',gene_sym2)) and locate(':Y',frame)=0 and samp_id='%s' order by nPos desc limit 5" % (geneN,geneN,sId))
	else :
		cursor.execute("select gene_sym1, gene_sym2, ftype, loc1, loc2, nPos, nReads, nReads_w1, nReads_w2 from splice_fusion_AF where (find_in_set('%s',gene_sym1) or find_in_set('%s',gene_sym2)) and locate(':Y',frame)!=0 and samp_id='%s' order by nPos desc limit 5" % (geneN,geneN,sId))

	results = cursor.fetchall()

	html_contentL = []
	html_contentL.append('<b> Sample ID : %s' % sId)

	html_contentL.append('<table border="1" cellpadding="0" cellspacing="0"> <tr> <td nowrap>gene_sym1</td><td nowrap>gene_sym2</td><td nowrap>ftype</td> <td nowrap>loc1</td><td nowrap>loc2</td> <td nowrap>nPos</td> <td nowrap>nReads</td> <td>nReads_w1</td> <td>nReads_w2</td> </tr>')

	for row in results:

		html_line = '<tr>'

		for c in row:
			html_line += '<td>%s</td>' % c
		html_line += '</tr>'

		html_contentL.append(html_line)

	html_contentL.append('</table>')

	return ''.join(html_contentL)

if __name__ == '__main__':
	print db2dsetN('ircr1')
