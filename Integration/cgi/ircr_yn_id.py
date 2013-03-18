#!/usr/bin/python

import cgi, MySQLdb, sys

def get_fusion_data(dbN, sId) :

    #connect
    db = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db=dbN)
    db.autocommit = True

    #cursor
    cursor = db.cursor()
    cursor.execute("select * from splice_fusion where samp_id = '%s' order by gene_sym1 desc" % sId)
    results = cursor.fetchall()

    content = []
    for record in results:
        row_content = []
        for r in record:
            row_content.append(r)
        content.append(row_content)

    return results

def print_table(table_content):
    print '<b> Sample ID : %s ' % table_content[0][0]

    #print row0 - tableName
    print '''
        <table border="1" cellpadding="0" cellspacing="0">
        <thead>
            <th colspan=9> Fusion </th>'''

    #print row1 - header
    print '''
		<tr>
		<td nowrap>loc1</td>
		<td nowrap>loc2</td>
		<td nowrap>gene_sym1</td>
		<td nowrap>gene_sym2</td>
		<td nowrap>ftype</td>
		<td nowrap>exon1</td>
		<td nowrap>exon2</td>
		<td nowrap>frame</td>
		<td nowrap>nPos</td>
		</tr>
		</thead>
		<tbody>
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
if link.has_key("dbN") :
    dbN = link.getvalue("dbN")
else :
    dbN = "ircr1"

if link.has_key("sId") :
    sId = link.getvalue("sId")
else :
    sId = "S780"

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Sample Detail Page</title>
<link rel="stylesheet" href="/twitter-bootstrap/twitter-bootstrap-v2/docs/assets/css/bootstrap.css">
</head>
<body>
<center>
<a href="/cgi-bin/yn_test/ircr_yn.py">Search by a gene</a> or Search by a Sample ID :
    <form method='get' action="/cgi-bin/yn_test/ircr_yn_id.py">
        <select name="dbN">
            <option value ='ircr1' name='dbN' %s>IRCR GBM</option>
            <option value ='tcga1' name='dbN' %s>TCGA GBM</option>
        </select>
        <input type='text' name='sId' value='%s'>
        <input type='submit' value='Submit'>
    </form>
</center>

'''% (('selected' if dbN=='ircr1' else ''),('selected' if dbN=='tcga1' else ''), sId)
## call function here

table_content = get_fusion_data(dbN, sId)
print_table(table_content)

print('''
</tbody>
</table>
</body>
</html>''')



