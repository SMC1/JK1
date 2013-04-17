import MySQLdb


db2dsetN = {'ircr1':'AVATAR GBM', 'tcga1':'TCGA GBM', 'ccle1':'CCLE'}


def connectDB(user='cancer', passwd='cancer', db='ircr1'):

	con = MySQLdb.connect(host="localhost", user=user, passwd=passwd, db=db)

	con.autocommit = True
	cursor = con.cursor()

	return (con,cursor)


def compose_fusion_table(dbN, geneN, sId, flag):

    #connect
    db = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db=dbN)
    db.autocommit = True

    #cursor
    cursor = db.cursor()

    if flag == 'off':
        cursor.execute("select samp_Id, nPos, loc1, loc2, gene_sym1, gene_sym2, ftype from splice_fusion where (find_in_set('%s',gene_sym1) or find_in_set('%s',gene_sym2)) and locate(':Y',frame)=0 and samp_id='%s' order by nPos desc limit 5" % (geneN,geneN,sId))
    else :
        cursor.execute("select samp_Id, nPos, loc1, loc2, gene_sym1, gene_sym2, ftype from splice_fusion where (find_in_set('%s',gene_sym1) or find_in_set('%s',gene_sym2)) and locate(':Y',frame)!=0 and samp_id='%s' order by nPos desc limit 5" % (geneN,geneN,sId))

    results = cursor.fetchall()

    table_content = []
    for record in results:
        row_content = []
        for r in record:
            row_content.append(r)
        table_content.append(row_content)

    html_content = ""
    html_content += '<b> Sample ID : ' + table_content[0][0]

    #print row1 - header
    html_content += '<table border="1" cellpadding="0" cellspacing="0"><tr><td nowrap>nPos</td><td nowrap>loc1</td><td nowrap>loc2</td><td nowrap>gene_sym1</td><td nowrap>gene_sym2</td><td nowrap>ftype</td></tr>'

    #print row2 - data
    for i in range(len(table_content)) :
        row = table_content[i]
        html_content += '<tr>'
        for j in range(len(row)) :
            j += 1
            if not j == len(row) :
                html_content += '<td>'+ str(row[j]) + '</td>'
        html_content += '</tr>'

    html_content += '</table>'

    return html_content
