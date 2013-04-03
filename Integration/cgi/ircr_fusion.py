#!/usr/bin/python

import sys, MySQLdb, cgi

def Process(dbN, geneN, sId, flag):

    #connect
    db = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db=dbN)
    db.autocommit = True

    #cursor
    cursor = db.cursor()

    if flag == 'off':
        cursor.execute("select samp_Id, nPos, frame, loc1, loc2, gene_sym1, gene_sym2, ftype, exon1, exon2 from splice_fusion where (find_in_set('%s',gene_sym1) or find_in_set('%s',gene_sym2)) and locate(':Y',frame)=0 and samp_id='%s' order by nPos;" % (geneN,geneN,sId))
    else :
        cursor.execute("select samp_Id, nPos, frame, loc1, loc2, gene_sym1, gene_sym2, ftype, exon1, exon2 from splice_fusion where (find_in_set('%s',gene_sym1) or find_in_set('%s',gene_sym2)) and locate(':Y',frame)!=0 and samp_id='%s' order by nPos;" % (geneN,geneN,sId))

    results = cursor.fetchall()

    content = []
    for record in results:
        row_content = []
        for r in record:
            row_content.append(r)
        content.append(row_content)

    return content

def print_table(table_content):
    print '<b> Sample ID : %s ' % table_content[0][0]

    #print row1 - header
    print '''
		<table border="1" cellpadding="0" cellspacing="0">
		<tr>
		<td nowrap>nPos</td>
		<td nowrap>frame</td>
		<td nowrap>loc1</td>
		<td nowrap>loc2</td>
		<td nowrap>gene_sym1</td>
		<td nowrap>gene_sym2</td>
		<td nowrap>ftype</td>
		<td nowrap>exo1</td>
		<td nowrap>exon2</td>
		</tr>
		'''

    #print row2 - data
    for i in range(len(table_content)) :
        row = table_content[i]
        print '<tr>'
        for j in range(len(row)) :
            j += 1
            if not j == len(row) :
                print '<td nowrap> %s </td>' %row[j]
        print '<tr>'

link = cgi.FieldStorage()
if link.has_key("geneN") :
	geneN = link.getvalue("geneN")
else :
	geneN = "EGFR"

if link.has_key("dbN") :
	dbN = link.getvalue("dbN")
else :
	dbN = "ircr1"

if link.has_key("sId") :
	sId = link.getvalue("sId")
else :
	sId = "S780"

if link.has_key("flag") :
    flag = link.getvalue("flag")
else :
   flag = 'in'

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Fusion Detail</title>
<style type="text/css">
.verticaltext{
-webkit-transform:rotate(-90deg); writing-mode:tb-rl; -moz-transform:rotate(90deg); -o-transform: rotate(90deg); white-space:nowrap; display:blocking; padding-left:1px;padding-right:1px;padding-top:10px;padding-bottom:10px;
}
</style>
</head>
<body>'''

dbN = str(dbN)
table_content = Process(dbN, geneN, sId, flag)
print_table(table_content)

print('''
</body>
</html>''')
