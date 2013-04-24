#!/usr/bin/python

import sys, cgi, json
import mycgi

sampInfoH = { \
	'Rsq': ('Rsq','samp_id','splice_normal','True'),
	'Xsq': ('Xsq','tag','sample_tag','tag like "XSeq_%"')
	}

afColNameH = {
	'mutation': ('nReads_alt','nReads_ref'),
	'splice_fusion_AF': ('nReads','nReads_w1'),
	'splice_skip_AF': ('nReads','nReads_w1'),
	'splice_eiJunc_AF': ('nReads','nReads_w'),
}

mutTypeH = {
	'MUT': ('mutation','ch_aa', lambda x:x),
	'SKIP': ('splice_skip_AF','delExons', lambda x:x),
	'3pDEL': ('splice_eiJunc_AF','juncAlias', lambda x: '%s-' % (int(x.split('/')[0])+1,))
}


def genJson(dbN,af,qText):

	qStmtL = qText.rstrip().lstrip().split('\r')

	(con,cursor) = mycgi.connectDB(db=dbN)

	cursor.execute('select distinct samp_id from array_gene_expr union select distinct samp_id from array_cn union select distinct samp_id from splice_normal union select distinct samp_id from mutation')
	sIdL = [x for (x,) in cursor.fetchall()]
	sIdL.sort()
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
			qId = qIdF(mV)
			cnd = 'gene_sym="%s" and %s like "%s%s%s"' % (gN,col,'%',mV,'%')
		else:
			print '<b>Input Error: %s</b><br>' % qStmt
			sys.exit(1)
		
		if tbl in afColNameH:
			af_cond = 'and %s/(%s+%s) > %s' % (afColNameH[tbl][0],afColNameH[tbl][0],afColNameH[tbl][1],af)
			ord_cond = '%s desc' % afColNameH[tbl][0]
		else:
			af_cond = ''
			ord_cond = col

		count = 0
		dataL = []

		for sId in sIdL:
			cursor.execute('select %s from %s where samp_id="%s" and %s %s order by %s limit 1' % (col,tbl,sId,cnd,af_cond,ord_cond))
			r = cursor.fetchone()
			if r:
				dataL.append("%s" % (r[0],))
				count += 1
			else:
				dataL.append("")

		geneIdxL.append((qId,i))
		geneDataL.append({"rppa":nullL, "hugo":qId, "mutations":dataL, "mrna":nullL, "cna":nullL, "percent_altered":"%s (%d%s)" % (count, 100.*count/len(sIdL), '%')})

	resultH = { \
		"dbN":dbN,
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

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Oncoprint (%s)</title>
<link href="http://www.cbioportal.org/public-portal/css/redmond/jquery-ui-1.8.14.custom.css" rel="stylesheet">
<link href="http://www.cbioportal.org/public-portal/css/jquery.qtip.min.css" type="text/css" rel="stylesheet">
<script src="http://code.jquery.com/jquery.js"></script>
<script type="text/javascript" src="/js/d3.v2.min.js"></script>
<script src="/js/jquery.min.js"></script>
<script src="/js/jquery-ui-1.8.14.custom.min.js"></script>
<script src="http://www.cbioportal.org/public-portal/js/jquery.qtip.min.js"></script>
<script src="/js/MemoSort.js"></script>
<script src="/js_yn/oncoprint.js"></script>
<script src="/js/QueryGeneData.js"></script>
<script src="/js/oncoprint_demo.js"></script>
<script src="http://www.cbioportal.org/public-portal/js/jquery-ui-1.8.14.custom.min.js"></script>

<script type="text/javascript">

var $ex_EGFR = "Rsq\\rEGFR:SKIP:25-27\\rEGFR:SKIP:25-26\\rEGFR:SKIP:27-27\\rEGFR:3pDEL:24/28\\rEGFR:3pDEL:27/28\\rEGFR:3pDEL:26/28\\rEGFR:SKIP:2-7\\rEGFR:SKIP:12-13\\rEGFR:MUT:A289\\rEGFR:MUT:R222\\rEGFR:MUT:G598\\rEGFR:MUT:R108\\rXsq";

$(document).ready(function() {

    $('#ex_EGFR').click(function () {
		$('textarea').val($ex_EGFR)
	});

})

</script>

</head>''' % mycgi.db2dsetN[dbN]


print '''
<body>
<div>
<h2>Oncoprint (%s)</h2>
''' % (mycgi.db2dsetN[dbN],)


print 'Input (per line): <br>[sample info] OR [gene name]:[mutation type]:[mutation value] OR [(qId,col,tbl,cnd)] <br>'

print '<dl>[sample info]'
for scut in ['Rsq','Xsq']:
    print '<dt> * %s: %s </dt>' % (scut,str(sampInfoH[scut]))

print '''<dl>[mutation type]: eg. [mutation value]
<dt> * MUT: eg. A289</dt>
<dt> * SKIP: eg. 2-7</dt>
<dt> * 3pDEL: eg. 24/28</dt>
'''

print '''<dl>[(qId,col,tbl,cnd)]
<dt> * ('A289','ch_aa','mutation','gene_sym="EGFR" and ch_aa like "%A289%"')</dt>
<dt> * ('2-7','delExons','splice_skip_AF','gene_sym="EGFR" and delExons like "%2-7%"')</dt>
<dt> * ('25-','juncAlias','splice_eiJunc_AF','gene_sym="EGFR" and juncAlias like "%24/28%"')</dt>
'''

print '<p>Example query: <a href="#current" id="ex_EGFR">[EGFR]</a></p>'

print '</dl><br>'

print '''
<form method='get'>
Dataset:<select name='dbN'>
<option value ='ircr1' %s>AVATAR GBM</option>
<option value ='tcga1' %s>TCGA GBM</option>
<option value ='ccle1' %s>CCLE</option>
</select>''' % (('selected' if dbN=='ircr1' else ''),('selected' if dbN=='tcga1' else ''),('selected' if dbN=='ccle1' else ''))

print '''
Mutant allelic frequency:<select name='af'>
<option value ='0.01' %s>>0.01</option>
<option value ='0.05' %s>>0.05</option>
<option value ='0.1' %s>>0.10</option>
<option value ='0.5' %s>>0.50</option>
</select><br>
<textarea name='qText' cols='50' rows='15' id='qText'>%s</textarea><br>
<input type='submit' value='Submit'>
</form>
</div> 
''' % (('selected' if af==0.01 else ''),('selected' if af==0.05 else ''),('selected' if af==0.10 else ''),('selected' if af==0.50 else ''), qText)

if qText != 'null':
	genJson(dbN,af,qText)

print '''
<br>
<div id="oncoprint_controls">
<input type="checkbox" onclick="oncoprint.toggleUnaltered();"> remove unaltered cases <br>
<input type="checkbox" onclick="if ($(this).is(":checked")) {oncoprint.defaultSort();} else {oncoprint.memoSort();}"> Restore case order <br>
<input type="checkbox" onclick="oncoprint.toggleWhiteSpace();"> Remove Whitespace<br>
<span>Zoom</span>
<div id="zoom" style="display: inline-table;"></div></div>'''

print'''
<br>
<form id="oncoprintForm" action="oncoprint_download.py" enctype="multipart/form-data" method="POST" onsubmit="this.elements['xml'].value=oncoprint.getOncoPrintBodyXML(); return true;" target="_blank">
<input type="hidden" name="xml">
<input type="hidden" name="longest_label_length">
<input type="hidden" name="format" value="svg">
Download SVG : <input type="submit" value="SVG">
</form>

<div id="oncoprint"></div>
</body>
</html>'''

