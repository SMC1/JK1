#!/usr/bin/python

import sys, cgi
import mycgi


conditionL_preH = {
	'ircr1': [
		('"S"', 'sample_tag', 'tag="panel_screening"', '%s','scrn'),
		('"R"', 't_avail_RNASeq', 'True', '%s','RSq'),
		('substring(tag,6)', 'sample_tag', 'tag like "XSeq_%"', '%s','XSq'),
		('substring(tag,6)', 'sample_tag', 'tag like "pair_%"', '%s','pair'),
		('substring(tag,5)', 'sample_tag', 'tag like "tum_%"', '%s','tum'),
		('substring(tag,5)', 'sample_tag', 'tag like "inv_%"', '%s','inv'),
		('z_score', 'array_gene_expr', 'z_score is not NULL', '%4.1f','expr'),
		('expr_MAD', 'array_gene_expr_MAD', 'expr_MAD is not NULL', '%4.1f', 'expr<br><sup>(MAD'),
		('value_log2', 'array_cn', 'True', '%4.1f','CN'),
		('rpkm', 'rpkm_gene_expr', 'rpkm is not NULL', '%4.1f','RPKM')
	],

	'tcga1': [
		('"R"', 't_avail_RNASeq', 'True', '%s','RSq'),
		('substring(tag,6)', 'sample_tag', 'tag like "XSeq_%"', '%s','XSq'),
		('substring(tag,1,3)', 'sample_tag', 'tag="Recur" or tag="Sec"', '%s','R/S'),
		('z_score', 'array_gene_expr', 'z_score is not NULL', '%4.1f','expr'),
		('expr_MAD', 'array_gene_expr_MAD', 'expr_MAD is not NULL', '%4.1f', 'expr<br><sup>(MAD'),
		('value_log2', 'array_cn', 'True', '%4.1f','CN'),
		('rpkm', 'rpkm_gene_expr', 'rpkm is not NULL', '%4.1f','RPKM')
	],

	'ccle1': [
		('z_score', 'array_gene_expr', 'z_score is not NULL', '%4.1f','expr'),
		('expr_MAD', 'array_gene_expr_MAD', 'expr_MAD is not NULL', '%4.1f', 'expr<br><sup>(MAD'),
		('value_log2', 'array_cn', 'True', '%4.1f','CN')
	]

}

conditionL_fusion = [ ('nEvents', 't_fusion', 'frame=True', '%3d', 'in'),
					  ('nEvents', 't_fusion', 'frame=False', '%3d', 'off')]


cutoff = .1

def main(dbN,geneN):

	(con,cursor) = mycgi.connectDB(db=dbN)

	if dbN == 'ccle1':

		mutation_map = {'DEL:3\'UTR':'UTR', 'SNP:3\'UTR':'UTR', 'SNP:Missense_Mutation':'MS', 'SNP:Intron':'INT', 'DEL:Frame_Shift_Del':'FS', \
						'SNP:5\'UTR':'UTR', 'DEL:In_Frame_Del':'FP', 'INS:3\'UTR':'UTR', 'SNP:Splice_Site_SNP':'SS', 'SNP:Nonsense_Mutation':'NS', \
						'INS:Frame_Shift_Ins':'FS', 'DEL:Intron':'INT', 'INS:Intron':'INT', 'DNP:Missense_Mutation':'MS', 'INS:Splice_Site_Ins':'SS', \
						'TNP:Intron':'INT', 'DNP:Nonsense_Mutation':'NS', 'DNP:Intron':'INT', 'SNP:De_novo_Start_OutOfFrame':'SOF', 'DNP:5\'UTR':'UTR', \
						'INS:5\'UTR':'UTR', 'SNP:Nonstop_Mutation':'NM', 'DNP:3\'UTR':'UTR', 'SNP:5\'Flank':'FLK', 'DEL:5\'UTR':'UTR', 'DNP:Splice_Site_DNP':'SS', \
						'INS:In_Frame_Ins':'FP', 'DEL:Splice_Site_Del':'SS', 'SNP:De_novo_Start_InFrame':'SIF', 'DEL:5\'Flank':'FLK', 'INS:5\'Flank':'FLK', \
						'DNP:De_novo_Start_InFrame':'SIF', 'DNP:Stop_Codon_DNP':'STC', 'INS:Stop_Codon_Ins':'STC', 'TNP:Nonsense_Mutation':'NS', \
						'TNP:Missense_Mutation':'MS', 'DEL:Start_Codon_Del':'SC'}

	else:

		mutation_map = {'':'UK','SNP:Intron':'INT', 'SNP:5\'UTR':'UTR', 'SNP:3\'UTR':'UTR', 'SNP:RNA':'RNA', 'SNP:5\'Flank':'FLK', \
						'DEL:Frame_Shift_Del':'FS', 'DEL:In_Frame_Del':'FP', 'DEL:Splice_Site':'SS', 'DEL:Translation_Start_Site':'TSS', \
						'DNP:Missense_Mutation':'MS', 'DNP:Nonsense_Mutation':'NS', 'DNP:Splice_Site':'SS', \
						'INS:Frame_Shift_Ins':'FS', 'INS:In_Frame_Ins':'FP', 'INS:Splice_Site':'SS', \
						'SNP:Missense_Mutation':'MS', 'SNP:Nonsense_Mutation':'NS', 'SNP:Nonstop_Mutation':'NM', 'SNP:Splice_Site':'SS', 'SNP:Translation_Start_Site':'TSS', \
						'Substitution - Missense':'MS', 'Substitution - Nonsense':'NS', 'Substitution - Missense,Substitution - coding silent':'MS', 'Nonstop extension':'rNS'}

	# prep RNA-Seq data availability table
	cursor.execute('create temporary table t_avail_RNASeq as select distinct samp_id from rpkm_gene_expr')

	# prep exonSkip info
	cursor.execute('select delExons,frame,loc1,loc2, count(*) cnt from splice_skip where gene_sym = "%s" and nPos>=5 group by delExons order by count(*) desc' % geneN)
	results = cursor.fetchall()

	conditionL_exonSkip = []

	for (delExons,frame,loc1,loc2, cnt) in results:

		if ':Y' in frame:
			frame_code = 'in'
		elif ':N' in frame:
			frame_code = 'off'
		else:
			frame_code = 'utr'

		conditionL_exonSkip.append( [
			('nReads', 'splice_skip', 'loc1="%s" and loc2="%s" and nPos>=5' % (loc1,loc2), '%3d', '%s<br><sup>(n=%s, %s)</sup>' % (delExons.split(',')[0], cnt,frame_code),), \
			#			('avg(nReads)', 'splice_normal', 'loc1="%s" or loc2="%s"' % (loc1,loc2), '%d') ])
			('sum(nReads)', 'splice_normal', 'loc1="%s"' % (loc1,), '%d') ])

	# prep mutation info
	cursor.execute('create temporary table t_mut as \
		select concat(substring(chrom,4,4),":",cast(chrSta as char),ref,">",alt) as ch_pos, ch_dna,ch_aa,ch_type,cosmic from mutation_rxsq \
		where gene_symL like "%s%s%s" and nReads_alt<>2 order by ch_type desc' % ('%',geneN,'%'))

	cursor.execute('select *,count(*) cnt from t_mut group by ch_pos order by count(*) desc, cosmic desc limit 20')
	results = cursor.fetchall()

	conditionL_mutation = []

	for (ch_pos,ch_dna,ch_aa,ch_type,cosmic,cnt) in results:

		ch_aa = ch_aa.replace(',','<br>')

		if cosmic:
			cosmic_fmt = '<font color="red">%s</font><br><sup>(n=%d, %s)</sup>'

		else:
			cosmic_fmt = '%s<br><sup>(n=%d, %s)</sup>'

		if ch_aa:
			cnd = ch_aa
		elif ch_dna:
			cnd = ch_dna
		else:
			cnd = ch_pos

		conditionL_mutation.append( [
			('nReads_alt,r_nReads_alt', 'mutation_rxsq', 'nReads_alt<>2 and concat(substring(chrom,4,4),":",cast(chrSta as char),ref,">",alt)="%s"' % ch_pos, '%d', cosmic_fmt % (cnd, cnt, mutation_map[ch_type])), \
			('nReads_ref,r_nReads_ref', 'mutation_rxsq', 'nReads_alt<>2 and concat(substring(chrom,4,4),":",cast(chrSta as char),ref,">",alt)="%s"' % ch_pos, '%d') ])

	# prep fusion table
	cursor.execute('create temporary table t_fusion as \
		select samp_id,locate(":Y",frame)>1 frame,count(nPos) nEvents \
		from splice_fusion where nPos>=2 and (find_in_set("%s",gene_sym1) or find_in_set("%s",gene_sym2)) group by samp_id, locate(":Y",frame)>1' % (geneN,geneN))

	# prep eiJunc info
	cursor.execute('select loc,juncAlias, count(*) cnt from splice_eiJunc where gene_sym="%s" and nReads>=10 group by loc' % geneN)
	results = cursor.fetchall()

	conditionL_eiJunc = []

	for (loc,juncAlias,cnt) in results:
		conditionL_eiJunc.append( [
			('nReads', 'splice_eiJunc', 'loc="%s" and nReads>=10' % loc, '%3d', '%s<br><sup>(n=%s)</sup>' % (juncAlias, cnt)),
			('sum(nReads)', 'splice_normal', 'loc1="%s"' % (loc,), '%d') ])

	# outlier
	outlier_sId = []
	
	cursor.execute('select samp_id, expr_MAD from array_gene_expr_MAD mad, gene_expr_stat stat where mad.gene_sym = stat.gene_sym and (mad.expr_MAD >= stat.q75 + 3*(stat.q75 - stat.q25) or mad.expr_MAD <= stat.q25 - 3*(stat.q75 - stat.q25)) and mad.gene_sym = "%s"' % geneN)
	results3 = cursor.fetchall()
	
	for i in range(len(results3)):
		outlier_sId.append(results3[i][0])

	
	conditionL = conditionL_preH[dbN] + conditionL_mutation + conditionL_fusion + conditionL_exonSkip + conditionL_eiJunc

	print '<p><h4>%s status of %s panel <small><a href="http://www.genecards.org/cgi-bin/carddisp.pl?gene=%s">[GeneCard]</a> <a href="http://www.ncbi.nlm.nih.gov/pubmed/?term=%s">[PubMed]</a></small></h4></p>' % (geneN,mycgi.db2dsetN[dbN],geneN,geneN)

	# census
	cursor.execute('select tumor_soma, tumor_germ, syndrome, mut_type from common.census where gene_sym="%s"' % geneN)
	census = cursor.fetchall()
	
	print('\n<font size=2> <table border="1" cellpadding="0" cellspacing="0">')
	print('<tr>\n<td rowspan=2>Census</td>\n<td>tumor_soma</td>\n<td>tumor_germ</td>\n<td>syndrome</td>\n<td>mut_type</td>\n</tr>\n')
	
	if len(census) != 0:
		print('<tr>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n</tr>\n' % (census[0][0],census[0][1],census[0][2],census[0][3]))
	else:
		print('<tr>\n<td></td>\n<td></td>\n<td></td>\n<td></td>\n</tr>\n')

	# drugbank
	cursor.execute('select drug from common.drugbank where gene_sym="%s"' % geneN)
	drug = [x for (x,) in cursor.fetchall()]
	
	print('\n<font size=2> <table border="1" cellpadding="0" cellspacing="0">')
	print('<br><tr>\n<td>Drug</td>\n')
	print('<td>%s</td>\n</tr>\n' % ('</br>\n'.join(drug)))
	
	# pathway
	cursor.execute('select biocarta_id, biocarta_desc from common.biocarta where gene_sym="%s"' % geneN)
	biocarta = cursor.fetchall()

	cursor.execute('select kegg_id, kegg_desc from common.kegg where gene_sym="%s"' % geneN)
	kegg = cursor.fetchall()

	cursor.execute('select go_id, go_desc from common.go where gene_sym="%s"' % geneN)
	go = cursor.fetchall()

	print('\n<font size=2> <table border="1" cellpadding="0" cellspacing="0">')
	print('<br><tr>\n<td>Biocarta</td>\n<td>KEGG</td>\n<td>GO</td>\n</tr>\n')
	print('<tr><td><div style="width:100%; height:50px; overflow:auto">')
	for (id,desc) in biocarta:
		print('<a href="http://cgap.nci.nih.gov/Pathways/BioCarta/%s">%s</br>' % (id,desc))
	print('</td>\n<td><div style="width:100%; height:50px; overflow:auto">')
	for (id,desc) in kegg:
		print('<a href="http://www.genome.jp/dbget-bin/www_bget?pathway+%s">%s</br>' % (id,desc))
	print('</td>\n<td><div style="width:100%; height:50px; overflow:auto">')
	for (id,desc) in go:
		print('<a href="http://amigo.geneontology.org/cgi-bin/amigo/term_details?term=GO:%s">%s</br>' % (id,desc))
	print('</div></td>\n</tr>\n')


	cursor.execute('create temporary table t_id as \
		select distinct samp_id from array_gene_expr union select distinct samp_id from array_cn union select distinct samp_id from splice_normal union select distinct samp_id from mutation_rxsq union select distinct samp_id from rpkm_gene_expr')

	cursor.execute('alter table t_id add index (samp_id)')

	cursor.execute('create temporary table t_expr as select * from array_gene_expr where gene_sym="%s"' % geneN)

	cursor.execute('alter table t_expr add index (samp_id,gene_sym)')

	cursor.execute('select samp_id from t_id left join t_expr using (samp_id) order by z_score desc')

	results = cursor.fetchall()

	numTotSamp = len(results)

	print('\n<font size=3> <table border="1" cellpadding="0" cellspacing="0">')

	# header: row1
	print '<br><tr>\n<td rowspan=2><div class="verticaltext" align="middle">samples<br><sup>n=%s</sup></div></td>' % numTotSamp,

	for i in range(len(conditionL)):

		row = conditionL[i]
		
		if type(row) == list:
			row = row[0]

		if i < len(conditionL_preH[dbN]):
			if ('tag' in row[1]) or ('t_avail' in row[1]):
				cursor.execute('select count(*) from %s where %s' % (row[1], row[2]))
			else:
				cursor.execute('select count(*) from %s where %s and gene_sym ="%s"' % (row[1], row[2], geneN))
			
			count = cursor.fetchone()
			if 'MAD' in row[4]:
				print('<td rowspan=2 align="middle"><div class="verticaltext">%s, n=%s)</sup></div></td>' % (row[-1],count[0]))
			else:
				print('<td rowspan=2 align="middle"><div class="verticaltext">%s<br><sup>(n=%s)</sup></div></td>' % (row[-1],count[0]))
		else:
			if i == len(conditionL_preH[dbN]) and len(conditionL_mutation)>0:
				print('<td align="middle" colspan=%s>mutation (mt/wt)</td>' % len(conditionL_mutation))
			elif i == len(conditionL_preH[dbN])+len(conditionL_mutation):
				print('<td align="middle" colspan=%s><a href="ircr_samp.py?dbN=%s&dType=Fusion">fusion</a></td>' % (len(conditionL_fusion),dbN))
			elif i == len(conditionL_preH[dbN])+len(conditionL_mutation)+len(conditionL_fusion) and len(conditionL_exonSkip)>0:
				print('<td align="middle" colspan=%s><a href="ircr_samp.py?dbN=%s&dType=ExonSkipping">exonSkip</a> (mt/wt)</td>' % (len(conditionL_exonSkip),dbN))
			elif i == len(conditionL_preH[dbN])+len(conditionL_mutation)+len(conditionL_fusion)+len(conditionL_exonSkip) and len(conditionL_eiJunc)>0:
				print('<td align="middle" colspan=%s><a href="ircr_samp.py?dbN=%s&dType=3pDeletion">3p deletion</a> (mt/wt)</td>' % (len(conditionL_eiJunc),dbN))

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

	for (sId,) in results:

		print '<tr>',
		print '<td nowrap><a href="ircr_samp.py?dbN=%s&sId=%s">%s</td>' % (dbN,sId,sId),

		d_flag = None
		r_flag = None

		for row in conditionL:
		
			outlier = None

			if type(row) == list:
				row_wt = row[1]
				row = row[0]
			else:
				row_wt = None

			(col,tbl,cnd,fmt) = row[:4]
				
			cursor.execute('show columns from %s like "gene_sym"' % tbl)

			if cursor.fetchone():
				cnd += ' and gene_sym="%s"' % geneN

			cursor.execute('select %s from %s where samp_id="%s" and (%s)' % (col,tbl,sId,cnd))

			results2 = cursor.fetchall()
					
			if len(results2) > 1:
				print sId
				raise Exception

			if type(row)==tuple and row[-1]=='RSq':

				if len(results2) > 0:
					r_flag = True
				else:
					r_flag = False

			if type(row)==tuple and row[-1]=='XSq':

				if len(results2) > 0:
					d_flag = True
				else:
					d_flag = False


			if type(row)==tuple and row[-1]=='expr<br><sup>(MAD':

				if sId in outlier_sId:
					outlier = True	
				else:
					outlier = False
			
			if len(results2) == 1:# and results2[0][0] not in (0,'0'):
									
				value = ('%s' % fmt) % results2[0][0]
			
				if len(results2[0]) >= 2:
					n_value = ('%s' % fmt) % results2[0][1]
				else:
					n_value = 0

				if row_wt:

					(col,tbl,cnd,fmt) = row_wt[:4]

					cursor.execute('select %s from %s where samp_id="%s" and %s' % (col,tbl,sId,cnd))

					results_wt = cursor.fetchone()
				
					n_count_wt = 0
				
					if results_wt[0]:
						count_wt = ('%s' % fmt) % results_wt[0]
					else:
						count_wt = 0

					if len(results_wt) >= 2:
						count_wt = ('%s' % fmt) % results_wt[0]
						n_count_wt = ('%s' % fmt) % results_wt[1]
					
					if row[1]=='mutation_rxsq':
							
						if int(n_value)!=0 and int(n_count_wt)!=0 and int(value)!=0 and int(count_wt)!=0:
							if int(value) > (int(value)+int(count_wt)) * cutoff and int(n_value) > (int(n_value)+int(n_count_wt)) * cutoff:
								print '<td><font color=red><b>%s</b></font><sub>/%s</sub>,<font color=468847><b>%s</b><sub>/%s</sub></font></td>' % (value,count_wt,n_value, n_count_wt),
							elif int(n_value) > (int(n_value)+int(n_count_wt)) * cutoff:
								print '<td>%s<sub>/%s</sub>,<font color=468847><b>%s</b><sub>/%s</sub></font></td>' % (value,count_wt,n_value, n_count_wt),
							elif int(value) > (int(value)+int(count_wt)) * cutoff:
								print '<td><font color=red><b>%s</b></font><sub>/%s</sub>,<font color=468847>%s<sub>/%s</sub></font></td>' % (value,count_wt,n_value, n_count_wt),
							else:
								print '<td>%s<sub>/%s</sub>,<font color=468847>%s<sub>/%s</sub></font></td>' % (value,count_wt,n_value, n_count_wt),
						
						elif int(value)==0 and int(count_wt) ==0:
							if int(n_value) > (int(n_value)+int(n_count_wt)) * cutoff:
								print '<td><font color=468847><b>%s</b><sub>/%s</sub></font></td>' % (n_value, n_count_wt),
							else:
								print '<td><font color=468847>%s<sub>/%s</sub></font></td>' % (n_value, n_count_wt),
						elif int(n_value) ==0 and int(n_count_wt)==0:
							if int(value) > (int(value)+int(count_wt)) * cutoff:
								print '<td><font color=red><b>%s</b></font><sub>/%s</sub></td>' % (value, count_wt),
							else:
								print '<td>%s<sub>/%s</sub></td>' % (value, count_wt),
							
					
					else:
						if int(value) > (int(value)+int(count_wt)) * cutoff:
							tmp = row[4].split('<br>')[0].split('/')
							if len(tmp)>1 and tmp[0]==tmp[1]:
								print '<td>%s<sub>/%s</sub></td>' % (value, count_wt),
							else:
								print '<td><font color=red><b>%s</b></font><sub>/%s</sub></td>' % (value, count_wt),
						else:
							print '<td>%s<sub>/%s</sub></td>' % (value, count_wt),

				else:
					if row[1] == 't_fusion':
						html_content = ""
						if row[4] == 'in':
							print '<a name="%s"></a>' %sId
							html_content = mycgi.compose_fusion_table(cursor,dbN, geneN, sId, "in")
							print '''
									<td><div class="tooltip_content">%s</div><div class="tooltip_link"><a href="#current">%s</a></div></td>
									''' % (html_content, value)
						else :
							html_content = mycgi.compose_fusion_table(cursor,dbN, geneN, sId, "off")
							print '''
									<td><div class="tooltip_content">%s</div><div class="tooltip_link"><a href="#current">%s</a></div></td>
									''' % (html_content, value)
					elif outlier:
						print '<td><font color=red><b>%s</b></font></td>' % value
				
					else :
						print '<td>%s</td>' % value

			else:
				#grey out
				if (r_flag==False and row[1] in ('splice_skip','t_fusion','splice_eiJunc')) or (r_flag==False and d_flag==False and row[1] in ('mutation_rxsq')):
					print '<td bgcolor=silver></td>'
				else:
					print '<td></td>'

		print '</tr>'

	print('\n</table> </font>\n')
	return


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

geneN = geneN.upper()

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>%s status of %s panel</title>
<link href="/js/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
<style type="text/css">
.verticaltext{
-webkit-transform:rotate(-90deg); writing-mode:tb-rl; -moz-transform:rotate(90deg); -o-transform: rotate(90deg); white-space:nowrap; display:blocking; padding-left:1px;padding-right:1px;padding-top:10px;padding-bottom:10px;
}

.tooltip_content {
	background-color: white;
	display: none;
	padding: 5px 10px;
	border: #CACACA 1px solid;
	position: fixed;
	z-index: 9999;
	color: #0C0C0C;
	margin: 0 0 0 10px;
	-webkit-border-radius: 8px;
	-moz-border-radius: 8px;
	border-radius: 8px;
}

td{
font-size:9pt;
}
</style>

<script type="text/javascript" src="http://code.jquery.com/jquery-1.3.2.js"></script>
<script type="text/javascript" src="/js/bootstrap/js/bootstrap.min.js"></script>
<script type="text/javascript">

$(document).ready(function() {

	function showTooltip(ele) {
		var tt = $(ele).prev();
		var lnk = $(ele);
		tt.css({
			left: lnk.offset().left - $(document).scrollLeft(),
			top: lnk.offset().top - tt.height() - $(document).scrollTop(),
			opacity: 1
		}).show();
	}

	$('.tooltip_link').click(function () {

		showTooltip(this);

		var tmp = this;
	
		$(this).one('mouseout', function(){
			$(document).one('click', function() { $(tmp).prev().fadeOut(); });
		});

	})
})

</script>

</head>
<body>
<div class="row-fluid">
<div class="span12" style="margin-left:10px; margin-top:10px;">
<form method='get' class="form-inline">
<select name='dbN' style="width:120px; height:23px; font-size:9pt">
<option value ='ircr1' name='dbN' %s>AVATAR GBM</option>
<option value ='tcga1' name='dbN' %s>TCGA GBM</option>
<option value ='ccle1' name='dbN' %s>CCLE</option>
</select>
<input type='text' name='geneN' value='%s' style="width:130px; height:15px; font-size:9pt">
<input type='submit' class="btn btn-small" value='Submit'>
</form>

''' % (geneN,mycgi.db2dsetN[dbN],('selected' if dbN=='ircr1' else ''),('selected' if dbN=='tcga1' else ''),('selected' if dbN=='ccle1' else ''),geneN)

main(dbN,geneN)

print('''
<br><h5>Legends</h5>
* "expr": z-normalized <br>
* "CN": in log2 scale <br>
* "mutation": (alt allele count) > 2 <br>
* "mutation": no silent <br>
* red in "mutation": in COSMIC database <br>
* "fusion": nPos > 1 <br>
* "exonSkip": nPos >= 5 <br>
* "3p deletion": nReads >= 10 <br>
* red numbers: (mut allele count) > (ref allele count) * 0.1 <br>
<br><br></div></div></font>
</body>
</html>''')

