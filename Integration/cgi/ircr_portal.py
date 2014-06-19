#!/usr/bin/python

import sys, cgi
import mycgi


form = cgi.FieldStorage()

if form.has_key('geneN'):
	geneN = form.getvalue('geneN')
else:
	geneN = 'EGFR'

if form.has_key('sId'):
	sId = form.getvalue('sId')
else:
	sId = 'IRCR_GBM_352_TR'

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
<title>AVATAR Cancer Genome Viewer</title>
<link href="/js/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">

<style type="text/css">
hr{
color: #000000;
background-color: #000000;
}
</style>

<script type="text/javascript" src="http://code.jquery.com/jquery-1.3.2.js"></script>
<script type="text/javascript" src="/js/bootstrap/js/bootstrap.min.js"></script>

</head>
<body>
<div class="row-fluid">
<div class="span12" style="margin-left:10px; margin-top:10px;">
<table cellpadding=20 border=0 align='center'>
<tr>
<td colspan=2><font size=5><b>AVATAR Cancer Genome Viewer</b></font><hr color='black'/></td>
</tr>
<tr>
<td>
<p>Query by Patient:</p>
<form method='get' class="form-inline" action="ircr_samp.py">
<select name='dbN' style="width:120px; height:23px; font-size:9pt">
'''

mycgi.dbOptions(dbN)

print '''
</select>
<input type='text' name='sId' value='%s' style="width:130px; height:15px; font-size:9pt">
<input type='submit' class="btn btn-small" value='Submit'>
</form>
</td>
</tr>
<tr>
<td>
<p>Query by Gene:</p>
<form method='get' class="form-inline" action="ircr.py">
<select name='dbN' style="width:120px; height:23px; font-size:9pt">
''' % (sId)

mycgi.dbOptions(dbN)

print '''
</select>
<input type='text' name='sId' value='%s' style="width:130px; height:15px; font-size:9pt">
<input type='submit' class="btn btn-small" value='Submit'>
</form>
</td>
</tr>
</table>
''' % (geneN)
