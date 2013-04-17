#!/usr/bin/python

import sys, cgi, re
import mycgi

def linkSamp(text):

	for g in re.findall('(S[0-9]{3})',text):
		text = text.replace(g,'<a href="ircr_samp.py?dbN=%s&sId=%s">%s</a>' % (dbN,g,g))

	return text

def main():

	## sample information

	print '<p><b>%s (%s)</b></p> <p><ul>' % (sId,mycgi.db2dsetN[dbN])

	cursor.execute('select tag from sample_tag where samp_id="%s"' % (sId))
	tags = [x[0] for x in cursor.fetchall()]

	cursor.execute('select 1 from splice_normal where samp_id="%s" limit 1' % (sId))
	avail_RSq = cursor.fetchone()

	# panel_S
	print '<li>Panel: %s' % ', '.join(map(lambda x: x[6:], filter(lambda x: x.startswith('panel_'), tags)))

	# tum,inv
	tL = filter(lambda x: x.startswith('tum_') or x.startswith('inv_'), tags)
	tL.sort(lambda x,y: cmp(y,x))
	print '<li>Phenotype: %s' % ', '.join(tL)

	# data availability
	tL = filter(lambda x: x.startswith('XSeq_'), tags)
	if avail_RSq:
		tL.append('RNA-Seq') 
	print '<li>Available: %s' % ', '.join(tL)
		
	# matched
	text = ','.join(map(lambda x: x[5:], filter(lambda x: x.startswith('pair_'), tags)))
	print '<li>Matched: %s' % linkSamp(text).replace(',',', ')

	print '</ul></p> <font size=2>'

	#census gene
	cursor.execute("select gene_sym from common.census group by gene_sym")
	census_gene = cursor.fetchall()

	## variant information

	for spec in specL:

		(varType,colL,tblN,cond,ordr) = spec

		cursor.execute("select %s from %s where samp_id = '%s' and %s order by %s" % (','.join(colL), tblN, sId, cond, ordr))
		data = cursor.fetchall()

		# theader
		print '''
			<br><b>%s</b> (%s, %s): <a class="expand_%s" href="#">Expand</a> | <a class="collapse_%s" href="#">Collapse</a> | <a href="#" onclick='show("census_gene_%s", "not_census_gene_%s")'>Census</a> | <a onclick="$('tbody tr').show()" href="#">Show all gene</a><br>
			<table border="1" cellpadding="0" cellspacing="0" id="%s">
			<thead>''' % (varType,len(data),('All' if cond=='True' else cond),varType,varType,varType,varType,varType)

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
					if any (content in item for item in census_gene):
						print '<td><a href="ircr.py?dbN=%s&geneN=%s" class="census_gene_%s"> %s </a></td>' % (dbN,row[j],varType,content)
					else:
						print '<td><a href="ircr.py?dbN=%s&geneN=%s" class="not_census_gene_%s"> %s </a></td>' % (dbN, row[j],varType,content)
				elif colN=='ch_type':
					print '<td nowrap> %s </td>' % content
				elif 'coord' in colN:
					print '<td nowrap><a href="http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=%s"> %s </a></td>' % (content[1:],content)
				else:
					print '<td> %s </td>' % content

			print '</tr>'

		print '</tbody></table>'

	print '</font>'

	return

link = cgi.FieldStorage()

if link.has_key("dbN") :
	dbN = link.getvalue("dbN")
else :
	dbN = "tcga1"

if link.has_key("sId") :
	sId = link.getvalue("sId")
else :
	sId = "TCGA-06-5411"

specL = [
	('Mutation', ["concat(strand,chrom,':',chrSta,'-',chrEnd) coord_hg19", "ref", "alt", "nReads_ref", "nReads_alt", \
		"gene_sym", "ch_dna", "ch_aa", "ch_type", "cosmic", "mutsig", "if(census is NULL,'',census) census"], 't_mut', 'True', 'gene_sym,chrSta'),
	('Fusion', ["loc1 coord1", "loc2 coord2", "gene_sym1", "gene_sym2", "ftype", "exon1", "exon2", "frame", "nPos"], 'splice_fusion', 'nPos>2', 'nPos desc'),
	('ExonSkipping', ["loc1 coord1", "loc2 coord2", "gene_sym", "frame", "delExons", "exon1", "exon2", "nReads", "nPos"], 'splice_skip', 'nPos>2', 'nPos desc'),
	('3pDeletion', ["loc coord_hg19", "gene_sym", "juncInfo", "juncAlias", "nReads"], 'splice_eiJunc', 'nReads>5', 'nReads desc')
	]

(con,cursor) = mycgi.connectDB(db=dbN)

cursor.execute('create temporary table t_mut as \
	select mutation.*,concat(tumor_soma,";",tumor_germ,";",mut_type,";",tloc_partner) census \
	from mutation left join census using (gene_sym) where samp_id="%s"' % sId)

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>%s (%s)</title>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.js"></script>
<script type="text/javascript">
$(document).ready(function () {''' % (sId,mycgi.db2dsetN[dbN])

for spec in specL:

	varType = spec[0]

	print '''
			$(".expand_%s").click(function () {
				$("#%s tbody").show("slow");
			});
			$(".collapse_%s").click(function () {
				$("#%s tbody").hide("fast");
			});''' % ((varType,)*4)

print '''
	});

function show(census, notcensus){
$('tbody tr:has(a.'+notcensus+')').hide()   
$('tbody tr:has(a.'+census+')').show()
}

</script>
</head>

<body>
'''

main()

print('''
</body>
</html>''')
