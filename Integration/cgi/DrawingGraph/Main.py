#!/usr/bin/python

import cgi

from Parser import *
from Crawler import *
from Converter import *

form = cgi.FieldStorage()
if form.has_key('geneN'):
	geneN = form.getvalue('geneN')
else:
	geneN = 'EGFR'

if form.has_key('dbN'):
	dbN = form.getvalue('dbN')
else:
	dbN = 'ircr1'

if form.has_key('items'):
	items = form.getvalue('items')
else:
	items = "Rsq,CN >1.5"


#call Parser to parsing args
parser = Parser()
item_list = []
item_list = parser.parsing_input(items, geneN, dbN)

#call Crawler to get data from db
crawler = Crawler(dbN, geneN, item_list)

tag_index = ['inv_', 'pair_', 'panel_screening', 'RNA-Seq', 'tum_', 'Xseq_']

#swich / case
cnd_cnt_cn = 0
cnd_cnt_skip = 0
cnd_cnt_mutation = 0
cnd_cnt_deletion = 0
cnd_cnt_expr = 0
for item in item_list:
	if "CN" in item :
		condition_cn_list = parser.get_condition_cn_list()
		crawler.crawlingData_CN(geneN, condition_cn_list, cnd_cnt_cn)
		cnd_cnt_cn += 1

	if "SKIP" in item:
		condition_skip_list = parser.get_condition_skip_list()
		crawler.crawlingData_skip(geneN, condition_skip_list, cnd_cnt_skip)
		cnd_cnt_skip += 1

	if "MUT" in item:
		mutation_item_list = parser.get_mutation_item_list()
		crawler.crawlingData_mutation(geneN, mutation_item_list)
		cnd_cnt_mutation += 1

	if "DEL" in item:
		del_list = parser.get_deletion_item_list()
		crawler.crawlingData_del(geneN, del_list, cnd_cnt_deletion)
		cnd_cnt_deletion += 1

	if "expr" in item:
		condition_expr_list = parser.get_condition_expr_list()
		crawler.crawlingData_expr(geneN, condition_expr_list, cnd_cnt_expr)
		cnd_cnt_expr += 1

if "Rsq" in item_list:
	crawler.crawlingData_Rsq()

for tag in tag_index:
	if any(tag in item for item in item_list):
		tag_item_list = parser.get_tag_item_list()
		crawler.crawlingData_tag(tag_item_list)
		break

sample_list = crawler.get_sample_list()
converter = Converter(sample_list, item_list)
converter.writing_txt()
converter.writing_json()
converter.find_and_replace()

print "Content-type: text/html\r\n\r\n";

print'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>FIXME</title>
<!--
<link rel="stylesheet" type="text/css" href="FIXME" />
<script type="text/javascript" src="FIXME"></script>
<style type="text/css">
/* <![CDATA[ */
/* ]]> */
</style>
-->
<link href="/js/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
</head>
<body>
<div class = "row-fluid">
<div class = "span10 offset1">
<h3>Query guide</h3>
<dl>
	<dt> * Item to query : Query </dt>
	<dt> * SCRN : panel_screening </dt>
	<dt> * Rsq : Rsq </dt>
	<dt> * Xseq : Xseq_% </dt>
	<dt> * pair : pair_% </dt>
	<dt> * tum : tum_% </dt>
	<dt> * inv : inv_% </dt>
	<dt> * expression : expr all or expr operator(>,<,>=,<=) number </dt>
		<dd> ex) expr >0.5 </dd>
	<dt> * copy number : CN all or CN operator(>,<,>=,<=) number </dt>
		<dd> ex) CN >1.5 </dd>
	<dt> * mutation : MUT name </dt>
		<dd> ex) MUT p.A289V </dd>
	<dt> * exon skip : SKIP location or SKIP location and nReads operator(>,<,<=,>=) number </dt>
		<dd> ex) SKIP 12-13 or SKIP 12-13 and nReads >=20 </dd>
	<dt> * 3p deletion : DEL location or DEL location and nReads operator(>,<,<=,>=) number </dt>
		<dd> ex) DEL 3/28 or DEL 7 and nReads >100 </dd>
	<dt> * delimiter : ',' (space between queries is not allowed) </dt>
</dl><br>'''

print '''
	 <form method='get'>
		Select DB :
		<select name='dbN'>
			<option value ='ircr1' name='dbN' %s>IRCR GBM</option>
			<option value ='tcga1' name='dbN' %s>TCGA GBM</option>
			<!--<option value ='ccle1' name='dbN'>CCLE</option> -->
		</select> <br>
		Gene Name : <input type='text' name='geneN' placeholder="%s"> <br>
		Query : <textarea name='items' cols="25" rows="5">%s </textarea>
		<input type='submit' class="btn" value='Submit'>
	</form>

	<div id="oncoprint"></div>

	<br><br><br>
</div>
</div>

</body>
<script src="http://code.jquery.com/jquery.js"></script>
<script src="/js/bootstrap/js/bootstrap.min.js"></script>
<script type="text/javascript" src="/js/d3.v2.min.js"></script>

<script src="/js/jquery.min.js"></script>
<script src="/js/jquery-ui-1.8.14.custom.min.js"></script>
<script src="/js/MemoSort.js"></script>
<script src="/js/oncoprint.js"></script>
<script src="/js/QueryGeneData.js"></script>
<script src="/js/oncoprint_demo.js"></script>
</html> ''' % (('selected' if dbN=='ircr1' else ''),('selected' if dbN=='tcga1' else ''),geneN, items)
