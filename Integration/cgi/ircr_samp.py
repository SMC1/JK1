#!/usr/bin/python

import sys, cgi, re
import mycgi

def linkSamp(text):

	for g in re.findall('(S[0-9]{3})',text):
		text = text.replace(g,'<a href="ircr_samp.py?dbN=%s&sId=%s">%s</a>' % (dbN,g,g))

	return text

def main():

	## sample information

	if mode=='samp':

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

		print '</ul></p>'

	#census gene
	cursor.execute("select distinct gene_sym from common.census")
	census_gene = [x for (x,) in cursor.fetchall()]

	# drugbank
	cursor.execute("select distinct gene_sym from common.drugbank")
	drug_gene = [x for (x,) in cursor.fetchall()]

	# RTK
	rtk_gene= ['AATK','AATYK','AATYK2','AATYK3','ACH','ALK','anaplastic lymphoma kinase','ARK','ATP:protein-tyrosine O-phosphotransferase [ambiguous]','AXL','Bek','Bfgfr','BRT','Bsk','C-FMS','CAK','CCK4','CD115','CD135','CDw135','Cek1','Cek10','Cek11','Cek2','Cek3','Cek5','Cek6','Cek7','CFD1','CKIT','CSF1R','DAlk','DDR1','DDR2','Dek','DKFZp434C1418','Drosophila Eph kinase','DRT','DTK','Ebk','ECK','EDDR1','Eek','EGFR','Ehk2','Ehk3','Elk','EPH','EPHA1','EPHA2','EPHA6','EPHA7','EPHA8','EPHB1','EPHB2','EPHB3','EPHB4','EphB5','ephrin-B3 receptor tyrosine kinase','EPHT','EPHT2','EPHT3','EPHX','ERBB','ERBB1','ERBB2','ERBB3','ERBB4','ERK','Eyk','FGFR1','FGFR2','FGFR3','FGFR4','FLG','FLK1','FLK2','FLT1','FLT2','FLT3','FLT4','FMS','Fv2','HBGFR','HEK11','HEK2','HEK3','HEK5','HEK6','HEP','HER2','HER3','HER4','HGFR','HSCR1','HTK','IGF1R','INSR','INSRR','insulin receptor protein-tyrosine kinase','IR','IRR','JTK12','JTK13','JTK14','JWS','K-SAM','KDR','KGFR','KIA0641','KIAA1079','KIAA1459','Kil','Kin15','Kin16','KIT','KLG','LTK','MCF3','Mdk1','Mdk2','Mdk5','MEhk1','MEN2A/B','Mep','MER','MERTK','MET','Mlk1','Mlk2','Mrk','MST1R','MTC1','MUSK','Myk1','N-SAM','NEP','NET','Neu','neurite outgrowth regulating kinase','NGL','NOK','nork','novel oncogene with kinase-domain','Nsk2','NTRK1','NTRK2','NTRK3','NTRK4','NTRKR1','NTRKR2','NTRKR3','Nuk','NYK','PCL','PDGFR','PDGFRA','PDGFRB','PHB6','protein-tyrosine kinase [ambiguous]','protein tyrosine kinase [ambiguous]','PTK','PTK3','PTK7','receptor protein tyrosine kinase','RET','RON','ROR1','ROR2','ROS1','RSE','RTK','RYK','SEA','Sek2','Sek3','Sek4','Sfr','SKY','STK','STK1','TEK','TIE','TIE1','TIE2','TIF','TKT','TRK','TRKA','TRKB','TRKC','TRKE','TYK1','TYRO10','Tyro11','TYRO3','Tyro5','Tyro6','TYRO7','UFO','VEGFR1','VEGFR2','VEGFR3','Vik','YK1','Yrk']
	
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

		if mode=='samp':
			cursor.execute("select %s from %s where samp_id = '%s' and %s order by %s" % (','.join(colL), tblN, sId, cond, ordr))
		else:
			cursor.execute("select %s from %s where %s order by %s" % (','.join(colL), tblN, dTypeH[dt][1], ordr))

		data = cursor.fetchall()

		# theader
		if mode=='samp':
			if dt in ['Fusion','ExonSkipping','3pDeletion']:
				print '<br><b><a href="ircr_samp.py?dbN=%s&dType=%s">%s</a></b> (%s, %s, %s):' % (dbN,dt,dt,len(data),('All' if cond=='True' else cond),ordr)
			else:
				print '<br><b>%s</b> (%s, %s, %s):' % (dt,len(data),('All' if cond=='True' else cond),ordr)
		else:
			print '<font size=3><p id="%s_"><b>%s</b> (%s, %s, %s):</font></p>' % (dt,dt,len(data),dTypeH[dt][1],ordr)

		print '''

			<a href="#current" onclick="$('#%s tbody tr').hide()">None</a> | <a href="#current" onclick='filter("%s","census")'>Census</a> | <a href="#current" onclick='filter("%s","drugbank")'>Drugbank</a> | <a href="#current" onclick='filter("%s","rtk")'>RTK</a> | <a href="#current" onclick="$('#%s tbody tr').show()">All</a><br>
			<table border="1" cellpadding="0" cellspacing="0" id="%s">
			<thead>''' % ((dt,)*6)

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
					
				elif colN == 'ch_type':
					print '<td nowrap> %s </td>' % content
				elif colN == 'samp_id':
					print '<td nowrap> <a href="ircr_samp.py?dbN=%s&sId=%s"> %s </a> </td>' % (dbN,content,content)
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
	('Mutation', ["concat(strand,chrom,':',chrSta,'-',chrEnd) coord_hg19", "ref", "alt", "nReads_ref", "nReads_alt", \
		"gene_sym", "ch_dna", "ch_aa", "ch_type", "cosmic", "mutsig", "if(census is NULL,'',census) census"], 't_mut', 'True', 'gene_sym,chrSta'),
	('Fusion', ["loc1 coord1", "loc2 coord2", "gene_sym1", "gene_sym2", "ftype", "exon1", "exon2", "frame", "nPos","nReads","nReads_w1","nReads_w2"], 'splice_fusion_AF', 'nPos>2', 'nPos desc'),
	('ExonSkipping', ["loc1 coord1", "loc2 coord2", "gene_sym", "frame", "delExons", "exon1", "exon2", "nPos", "nReads","nReads_w1","nReads_w2"], 'splice_skip_AF', 'nPos>2', 'nPos desc'),
	('3pDeletion', ["loc coord_hg19", "gene_sym", "juncInfo", "juncAlias", "nReads","nReads_w"], 'splice_eiJunc_AF', 'nReads_w and nReads>5', '(nReads/nReads_w) desc'),
	('ExprOutlier',["gene_sym","expr_MAD","q25","median","q75"],'t_outlier', '(expr_MAD >= q75 + 3*(q75-q25) or expr_MAD <= q25 - 3*(q75-q25))', 'gene_sym')
	]

(con,cursor) = mycgi.connectDB(db=dbN)

if mode == 'samp':

	cursor.execute('create temporary table t_mut as \
		select mutation.*,concat(tumor_soma,";",tumor_germ,";",mut_type,";",tloc_partner) census \
		from mutation left join census using (gene_sym) where samp_id="%s"' % sId)

	cursor.execute('create temporary table t_outlier as \
		select samp_id,mad.gene_sym, expr_MAD, q25, median, q75 from array_gene_expr_MAD mad \
		join gene_expr_stat stat using (gene_sym) where samp_id="%s"' % sId)

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">'''

if mode =='samp':
	print '<title>%s (%s)</title>' % (sId,mycgi.db2dsetN[dbN])
else:
	print '<title>%s (%s)</title>' % (dType,mycgi.db2dsetN[dbN])

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