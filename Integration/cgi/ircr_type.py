#!/usr/bin/python

import sys, cgi, re
import mycgi

dTypeH = {
    'Fusion': (["samp_id", "gene_sym1", "gene_sym2", "loc1 coord1", "loc2 coord2", "ftype", "exon1", "exon2", "frame", "nPos","nReads","nReads_w1","nReads_w2"], 'splice_fusion_AF', 'nPos>10', 'nPos desc'),
    'ExonSkipping': (["samp_id", "gene_sym", "loc1 coord1", "loc2 coord2", "frame", "delExons", "exon1", "exon2", "nReads", "nPos","nReads","nReads_w1","nReads_w2"], 'splice_skip_AF', 'nPos>20', 'nPos desc'),
	'3pDeletion': (["samp_id","gene_sym", "loc coord_hg19", "juncInfo", "juncAlias", "nReads","nReads_w"], 'splice_eiJunc_AF', 'nReads_w and nReads/nReads_w>=500', '(nReads/nReads_w) desc')
	}

def main():

	(colL,tblN,cond,ordr) = dTypeH[dType]

	cursor.execute("select %s from %s where %s order by %s" % (','.join(colL), tblN, cond, ordr))
	data = cursor.fetchall()

	# theader
	print '''
		<p><b>%s</b> (%s, %s): <a class="expand_%s" href="#">Expand</a> | <a class="collapse_%s" href="#">Collapse</a></p>
		<font size=2>
		<table border="1" cellpadding="0" cellspacing="0" id="%s">
		<thead>''' % (dType,len(data),('All' if cond=='True' else cond),dType,dType,dType)

	print '<tr>'
	for colN in colL:
		print '<td> %s </td>' % colN.split(' ')[-1]
	print '</tr></thead><tbody>'

	# tbody
	for row in data:
		print '<tr>'

		for j in range(len(row)) :
			
			colN = colL[j].split(' ')[-1]

			content = str(row[j]).replace(',',', ').replace('|',', ')

			if colN in ('gene_sym','gene_sym1','gene_sym2'):
				print '<td><a href="ircr.py?dbN=%s&geneN=%s"> %s </a></td>' % (dbN,row[j],content)
			elif colN == "samp_id":
				print '<td><a href="ircr_samp.py?dbN=%s&sId=%s"> %s </a></td>' % (dbN,row[j],content)
			elif colN=='ch_type':
				print '<td nowrap> %s </td>' % content
			elif 'coord' in colN:
				print '<td nowrap><a href="http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=%s"> %s </a></td>' % (content[1:],content)
			else:
				print '<td> %s </td>' % content

		print '</tr>'

	print '</tbody></table></font>'


link = cgi.FieldStorage()

if link.has_key("dbN") :
	dbN = link.getvalue("dbN")
else :
	dbN = "ircr1"

if link.has_key("dType") :
	dType = link.getvalue("dType")
else :
	dType = "3pDeletion"

(con,cursor) = mycgi.connectDB(db=dbN)

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>%s (%s)</title>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.js"></script>
<script type="text/javascript">
$(document).ready(function () {''' % (dType,mycgi.db2dsetN[dbN])

print '''
		$(".expand_%s").click(function () {
			$("#%s tbody").show("slow");
		});
		$(".collapse_%s").click(function () {
			$("#%s tbody").hide("fast");
		});''' % ((dType,)*4)

print '''
	});

</script>
</head>

<body>
'''

if dType in dTypeH:
	main()
else:
	print '%s is not supported yet.<br><br>' % dType
	print 'Try instead: %s' % ', '.join(dTypeH.keys())

print('''
</body>
</html>''')
