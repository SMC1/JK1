#!/usr/bin/python

import sys, os, cgi

sys.path.append('/home/jinkuk/JK1/modules')

altTypeH = {
	'expr': ('array_gene_expr', 'z_score', 'gene_sym', 'array, z-score'),
	'rpkm': ('rpkm_gene_expr_lg2', 'lg2_rpkm', 'gene_sym', 'log2(rpkm+1)'),
	'methyl': ('methyl_view', 'fraction','gene_sym', 'methylation'),
	'cna': ('array_cn', 'value_log2','gene_sym', 'log2(copy number)'),
	'pathway': ('array_pathway', 'activity','pathway', 'activity')
	}

dsetH = {
	'tcga1': 'TCGA GBM',
	'ircr1': 'AVATAR GBM',
	}

def main(geneN1, geneN2, altType1='rpkm', altType2='rpkm', dset='tcga1'):

	tblN1,valN1,featN1,lab1 = altTypeH[altType1]
	tblN2,valN2,featN2,lab2 = altTypeH[altType2]

	ret1 = os.system('''(echo "SELECT t1.samp_id,t1.%s %s,t2.%s %s FROM %s t1, %s t2 where t1.%s='%s' and t2.%s='%s' and t1.samp_id=t2.samp_id" | mysql %s -u cancer --password=cancer > /var/www/html/tmp/correlation.txt) &> /var/www/html/tmp/correaltion.err''' % \
		(valN1,geneN1, valN2,geneN2, tblN1,tblN2, featN1,geneN1, featN2,geneN2, dset))

	ret2 = os.system('Rscript correlation.r "%s" "%s" "%s" png &>> /var/www/html/tmp/correaltion.err' % (dsetH[dset],lab1,lab2))

	return ret1!=0 or ret2!=0

form = cgi.FieldStorage()

if form.has_key('dset'):
	dset = form.getvalue('dset')
else:
	dset = 'tcga1'

if form.has_key('altType1'):
	altType1 = form.getvalue('altType1')
else:
	altType1 = 'expr'

if form.has_key('geneN1'):
	geneN1 = form.getvalue('geneN1')
else:
	geneN1 = 'NRP1'

if form.has_key('altType2'):
	altType2 = form.getvalue('altType2')
else:
	altType2 = 'expr'

if form.has_key('geneN2'):
	geneN2 = form.getvalue('geneN2')
else:
	geneN2 = 'SEMA2A'

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Correlation analysis</title>
</head>'''

error = main(geneN1,geneN2,altType1,altType2,dset)

if error:
	print 'Error: <pre>%s</pre>' % (open('/var/www/html/tmp/correaltion.err').read(),)
else:
	print '<img src="/tmp/correlation.png">'

print "<form method='get'>"

print '''
<br>
<select name='dset'>
<option value='tcga1' %s>%s</option>
<option value='ircr1' %s>%s</option>
</select>
''' % (
('selected' if dset=='tcga1' else ''), dsetH['tcga1'],
('selected' if dset=='ircr1' else ''), dsetH['ircr1'],
)

print '''
<br>X: 
<select name='altType1'>
<option value='expr' %s>expr-array</option>
<option value='rpkm' %s>expr-RNASeq</option>
<option value='methyl' %s>methyl</option>
<option value='cna' %s>CNA</option>
<option value='pathway' %s>Pathway</option>
</select>
<input type='text' name='geneN1' size=10 value='%s'>
''' % (
('selected' if altType1=='expr' else ''),
('selected' if altType1=='rpkm' else ''),
('selected' if altType1=='methyl' else ''),
('selected' if altType1=='cna' else ''),
('selected' if altType1=='pathway' else ''),
geneN1)

print '''
<br>Y: 
<select name='altType2'>
<option value='expr' %s>expr-array</option>
<option value='rpkm' %s>expr-RNASeq</option>
<option value='methyl' %s>methyl</option>
<option value='cna' %s>CNA</option>
<option value='pathway' %s>Pathway</option>
</select>
<input type='text' name='geneN2' size=10 value='%s'>
''' % (
('selected' if altType2=='expr' else ''),
('selected' if altType2=='rpkm' else ''),
('selected' if altType2=='methyl' else ''),
('selected' if altType2=='cna' else ''),
('selected' if altType2=='pathway' else ''),
geneN2)

print '''<br><input type='submit' value='Submit'>
</form>'''


print '''</html>'''
