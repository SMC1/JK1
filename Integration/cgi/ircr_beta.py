#!/usr/bin/python

import sys, MySQLdb, cgi

conditionL_preH = {
	'ircr1': [
	('"S"', 'sample_tag', 'tag="panel_screening"', '%s','scrn'),
	('"R"', 't_avail_RNASeq', 'True', '%s','RSq'),
	('substring(tag,6)', 'sample_tag', 'tag like "XSeq_%"', '%s','XSq'),
	('substring(tag,6)', 'sample_tag', 'tag like "pair_%"', '%s','pair'),
	('substring(tag,5)', 'sample_tag', 'tag like "tum_%"', '%s','tum'),
	('substring(tag,5)', 'sample_tag', 'tag like "inv_%"', '%s','inv'),
	('z_score', 'array_gene_expr', 'z_score is not NULL', '%4.1f','expr') 
	],
	
	'tcga1': [
	('"R"', 't_avail_RNASeq', 'True', '%s','RSq'),
	('substring(tag,6)', 'sample_tag', 'tag like "XSeq_%"', '%s','XSq'),
	('z_score', 'array_gene_expr', 'z_score is not NULL', '%4.1f','expr'),
	('value_log2', 'array_cn', 'True', '%4.1f','CN') 
	]
	}

conditionL_fusion = [ ('nEvents', 't_fusion', 'frame=True', '%3d', 'on'),
	('nEvents', 't_fusion', 'frame=False', '%3d', 'off')]

def main(dbN,geneN):

	# prep RNA-Seq data availability table
	cursor.execute('create temporary table t_avail_RNASeq as select distinct samp_id from splice_normal')

	# prep exonSkip info
	cursor.execute('select delExons,frame,loc1,loc2 from splice_skip where gene_sym = "%s" group by delExons order by count(*) desc' % geneN)
	results = cursor.fetchall()

	conditionL_exonSkip = []

	for (delExons,frame,loc1,loc2) in results:
		
		if ':Y' in frame:
			frame_code = 'y'
		elif ':N' in frame:
			frame_code = 'n'
		else:
			frame_code = 'u'

		conditionL_exonSkip.append( [
			('nReads', 'splice_skip', 'delExons="%s"' % delExons, '%3d', '%s%s' % (delExons.split(',')[0],frame_code)), \
#			('avg(nReads)', 'splice_normal', 'loc1="%s" or loc2="%s"' % (loc1,loc2), '%d') ])
			('sum(nReads)', 'splice_normal', 'loc1="%s"' % (loc1,), '%d') ])

	# prep mutation info
	cursor.execute('select ch_dna,ch_aa,ch_type,cosmic,count(*) cnt from mutation where gene_sym="%s" group by ch_dna having count(*)>1 order by count(*) desc, cosmic desc' % geneN)
	results = cursor.fetchall()

	conditionL_mutation = []

	for (ch_dna,ch_aa,ch_type,cosmic,cnt) in results:
		
		if cosmic:
			cosmic_fmt = '<font color="red">%s<sub>(%d)</sub></font>'
		else:
			cosmic_fmt = '%s<sub>(%d)</sub>'

		conditionL_mutation.append( [
			('nReads_alt', 'mutation', 'ch_dna="%s"' % ch_dna, '%d', cosmic_fmt % (ch_aa if(ch_aa) else ch_dna, cnt)), \
			('nReads_ref', 'mutation', 'ch_dna="%s"' % ch_dna, '%d') ])

	# prep fusion table
	cursor.execute('create temporary table t_fusion as \
		select samp_id,locate(":Y",frame)>1 frame,count(nPos) nEvents \
		from splice_fusion where (find_in_set("%s",gene_sym1) or find_in_set("%s",gene_sym2)) group by samp_id, locate(":Y",frame)>1' % (geneN,geneN))

	# prep eiJunc info
	cursor.execute('select loc,juncAlias from splice_eiJunc where gene_sym="%s" and nReads>10 group by loc' % geneN)
	results = cursor.fetchall()

	conditionL_eiJunc = []

	for (loc,juncAlias) in results:
		conditionL_eiJunc.append( [
			('nReads', 'splice_eiJunc', 'loc="%s" and nReads>10' % loc, '%3d', juncAlias),
			('sum(nReads)', 'splice_normal', 'loc1="%s"' % (loc,), '%d') ])

#	# prep fusion table
#	cursor.execute('create temporary table t_mut_count as \
#		select samp_id,locate(":Y",frame)>1 frame,count(nPos) nEvents \
#		from splice_fusion where (find_in_set("%s",gene_sym1) or find_in_set("%s",gene_sym2)) group by samp_id, locate(":Y",frame)>1' % (geneN,geneN))

	conditionL = conditionL_preH[dbN] + conditionL_exonSkip + conditionL_fusion + conditionL_eiJunc + conditionL_mutation

	print '<p>%s status of %s panel</p>' % (geneN,dbT_h[dbN])

	cursor.execute('create temporary table t_id as \
		select distinct samp_id from array_gene_expr union select distinct samp_id from splice_skip')

	cursor.execute('alter table t_id add index (samp_id)')

	print('\n<table border="1" cellpadding="0" cellspacing="0">')

	# header: row1
	print '<tr>\n<td rowspan=2></td>',

	for i in range(len(conditionL)):

		row = conditionL[i]

		if type(row) == list:
			row = row[0]

		if i < len(conditionL_preH[dbN]):
			print('<td rowspan=2 align="middle"><div class="verticaltext">%s</div></td>' % row[-1])
		else:
			if i == len(conditionL_preH[dbN]) and len(conditionL_exonSkip)>0:
				print('<td align="middle" colspan=%s>exonSkip (mt/wt)</td>' % len(conditionL_exonSkip))
			elif i == len(conditionL_preH[dbN])+len(conditionL_exonSkip):
				print('<td align="middle" colspan=%s>fusion</td>' % len(conditionL_fusion))
			elif i == len(conditionL_preH[dbN])+len(conditionL_exonSkip)+len(conditionL_fusion):
				print('<td align="middle" colspan=%s>eiJunc</td>' % len(conditionL_eiJunc))
			elif i == len(conditionL_preH[dbN])+len(conditionL_exonSkip)+len(conditionL_fusion)+len(conditionL_mutation):
				print('<td align="middle" colspan=%s>mutation</td>' % len(conditionL_mutation))

	print('\n</tr>\n')

	# header: row2
	print '<tr>\n',

	for i in range(len(conditionL)):

		row = conditionL[i]

		if type(row) == list:
			row = row[0]

		if i < len(conditionL_preH[dbN]):
			pass
		else:
			print('<td height="100"><div class="verticaltext" align="middle">%s</div></td>' % row[-1])

	print('\n</tr>\n')

	cursor.execute('select samp_id from t_id left join array_gene_expr using (samp_id) \
		where gene_sym="%s" or gene_sym is NULL order by z_score desc' % geneN)

	results = cursor.fetchall()

	for (sId,) in results:

		print '<tr>',
		print '<td nowrap>%s</td>' % sId,

		for row in conditionL:

			if type(row) == list:
				row_wt = row[1]
				row = row[0]
			else:
				row_wt = None

			(col,tbl,cnd,fmt) = row[:4]

			cursor.execute('show columns from %s like "gene_sym"' % tbl)

			if cursor.fetchone():
				cnd += ' and gene_sym="%s"' % geneN

			cursor.execute('select %s from %s where samp_id="%s" and %s' % (col,tbl,sId,cnd))
			
			results2 = cursor.fetchall()

			if len(results2) > 1:
				print sId
				raise Exception

			if len(results2) == 1 and results2[0][0] not in (0,'0'):

				value = ('%s' % fmt) % results2[0][0]

				if row_wt:

					(col,tbl,cnd,fmt) = row_wt[:4]

					cursor.execute('select %s from %s where samp_id="%s" and %s' % (col,tbl,sId,cnd))
					
					results_wt = cursor.fetchone()

					if results_wt[0]:
						count_wt = ('%s' % fmt) % results_wt[0]
					else:
						count_wt = 0
	
					print '<td>%s<sub>/%s</sub></td>' % (value, count_wt),

				else:

					print '<td>%s</td>' % value

			else:

				print '<td></td>'

		print '</tr>'

	print('\n</table>\n')


dbT_h = {'ircr1':'IRCR GBM', 'tcga1':'TCGA GBM'}

form = cgi.FieldStorage()

if form.has_key('geneN'):
	geneN = form.getvalue('geneN')
else:
	geneN = 'EGFR'

if form.has_key('dbN'):
	dbN = form.getvalue('dbN')
else:
	dbN = 'ircr1'

if len(sys.argv) >1:
	dbN = sys.argv[1]

con = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db=dbN)

con.autocommit = True
cursor = con.cursor()

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>%s status of %s panel</title>
<style type="text/css">
.verticaltext{
-webkit-transform:rotate(-90deg); writing-mode:tb-rl; -moz-transform:rotate(90deg); -o-transform: rotate(90deg); white-space:nowrap; display:blocking; padding-left:1px;padding-right:1px;padding-top:10px;padding-bottom:10px;
}
</style>
</head>
<body>

<form action='./ircr_beta.py' method='get'>
<input type='hidden' name='dbN' value='ircr1'>
<input type='text' name='geneN'>
<input type='submit' value='Submit'>
</form>

''' % (geneN,dbT_h[dbN])

main(dbN,geneN)

print('''
</body>
</html>''')
