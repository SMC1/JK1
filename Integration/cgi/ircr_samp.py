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
	cursor.execute("select distinct gene_sym from common.census")
	census_gene = [x for (x,) in cursor.fetchall()]

	# drugbank
	cursor.execute("select distinct gene_sym from common.drugbank")
	drug_gene = [x for (x,) in cursor.fetchall()]

	# RTK
	rtk_gene= ['AATK','AATYK','AATYK2','AATYK3','ACH','ALK','anaplastic lymphoma kinase','ARK','ATP:protein-tyrosine O-phosphotransferase [ambiguous]','AXL','Bek','Bfgfr','BRT','Bsk','C-FMS','CAK','CCK4','CD115','CD135','CDw135','Cek1','Cek10','Cek11','Cek2','Cek3','Cek5','Cek6','Cek7','CFD1','CKIT','CSF1R','DAlk','DDR1','DDR2','Dek','DKFZp434C1418','Drosophila Eph kinase','DRT','DTK','Ebk','ECK','EDDR1','Eek','EGFR','Ehk2','Ehk3','Elk','EPH','EPHA1','EPHA2','EPHA6','EPHA7','EPHA8','EPHB1','EPHB2','EPHB3','EPHB4','EphB5','ephrin-B3 receptor tyrosine kinase','EPHT','EPHT2','EPHT3','EPHX','ERBB','ERBB1','ERBB2','ERBB3','ERBB4','ERK','Eyk','FGFR1','FGFR2','FGFR3','FGFR4','FLG','FLK1','FLK2','FLT1','FLT2','FLT3','FLT4','FMS','Fv2','HBGFR','HEK11','HEK2','HEK3','HEK5','HEK6','HEP','HER2','HER3','HER4','HGFR','HSCR1','HTK','IGF1R','INSR','INSRR','insulin receptor protein-tyrosine kinase','IR','IRR','JTK12','JTK13','JTK14','JWS','K-SAM','KDR','KGFR','KIA0641','KIAA1079','KIAA1459','Kil','Kin15','Kin16','KIT','KLG','LTK','MCF3','Mdk1','Mdk2','Mdk5','MEhk1','MEN2A/B','Mep','MER','MERTK','MET','Mlk1','Mlk2','Mrk','MST1R','MTC1','MUSK','Myk1','N-SAM','NEP','NET','Neu','neurite outgrowth regulating kinase','NGL','NOK','nork','novel oncogene with kinase-domain','Nsk2','NTRK1','NTRK2','NTRK3','NTRK4','NTRKR1','NTRKR2','NTRKR3','Nuk','NYK','PCL','PDGFR','PDGFRA','PDGFRB','PHB6','protein-tyrosine kinase [ambiguous]','protein tyrosine kinase [ambiguous]','PTK','PTK3','PTK7','receptor protein tyrosine kinase','RET','RON','ROR1','ROR2','ROS1','RSE','RTK','RYK','SEA','Sek2','Sek3','Sek4','Sfr','SKY','STK','STK1','TEK','TIE','TIE1','TIE2','TIF','TKT','TRK','TRKA','TRKB','TRKC','TRKE','TYK1','TYRO10','Tyro11','TYRO3','Tyro5','Tyro6','TYRO7','UFO','VEGFR1','VEGFR2','VEGFR3','Vik','YK1','Yrk']
	
	## variant information

	for spec in specL:

		(dType,colL,tblN,cond,ordr) = spec

		cursor.execute("select %s from %s where samp_id = '%s' and %s order by %s" % (','.join(colL), tblN, sId, cond, ordr))
		data = cursor.fetchall()

		# theader
		print '<br><a name="%s_"></a><b>%s</b> (%s, %s):' % (dType,dType,len(data),('All' if cond=='True' else cond))

		print '''
			<a href="#%s_" onclick="$('#%s tbody tr').hide()">None</a> | <a href="#%s_" onclick='filter("%s","census")'>Census</a> | <a href="#%s_" onclick='filter("%s","drugbank")'>Drugbank</a>| <a href="#%s_" onclick='filter("%s","rtk")'>RTK</a> | <a href="#%s_" onclick="$('#%s tbody tr').show()">All</a><br>
			<table border="1" cellpadding="0" cellspacing="0" id="%s">
			<thead>''' % (dType,dType,dType,dType,dType,dType,dType,dType,dType,dType,dType)

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

				cls = []
				
				if colN in ('gene_sym','gene_sym1','gene_sym2'):
					geneL = row[j].split(',')

					if any (g in geneL for g in census_gene):
						cls.append("census")
					else:
						cls.append("not_census")

					if any (g in geneL for g in drug_gene):
						cls.append("drugbank")
					else:
						cls.append("not_drugbank")

					if any (g in geneL for g in rtk_gene):
						cls.append("rtk")
					else:
						cls.append("not_rtk")

					print '<td><a href="ircr.py?dbN=%s&geneN=%s" class="%s"> %s </a></td>' % (dbN,row[j],' '.join(cls),content)
					
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
	('3pDeletion', ["loc coord_hg19", "gene_sym", "juncInfo", "juncAlias", "nReads","nReads_w"], 't_3p_af', 'nReads_w and nReads>5', 'nReads/nReads_w desc'),
	('ExprOutlier',["gene_sym","expr_MAD","q25","median","q75"],'t_outlier', '(expr_MAD >= q75 + 3*(q75-q25) or expr_MAD <= q25 - 3*(q75-q25))', 'gene_sym')
	]

(con,cursor) = mycgi.connectDB(db=dbN)

cursor.execute('create temporary table t_mut as \
	select mutation.*,concat(tumor_soma,";",tumor_germ,";",mut_type,";",tloc_partner) census \
	from mutation left join census using (gene_sym) where samp_id="%s"' % sId)

cursor.execute('create temporary table t_3p as select * from splice_eiJunc where samp_id="%s"' % sId)
cursor.execute('alter table t_3p add index (loc)')

cursor.execute('create temporary table t_splice_normal as select loc1,sum(nReads) nReads_w from splice_normal where samp_id="%s" group by loc1' % sId)
cursor.execute('alter table t_splice_normal add index (loc1)')

cursor.execute('create temporary table t_3p_af as \
	select samp_id,loc,gene_sym,juncInfo,juncAlias,t1.nReads,t2.nReads_w \
	from t_3p t1 left join t_splice_normal t2 on t1.loc=t2.loc1 where t1.samp_id="%s"' % sId)

cursor.execute('create temporary table t_outlier as \
	select samp_id,mad.gene_sym, expr_MAD, q25, median, q75 from array_gene_expr_MAD mad \
	join gene_expr_stat stat using (gene_sym) where samp_id="%s"' % sId)

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>%s (%s)</title>''' % (sId,mycgi.db2dsetN[dbN])

print '''
<script type="text/javascript" src="http://code.jquery.com/jquery-1.5.2.js"></script>
<script type="text/javascript">

function filter(dType,geneInfoDB){
	$("#"+dType+" tbody tr:has(a.not_"+geneInfoDB+")").hide()   
	$("#"+dType+" tbody tr:has(a."+geneInfoDB+")").show()
}

</script>
</head>

<body>
'''

main()

print('''
</body>
</html>''')
