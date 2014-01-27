#!/usr/bin/python

import sys, cgi, json, time
import mycgi

sampInfoH = { \
	'Rsq': ('Rsq','samp_id','splice_normal','True'),
	'Xsq': ('Xsq','tag','sample_tag','tag like "XSeq_%"')
}

afColNameH = {
	'mutation_normal': ('nReads_alt','nReads_ref'),
	'mutation_rsq': ('r_nReads_alt', 'r_nReads_ref'),
	'splice_fusion_AF': ('nReads','nReads_w1'),
	'splice_skip_AF': ('nReads','nReads_w1'),
	'splice_eiJunc_AF': ('nReads','nReads_w'),
}

mutTypeH = {
	'MUT': ('mutation_normal','ch_aa', lambda x:x),
	'MUTX': ('mutation_normal','ch_aa', lambda x:x),
	'MUTR': ('mutation_rsq', 'ch_aa', lambda x:x),
	'SKIP': ('splice_skip_AF','delExons', lambda x:x),
	'3pDEL': ('splice_eiJunc_AF','juncAlias', lambda x: '%s-' % (int(x.split('/')[0])+1,))
}

otherTypeH = {
	'RPKM': ('rpkm_gene_expr', 'rpkm'),
	'CNA': ('array_cn', 'value_log2'),
	'EXPR': ('array_gene_expr', 'z_score'),
	'PATHA': ('array_pathway', 'activity'),
	'PATHR': ('rpkm_pathway', 'activity'),
	'TYPEA': ('array_subtype',''),
	'TYPER': ('rpkm_subtype',''),
	'xCN': ('xsq_cn', 'value_log2')
}


def genJson(dbN,af,sampStr,qText):

	qStmtL = qText.rstrip().lstrip().split('\r')

	(con,cursor) = mycgi.connectDB(db=dbN)
	
	tag = "pair_R%"

	cursor.execute('select distinct samp_id from sample_tag where tag like "%s" and tag not like "%%,%%"' % tag)
	sIdL = [x for (x,) in cursor.fetchall()]	
	sIdL.sort()

	if sampStr:
		sIdL_tmp = list(sIdL)
		sIdL = []
		for s in sampStr.split(' '):
			if s in sIdL_tmp:
				sIdL.append(s)

	nullL = ["" for x in sIdL]

	geneIdxL = []
	geneDataL = []

	for i in range(len(qStmtL)):

		qStmt = qStmtL[i].rstrip().lstrip()

		if qStmt[0]=='(' and qStmt[-1]==')':
			(qId,col,tbl,cnd) = eval(qStmt)
		elif qStmt in sampInfoH:
			(qId,col,tbl,cnd) = sampInfoH[qStmt]
		elif qStmt.count(':')==2:
			(gN,mT,mV) = qStmt.split(':')
			(tbl,col,qIdF) = mutTypeH[mT]
			if (tbl=='mutation_normal') or (tbl=='mutation_rsq'):
				qId = gN + '-' + qIdF(mV) + ':' + mT[3:]
				cnd = 'gene_symL="%s" and %s like "%%%s%%"' % (gN,col,mV)
			else:
				qId = gN + '-' + qIdF(mV)
				cnd = 'gene_sym="%s" and %s like "%%%s%%"' % (gN,col,mV)
		elif qStmt.count(':')==1:
			(gN, qId) = qStmt.split(':')
			(tbl,col) = otherTypeH[qId]
			if 'PATH' in qId:
				cnd='pathway="%s"' % gN
			elif 'TYPE' in qId:
				cnd='%s' % gN
				col = gN
			else:	
				cnd = 'gene_sym="%s"' % gN
			qId = gN + '-' +qId
		else:
			print '<b>Input Error: %s</b><br>' % qStmt
			sys.exit(1)
		
		if tbl in afColNameH:
			af_cond = 'and %s/(%s+%s) > %s' % (afColNameH[tbl][0],afColNameH[tbl][0],afColNameH[tbl][1],af)
			ord_cond = '%s desc' % afColNameH[tbl][0]
			af_frequency = ',' + afColNameH[tbl][0] + '/(' + afColNameH[tbl][0] + '+' + afColNameH[tbl][1] + ') as frequency'
			af_numerator = ',' +  afColNameH[tbl][0]
			af_denominator = ',(' + afColNameH[tbl][0] + '+' + afColNameH[tbl][1] + ') as denominator' 
		else:
			af_cond = ''
			ord_cond = col
			af_frequency = ''
			af_numerator = ''
			af_denominator = ''

		count = 0
		dataL = []
		frequency_data = []
		pair_data = []
		fraction_data = []

		for sId in sIdL:
			pair_fraction = ''
			count_flag = 0
			tag = "pair_R%"
			cursor.execute('select tag from sample_tag where samp_id="%s" and tag like "%s"' % (sId, tag))
			t = cursor.fetchone()	
			pair_id = "%s" % (t[0].split(':')[1],)
		 		
			cursor.execute('select %s %s %s %s from %s where samp_id="%s" and %s %s order by %s limit 1' % (col,af_frequency,af_numerator,af_denominator,tbl,pair_id,cnd,af_cond,ord_cond))
			p = cursor.fetchone()
			if p:
				count += 1
				count_flag = 1
				if tbl in afColNameH:
					if p[1]:
						pair_freq = pair_id + ":" + str(float(p[1]))
						pair_data.append(pair_freq)

						pair_fraction += str(int(p[2])) + '/' + str(int(p[3]))
				elif (tbl in 'rpkm_gene_expr') or (tbl in 'array_cn') or (tbl in 'array_pathway') or (tbl in 'rpkm_pathway') or (tbl in 'array_gene_expr') or (tbl in 'array_subtype') or (tbl in 'rpkm_subtype') or (tbl in 'xsq_cn'):
					pair_value = pair_id + ":" + str(float(p[0]))
					pair_data.append(pair_value)
				else:
					pair_d = pair_id +":nofreq"
					pair_data.append(pair_d)
					pair_fraction = ':'
			else:
				if tbl in afColNameH:
					if tbl in "mutation_normal":
						tag = "Xseq_%"
						cursor.execute('select samp_id from sample_tag where samp_id = "%s" and tag like "%s"' % (pair_id, tag))
						x = cursor.fetchone()
						if x:
							pair_flag = pair_id + ":" + str(0);
						else:
							pair_flag = pair_id + ":null"
						
					else:
						cursor.execute('select samp_id from splice_normal where samp_id = "%s" limit 1' % pair_id)
						m = cursor.fetchone()
						if m:
							pair_flag = pair_id + ":" + str(0);
						else:
							pair_flag = pair_id + ":null"
				else:
					pair_flag = pair_id + ":null"
				pair_data.append(pair_flag)

			cursor.execute('select %s %s %s %s from %s where samp_id="%s" and %s %s order by %s limit 1' % (col,af_frequency,af_numerator,af_denominator,tbl,sId,cnd,af_cond,ord_cond))
			r = cursor.fetchone()
			
			if r:
				dataL.append("%s" % (r[0],))
				if count_flag == 0:
					count += 1

				if tbl in afColNameH:
					if r[1]:
						fraction = str(int(r[2])) + "/" + str(int(r[3]))
						fraction_data.append(fraction+ ":" +pair_fraction)
						frequency_data.append(float(r[1]))
				else:
					fraction_data.append("")
					frequency_data.append('nofreq')
			else:
				if tbl in afColNameH:
					if tbl in "mutation_normal":
						tag = "Xseq_%"
						cursor.execute('select samp_id from sample_tag where samp_id ="%s" and tag like "%s"' % (sId, tag))
						x = cursor.fetchone()
						if x:
							data_flag = qId
						else:
							data_flag = ""
					else:
						cursor.execute('select samp_id from splice_normal where samp_id = "%s" limit 1' % sId)
						m = cursor.fetchone()
						if m:
							data_flag = qId
						else:
							data_flag = ""
				else:
					data_flag = ""

				dataL.append(data_flag)
				fraction_data.append(pair_fraction)
				frequency_data.append(0)
		
		geneIdxL.append((qId,i))
		geneDataL.append({"rppa":nullL, "hugo":qId, "mutations":dataL, "mrna":nullL, "cna":nullL, "freq":frequency_data, "pair":pair_data, "fraction":fraction_data, "percent_altered":"%s (%d%s)" % (count, 100.*count/len(sIdL), '%')})

	resultH = { \
		"dbN":dbN,
		"af":af,
		"hugo_to_gene_index":dict(geneIdxL), \
		"gene_data": geneDataL, \
		"samples": dict((sIdL[i],i) for i in range(len(sIdL)))
		}

	jsonStr = json.dumps(resultH, sort_keys=True).replace('""','null')

	#print jsonStr

	jsonFile = open('/var/www/html/js/gene_data.json','w')
	jsonFile.write(jsonStr)
	jsonFile.close()


form = cgi.FieldStorage()

if form.has_key('dbN'):
	dbN = form.getvalue('dbN')
else:
	dbN = 'ircr1'

if form.has_key('af'):
	af = float(form.getvalue('af'))
else:
	af = 0.05

if form.has_key('qText'):
	qText = form.getvalue('qText')
else:
	qText = 'Rsq\rXsq'

if form.has_key('sampStr'):
	sampStr = form.getvalue('sampStr')
else:
	sampStr = ''

genJson(dbN,af,sampStr,qText)

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Oncoprint (%s)</title>

<link href="js/jquery-ui-1.8.14.custom.css" rel="stylesheet">
<link href="js/jquery.qtip.min.css" type="text/css" rel="stylesheet">
<link href="js/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">

<script src="http://code.jquery.com/jquery.js"></script>
<script src="js/jquery.min.js"></script>
<script src="js/jquery.qtip.min.js"></script>
<script src="js/jquery-ui-1.8.14.custom.min.js"></script>
<script src="js/bootstrap/js/bootstrap.min.js"></script>
<script src="js/d3.v2.min.js"></script>

<script src="js/MemoSort.js"></script>
<script src="js/oncoprint_demo.js"></script>
<script src="js/js_patient/oncoprint_patient.js"></script>
<script src="js/js_patient/QueryGeneData.js"></script>

<script type="text/javascript">

var $ex_EGFR = "Rsq\\rEGFR:SKIP:25-27\\rEGFR:SKIP:25-26\\rEGFR:SKIP:27-27\\rEGFR:3pDEL:24/28\\rEGFR:3pDEL:27/28\\rEGFR:3pDEL:26/28\\rEGFR:SKIP:2-7\\rEGFR:SKIP:12-13\\rEGFR:MUTR:A289\\rEGFR:MUTX:A289\\rEGFR:MUTR:R222\\rEGFR:MUTX:R222\\rEGFR:MUTR:G598\\rEGFR:MUTX:G598\\rEGFR:MUTR:R108\\rEGFR:MUTX:R108\\rEGFR:CNA\\rEGFR:xCN\\rEGFR:RPKM\\rEGFR:EXPR\\rXsq";

var $ex_IDH1 = "Rsq\\rIDH1:MUT:R132\\rXsq";

$(document).ready(function() {

    $('#ex_EGFR').click(function () {
		$('#qText').val($ex_EGFR)
	});

	$('#ex_IDH1').click(function() { 
		$('#qText').val($ex_IDH1)
	});

})

</script>

</head>''' % mycgi.db2dsetN[dbN]


print '''
<body>
<div class='row-fluid'>
<div class="span1"></div>
<div class="span12">
<h2>Oncoprint <small> (%s) </small></h2>
''' % (mycgi.db2dsetN[dbN],)


print '<dl><dt><i class="icon-search"></i> Input (per line):</dt><dd>[sample info] OR [gene name]:[mutation type]:[mutation value] OR [(qId,col,tbl,cnd)]</dd></dl>'

print '<dl><dt><i class="icon-tags"></i> [sample info]</dt>'
for scut in ['Rsq','Xsq']:
    print '<dd><i class="icon-chevron-down"></i>  %s: %s </dd>' % (scut,str(sampInfoH[scut]))

print '''<dt><i class="icon-tags"></i> [mutation type]: eg. [mutation value]</dt>
<dd><i class="icon-chevron-down"></i> CNA or xCN</dd>
<dd><i class="icon-chevron-down"></i> EXPR or RPKM</dd>
<dd><i class="icon-chevron-down"></i> MUT: eg. A289</dd>
<dd><i class="icon-chevron-down"></i> SKIP: eg. 2-7</dd>
<dd><i class="icon-chevron-down"></i> 3pDEL: eg. 24/28</dd>
'''

print '''<dt><i class="icon-tags"></i> [(qId,col,tbl,cnd)]</dt>
<dd><i class="icon-chevron-down"></i> ('EGFR-A289:X','ch_aa','mutation_normal','gene_symL="EGFR" and ch_aa like "%A289%"')</dd>
<dd><i class="icon-chevron-down"></i> ('TP53-splice','ch_dna','mutation_normal','gene_symL="TP53" and ch_dna like "%c.523+1G%"')</dd>
<dd><i class="icon-chevron-down"></i> ('EGFR-fusion','concat(gene_sym1,"-",gene_sym2)','splice_fusion_AF','(gene_sym1="EGFR" or gene_sym2="EGFR") and frame!=""')</dd>
<dd><i class="icon-chevron-down"></i> ('2-7','delExons','splice_skip_AF','gene_sym="EGFR" and delExons like "%2-7%"')</dd>
<dd><i class="icon-chevron-down"></i> ('25-','juncAlias','splice_eiJunc_AF','gene_sym="EGFR" and juncAlias like "%24/28%"')</dd>
'''

print '<br><dt><i class="icon-gift"></i> Example query: <a href="#current" id="ex_EGFR">[EGFR]</a> <a href="#current" id="ex_IDH1">[IDH1]</a></dt>'

print '</dl>'

print '''
<form method='get'>
Dataset: <select name='dbN' style="width:130px; height:23px; font-size:9pt">
<option value ='ircr1' %s>AVATAR GBM</option>
<option value ='tcga1' %s>TCGA GBM</option>
<option value ='ccle1' %s>CCLE</option>
</select>''' % (('selected' if dbN=='ircr1' else ''),('selected' if dbN=='tcga1' else ''),('selected' if dbN=='ccle1' else ''))

print '''
Mutant allelic frequency: <select name='af' style="width:80px; height:23px; font-size:9pt">
<option value ='0.01' %s>>0.01</option>
<option value ='0.05' %s>>0.05</option>
<option value ='0.1' %s>>0.10</option>
<option value ='0.5' %s>>0.50</option>
</select><br>
Samples: <br><textarea name='sampStr' id='sampStr' rows='2' style="width:550px">%s</textarea><br>
Query:<br><textarea name='qText' cols='50' rows='15' id='qText' style="width:550px">%s</textarea><br>
<input type='submit' value='Submit' class="btn">
</form>
''' % (('selected' if af==0.01 else ''),('selected' if af==0.05 else ''),('selected' if af==0.10 else ''),('selected' if af==0.50 else ''), sampStr, qText)

print '''

<div id="oncoprint_controls">
<input type="checkbox" onclick="oncoprint.toggleUnaltered();"> remove unaltered cases <br>
<input type="checkbox" onclick="if ($(this).is(':checked')) {oncoprint.defaultSort();} else {oncoprint.memoSort();}"> Restore case order <br>
<input type="checkbox" onclick="oncoprint.toggleWhiteSpace();"> Remove Whitespace<br>
<br><span>Zoom</span>
<div id="zoom" style="display: inline-table;"></div></div>'''

print'''
<br>
<div id="oncoprint"></div>
<br><br>
Download :  
<form id="oncoprintForm" action="oncoprint_download.py" enctype="multipart/form-data" method="POST" onsubmit="this.elements['xml'].value=oncoprint.getOncoPrintBodyXML(); return true;" target="_blank" style="display: inline">
<input type="hidden" name="xml">
<input type="hidden" name="longest_label_length">
<input type="hidden" name="format" value="svg">
<input type="submit" class="btn" value="SVG">
</form>
<form id="oncoprintForm" action="oncoprint_download_pdf.py" enctype="multipart/form-data" method="POST" onsubmit="this.elements['xml2'].value=oncoprint.getOncoPrintBodyXML(); return true;" target="_blank" style="display: inline">
<input type="hidden" name="xml2">
<input type="hidden" name="longest_label_length">
<input type="hidden" name="format" value="pdf">
<input type="submit" class="btn" value="PDF">
</form><br><br><br>
</div></div></body>
</html>'''

