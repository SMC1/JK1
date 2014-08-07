#!/usr/bin/python

import sys, cgi, re, os
import mycgi
from glob import glob

def linkSamp(text):

	for g in re.findall('(S[0-9]{3}|S[0-9]{1,2}[ABC])',text):
		text = text.replace(g,'<a href="ircr_samp.py?dbN=%s&sId=%s">%s</a>' % (dbN,g,g))

	return text

def main():

	## sample information

	if mode=='samp':

		print '<p><h4><a name="top"></a>%s <small> (%s)</small></h4></p> <p><ul>' % (sId,mycgi.db2dsetN(dbN))

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

		# normal
		print '<li>Normal: %s' % ', '.join(map(lambda x: x[7:], filter(lambda x: x.startswith('normal_'), tags)))

		if dbN == 'ircr1':
			cursor.execute('select tumor_frac from xsq_purity where samp_id="%s"' % (sId))
			tfrac = cursor.fetchone()
			print '<li>Tumor fraction (estimated from WXS): %s%%' % tfrac
		
		print '</ul>'

		tags = []
		for spec in specL:
			(dt,colL,tblN,cond,ordr) = spec
			tags.append(' <a href="#%s">%s</a> ' % (dt, dt))
		print '|'.join(tags)

		print '</p>'


	#census gene
	cursor.execute("select distinct gene_sym from common.census")
	census_gene = [x for (x,) in cursor.fetchall()]

	# drugbank
	cursor.execute("select distinct gene_sym from common.drugbank")
	drug_gene = [x for (x,) in cursor.fetchall()]

	# genes targeted by in-house HTS screening
	cursor.execute("select distinct gene_sym from common.scrn_drug")
	scrn_gene = [x for (x,) in cursor.fetchall()]

	# RTK
	rtk_gene= ['AATK','AATYK','AATYK2','AATYK3','ACH','ALK','anaplastic lymphoma kinase','ARK','ATP:protein-tyrosine O-phosphotransferase [ambiguous]','AXL','Bek','Bfgfr','BRT','Bsk','C-FMS','CAK','CCK4','CD115','CD135','CDw135','Cek1','Cek10','Cek11','Cek2','Cek3','Cek5','Cek6','Cek7','CFD1','CKIT','CSF1R','DAlk','DDR1','DDR2','Dek','DKFZp434C1418','Drosophila Eph kinase','DRT','DTK','Ebk','ECK','EDDR1','Eek','EGFR','Ehk2','Ehk3','Elk','EPH','EPHA1','EPHA2','EPHA6','EPHA7','EPHA8','EPHB1','EPHB2','EPHB3','EPHB4','EphB5','ephrin-B3 receptor tyrosine kinase','EPHT','EPHT2','EPHT3','EPHX','ERBB','ERBB1','ERBB2','ERBB3','ERBB4','ERK','Eyk','FGFR1','FGFR2','FGFR3','FGFR4','FLG','FLK1','FLK2','FLT1','FLT2','FLT3','FLT4','FMS','Fv2','HBGFR','HEK11','HEK2','HEK3','HEK5','HEK6','HEP','HER2','HER3','HER4','HGFR','HSCR1','HTK','IGF1R','INSR','INSRR','insulin receptor protein-tyrosine kinase','IR','IRR','JTK12','JTK13','JTK14','JWS','K-SAM','KDR','KGFR','KIA0641','KIAA1079','KIAA1459','Kil','Kin15','Kin16','KIT','KLG','LTK','MCF3','Mdk1','Mdk2','Mdk5','MEhk1','MEN2A/B','Mep','MER','MERTK','MET','Mlk1','Mlk2','Mrk','MST1R','MTC1','MUSK','Myk1','N-SAM','NEP','NET','Neu','neurite outgrowth regulating kinase','NGL','NOK','nork','novel oncogene with kinase-domain','Nsk2','NTRK1','NTRK2','NTRK3','NTRK4','NTRKR1','NTRKR2','NTRKR3','Nuk','NYK','PCL','PDGFR','PDGFRA','PDGFRB','PHB6','protein-tyrosine kinase [ambiguous]','protein tyrosine kinase [ambiguous]','PTK','PTK3','PTK7','receptor protein tyrosine kinase','RET','RON','ROR1','ROR2','ROS1','RSE','RTK','RYK','SEA','Sek2','Sek3','Sek4','Sfr','SKY','STK','STK1','TEK','TIE','TIE1','TIE2','TIF','TKT','TRK','TRKA','TRKB','TRKC','TRKE','TYK1','TYRO10','Tyro11','TYRO3','Tyro5','Tyro6','TYRO7','UFO','VEGFR1','VEGFR2','VEGFR3','Vik','YK1','Yrk']

	# CancerScan
	cs_gene = ['ABL1','AKT1','AKT2','AKT3','ALK','APC','ARID1A','ARID1B','ARID2','ATM','ATRX','AURKA','AURKB','BCL2','BRAF','BRCA1','BRCA2','CDH1','CDK4','CDK6','CDKN2A','CSF1R','CTNNB1','DDR2','EGFR','EPHB4','ERBB2','ERBB3','ERBB4','EWSR1','EZH2','FBXW7','FGFR1','FGFR2','FGFR3','FLT3','GNA11','GNAQ','GNAS','HNF1A','HRAS','IDH1','IDH2','IGF1R','ITK','JAK1','JAK2','JAK3','KDR','KIT','KRAS','MDM2','MET','MLH1','MPL','MTOR','NF1','NOTCH1','NPM1','NRAS','NTRK1','PDGFRA','PDGFRB','PIK3CA','PIK3R1','PTCH1','PTCH2','PTEN','PTPN11','RB1','RET','ROS1','SMAD4','SMARCB1','SMO','SRC','STK11','SYK','TMPRSS2','TOP1','TP53','VHL']
	
	## variant information

	if mode=='type':
		tableL = [specL[dTypeH[dType][0]]]
	else:
		tableL = specL

	print '<font size=2>'

	for spec in tableL:

		(dt,colL,tblN,cond,ordr) = spec

		if mode=='type':
			colL = ["samp_id"] + colL

		if dbN not in ['tcga1','ircr1','ccle1'] and tblN in ['t_outlier','t_expr']:
			continue
		elif dbN not in ['tcga1','ircr1','ccle1','CancerSCAN'] and tblN in ['xsq_cn']:
			continue
		elif dbN not in ['CancerSCAN'] and tblN in ['t_mut_cs','cs_cn']:
			continue

		if mode=='samp':
			cursor.execute("select %s from %s where samp_id = '%s' and %s order by %s" % (','.join(colL), tblN, sId, cond, ordr))
		else:
			cursor.execute("select %s from %s where %s order by %s" % (','.join(colL), tblN, dTypeH[dt][1], ordr))

		data = cursor.fetchall()

		print '<a name="%s"></a>' % (dt)
		
		# theader
		if mode=='samp':
			if dt in ['Fusion','ExonSkipping','3pDeletion']:
				print '<br><h5><a href="ircr_samp.py?dbN=%s&dType=%s">%s</a> (%s, %s, %s):' % (dbN,dt,dt,len(data),('All' if cond=='True' else cond),ordr)
			else:
				print '<br><h5>%s (%s, %s, %s):' % (dt,len(data),('All' if cond=='True' else cond),ordr)
		else:
			print '<h5><p id="%s_"><b>%s</b> (%s, %s, %s):</p>' % (dt,dt,len(data),dTypeH[dt][1],ordr)
		if dt in ['Mutation','Mutation_CS']:
			flt_germ=''' | <a href="#current" onclick='filter("%s","somatic")'>Filter</a>''' % dt
		else:
			flt_germ=''

		print '''
			<small>
			<a name="%s"></a><a href="#top">Page Top</a> |
			<a href="#current" onclick="$('#%s tbody tr').show()">All</a> | <a href="#current" onclick='filter("%s","census")'>Census</a> | <a href="#current" onclick='filter("%s","rtk")'>RTK</a> | <a href="#current" onclick='filter("%s","drugbank")'>Drugbank</a> | <a href="#current" onclick="$('#%s tbody tr').hide()">None</a> | <a href="#current" onclick='filter("%s","scrn")'>Screening</a> | <a href="#current" onclick='filter("%s","regulatory")'>Regulatory</a> | <a href="#current" onclick='filter("%s","cancerscan")'>CancerScan</a>%s</small></h5>''' % tuple([dt,]*9+[flt_germ])

		if dt == 'xCN':
			cursor.execute("select samp_id from sample_tag where samp_id = '%s' and tag like 'XSeq_%%'" % sId)
			results = cursor.fetchall()
			if len(results) > 0:
				fL = glob('/EQL1/NSL/WXS/results/CNA/%s*_SS.*traj.png' % sId) + glob('/EQL1/NSL/WXS/results/CNA/%s*_TS.*traj.png' % sId)
				if len(fL) > 0:
					print '<div><img src="http://119.5.134.58/WXS_CNA/%s"></img></div>' % fL[0].split('/')[-1]
				if len(glob('/EQL1/NSL/WXS/results/CNA/%s*2pl.png' % sId)) > 0:
					basename = glob('/EQL1/NSL/WXS/results/CNA/%s*2pl.png' % sId)[0].split('/')[-1]
					print '<a href="http://119.5.134.58/WXS_CNA/%s" target="_blank">Comparison with array CGH</a>' % basename
		if dt == 'csCN':
			if len(glob('/EQL1/NSL/WXS/results/CNA/%s*_CS*traj.png' % sId)) > 0:
				sname = glob('/EQL1/NSL/WXS/results/CNA/%s*CS*traj.png' % sId)[0]
				print '<div><img src="http://119.5.134.58/WXS_CNA/%s"></img></div>' % sname.split('/')[-1]
		if dt == 'ExprCS':
			if len(glob('/EQL1/NSL/RNASeq/results/expression/%s_CS_expr.png' % sId)) > 0:
				print '<div><img src="http://119.5.134.58/RSQ_RPKM/%s_CS_expr.png"></img></div>' % sId


		print '''
			<table border="1.5" cellpadding="0" cellspacing="0" id="%s">
			<thead>''' % dt

		print '<tr>'
		for colN in colL:
			print '<td><b> %s </b></td>' % colN.split(' ')[-1]
		print '</tr></thead><tbody>'

		# tbody
		for row in data:
			print '<tr>'

			for j in range(len(row)) :
				
				colN = colL[j].split(' ')[-1]

				content = str(row[j]).replace(',',', ').replace('|',', ')

				cls = []
				
				if colN in ('gene_sym','gene_symL','gene_sym1','gene_sym2'):
					geneL = row[j].split(',')

					if any (g in geneL for g in census_gene):
						cls.append("census")
					else:
						cls.append("not_census")

					if any (g in geneL for g in drug_gene):
						cls.append("drugbank")
					else:
						cls.append("not_drugbank")

					if any (g in geneL for g in scrn_gene):
						cls.append("scrn")
					else:
						cls.append("not_scrn")

					if any (g in geneL for g in rtk_gene):
						cls.append("rtk")
					else:
						cls.append("not_rtk")

					if any (g in geneL for g in cs_gene):
						cls.append("cancerscan")
					else:
						cls.append("not_cancerscan")

					linkL = []

					for g in geneL:
						cursor.execute('select 1 from common.hugo where gene_sym="%s"' % g)
						if cursor.fetchone():
							linkL.append('<a href="ircr.py?dbN=%s&geneN=%s" class="%s"> %s </a>' % (dbN,g,' '.join(cls),g))
						else:
							linkL.append('<a class="%s">%s</a>' % (' '.join(cls),g))

					print '<td>%s</td>' % ', '.join(linkL)
					
				elif colN == 'ch_type':
					if 'regulatory' in row[j] or 'TFBS_' in row[j] or 'TF_binding_site_' in row[j]:
						cls.append("regulatory")
					else:
						cls.append("not_regulatory")
					content = '<a class="%s">%s</a>' % (' '.join(cls), content)
					print '<td nowrap> %s </td>' % content
				elif colN == 'nIRCRb':
					if int(row[j])<1:
						cls.append('somatic')
					else:
						cls.append('not_somatic')
					content = '<a class="%s">%s</a>' % (' '.join(cls), content)
					print '<td> %s </td>' % content
				elif colN == 'cosmic':
					tcga = ''
					cosmic=''
					if 'tcga:' in content:
						tcga = re.search('.*, tcga:(.*)', content).group(1)
						tcga = '''<div class="tooltip_content">%s</div><div class="tooltip_link"><a href="#current">tcga</a></div>''' % (tcga)
					if 'cosmic:' in content:
						cosmic = re.search('cosmic:(.*), .*', content).group(1)
						cosmic = '''<div class="tooltip_content">%s</div><div class="tooltip_link"><a href="#current">cosmic</a></div>''' % (cosmic)
					print '<td style=white-space:nowrap;">%s%s</td>' % (tcga, cosmic)
				elif colN == 'samp_id':
					print '<td nowrap> <a href="ircr_samp.py?dbN=%s&sId=%s"> %s </a> </td>' % (dbN,content,content)
				elif 'coord' in colN:
					if content[0] == 'c':
						print '<td nowrap><a href="http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=%s"> %s </a></td>' % (content,content)
					else:
						print '<td nowrap><a href="http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=%s"> %s </a></td>' % (content[1:],content)
				else:
					print '<td> %s </td>' % content

			print '</tr>'

		print '</tbody></table>'

	print '</font><br><br>'

	return

link = cgi.FieldStorage()

if link.has_key("dbN") :
	dbN = link.getvalue("dbN")
else :
	dbN = "tcga1"

if link.has_key("sId") :
	mode = 'samp'
	sId = link.getvalue("sId")
elif link.has_key("dType"):
	mode = 'type'
	dType = link.getvalue("dType")
else :
	mode = 'samp'
	sId = "TCGA-06-5411"

dTypeH = {
	'Fusion': (1,'nPos>10'),
	'ExonSkipping': (2,'nPos>20'),
	'3pDeletion': (3,'nReads_w and nReads/nReads_w>=50')
	}

specL = [
#	('Mutation', ["concat(strand,chrom,':',chrSta,'-',chrEnd) coord_hg19", "ref", "alt", "n_nReads_ref", "n_nReads_alt", "nReads_ref", "nReads_alt", \
	('Mutation', ["concat(chrom,':',chrSta,'-',chrEnd) coord_hg19", "ref", "alt", "n_nReads_ref", "n_nReads_alt", "nReads_ref", "nReads_alt", \
		"r_nReads_ref", "r_nReads_alt","if(count is NULL,'0',count) nIRCRb", "gene_symL", "ch_dna", "ch_aa", "ch_type", "cosmic", "mutsig", "if(census is NULL,'',census) census"], 't_mut', 'True', 'gene_symL,chrSta'),
	('Mutation_CS', ["concat(chrom,':',chrSta,'-',chrEnd) coord_hg19", "ref", "alt", "n_nReads_ref", "n_nReads_alt", "nReads_ref", "nReads_alt", \
		"r_nReads_ref", "r_nReads_alt","ifnull(count,'0') nIRCRb", "gene_sym", "ch_dna", "ch_aa", "ch_type", "cosmic", "mutsig", "ifnull(census,'')"], 't_mut_cs', 'True', 'gene_sym,chrSta'),
	('Fusion', ["loc1 coord1", "loc2 coord2", "gene_sym1", "gene_sym2", "frame", "ftype", "exon1", "exon2", "nPos","nReads","nReads_w1","nReads_w2"], 'splice_fusion_AF', 'nPos>2', 'nPos desc'),
	('ExonSkipping', ["loc1 coord1", "loc2 coord2", "gene_sym", "frame", "delExons", "exon1", "exon2", "nPos", "nReads","nReads_w1","nReads_w2"], 'splice_skip_AF', 'nPos>2 and nReads>10', 'nPos desc'),
	('3pDeletion', ["loc coord_hg19", "gene_sym", "juncInfo", "juncAlias", "nReads","nReads_w"], 'splice_eiJunc_AF', 'nReads_w and nReads>10 and (nReads/nReads_w)>0.5', '(nReads/nReads_w) desc'),
	('ExprOutlier',["gene_sym","expr_MAD","q25","median","q75"],'t_outlier', '(expr_MAD >= q75 + 3*(q75-q25) or expr_MAD <= q25 - 3*(q75-q25))', 'gene_sym'),
	('ExprCensus',["gene_sym","z_score","rpkm"],'t_expr', 'True', 'z_score desc'),
	('ExprCS',["gene_sym","rpkm"], 'rpkm_gene_expr', 'rpkm >= 10 and gene_sym in (select * from common.cs_gene)', 'gene_sym'),
	('xCN', ["gene_sym","value_log2"],'xsq_cn','abs(value_log2)>=0.7','abs(value_log2) desc'),
	('csCN', ["gene_sym","value_log2"], 'cs_cn', 'abs(value_log2)>=0.9', 'abs(value_log2) desc')
	]
if dbN != 'CancerSCAN':
	specL = [specL[0]] + specL[2:9]

(con,cursor) = mycgi.connectDB(db=dbN)

if mode == 'samp':

#	cursor.execute('create temporary table t_mut as \
#		select mutation_rxsq.*,concat(tumor_soma,";",tumor_germ,";",mut_type,";",tloc_partner) census \
#		from mutation_rxsq left join common.census on find_in_set(gene_sym,gene_symL) where samp_id="%s"' % sId)

	if dbN == 'CancerSCAN':
		cursor.execute('''CREATE TEMPORARY TABLE t_mut1 AS \
			SELECT samp_id,mutation_cs.chrom,mutation_cs.chrSta,mutation_cs.chrEnd,mutation_cs.ref,mutation_cs.alt,mutation_cs.n_nReads_ref,mutation_cs.n_nReads_alt,mutation_cs.nReads_ref,mutation_cs.nReads_alt,0 r_nReads_ref,0 r_nReads_alt,mutation_cs.gene_sym gene_sym,mutation_cs.ch_dna,mutation_cs.ch_aa,mutation_cs.ch_type,concat(mutation_cs.cosmic,",",mutation_cs.tcga) cosmic,'' mutsig,concat(tumor_soma,";",tumor_germ,";",mut_type,";",tloc_partner) census \
			FROM mutation_cs LEFT JOIN common.census ON mutation_cs.gene_sym=common.census.gene_sym WHERE samp_id="%s"''' % sId)
		cursor.execute('''CREATE TEMPORARY TABLE t_mut_cs AS \
			SELECT t_mut1.*,common.mutation_ctr.count count \
			FROM t_mut1 LEFT JOIN common.mutation_ctr ON t_mut1.chrom=common.mutation_ctr.chrom AND t_mut1.chrSta=common.mutation_ctr.chrSta \
			AND t_mut1.chrEnd=common.mutation_ctr.chrEnd AND t_mut1.ref=common.mutation_ctr.ref AND t_mut1.alt=common.mutation_ctr.alt''')
		cursor.execute('''DROP TEMPORARY TABLE t_mut1''')

	cursor.execute('CREATE TEMPORARY TABLE t_mut1 AS \
		SELECT mutation_rxsq.*,concat(tumor_soma,";",tumor_germ,";",mut_type,";",tloc_partner) census \
		FROM mutation_rxsq LEFT JOIN common.census ON find_in_set(gene_symL,gene_sym) WHERE samp_id="%s"' % sId)

	cursor.execute('CREATE TEMPORARY TABLE t_mut AS \
		SELECT t_mut1.*,common.mutation_ctr.count count \
		FROM t_mut1 LEFT JOIN common.mutation_ctr ON t_mut1.chrom=common.mutation_ctr.chrom AND t_mut1.chrSta=common.mutation_ctr.chrSta \
		AND t_mut1.chrEnd=common.mutation_ctr.chrEnd AND t_mut1.ref=common.mutation_ctr.ref AND t_mut1.alt=common.mutation_ctr.alt')
	cursor.execute('DROP TEMPORARY TABLE t_mut1')


	if dbN in ['ircr1','tcga1','ccle1']:
		cursor.execute('create temporary table t_outlier as \
			select samp_id,mad.gene_sym, expr_MAD, q25, median, q75 from array_gene_expr_MAD mad \
			join gene_expr_stat stat using (gene_sym) where samp_id="%s"' % sId)

	cursor.execute('create temporary table t_expr as \
		select t_a.samp_id, t_a.gene_sym, format(z_score,2) z_score, format(rpkm,1) rpkm from array_gene_expr t_a \
		join rpkm_gene_expr t_r using (samp_id,gene_sym) \
		join common.census using (gene_sym) where samp_id="%s"' % sId)

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML>
<html>
<head>
<link href="/js/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
<style type="text/css">
.td{font-size:9pt;}

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
</style>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">'''

if mode =='samp':
	print '<title>%s (%s)</title>' % (sId,mycgi.db2dsetN(dbN))
else:
	print '<title>%s (%s)</title>' % (dType,mycgi.db2dsetN(dbN))

print '''
<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.js"></script>
<script type="text/javascript" src="/js/bootstrap/js/bootstrap.min.js"></script>
<script type="text/javascript">
function filter(dType,geneInfoDB){
	$("#"+dType+" tbody tr:has(.not_"+geneInfoDB+")").hide()   
	$("#"+dType+" tbody tr:has(."+geneInfoDB+")").show()
}

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
'''

main()

print('''
</div></div>
</body>
</html>''')
