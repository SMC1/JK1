import MySQLdb


db2dsetN = {'ircr1':'AVATAR GBM', 'tcga1':'TCGA GBM', 'ccle1':'CCLE','phillips':'Phillips','IRCR_GBM_352_SCS':'352 SCS', 'IRCR_GBM_363_SCS':'363 SCS', 'RC085_LC195_bulk':'bulk RC'}


def connectDB(user='cancer', passwd='cancer', db='ircr1'):

	con = MySQLdb.connect(host="localhost", user=user, passwd=passwd, db=db)

	con.autocommit = True
	cursor = con.cursor()

	return (con,cursor)


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
