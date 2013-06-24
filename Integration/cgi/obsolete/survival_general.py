#!/usr/bin/python

import sys, os, cgi

sys.path.append('/home/jinkuk/JK1/modules')
import mymath, mymysql

sampInfoH = { 
	'Rsq': ('Rsq','samp_id','splice_normal','True'),
	'Xsq': ('Xsq','tag','sample_tag','tag like "XSeq_%"')
}

afColNameH = {
	'mutation': ('nReads_alt','nReads_ref'),
	'splice_fusion_AF': ('nReads','nReads_w1'),
	'splice_skip_AF': ('nReads','nReads_w1'),
	'splice_eiJunc_AF': ('nReads','nReads_w')
}

mutTypeH = {
	'MUT': ('mutation','ch_aa', lambda x:x),
	'SKIP': ('splice_skip_AF','delExons', lambda x:x),
	'3pDEL': ('splice_eiJunc_AF','juncAlias', lambda x: '%s-' % (int(x.split('/')[0])+1,))
}

altTypeH = {
	'METH': ('methyl_view', 'fraction'),
	'EXPR': ('array_gene_expr', 'z_score'),
	'RPKM': ('rpkm_gene_expr', 'log2(rpkm+1)'),
	'CNA': ('array_cn', 'value_log2')
	}

def main(dataN='TCGA_GBM', query):

	con,cursor = mymysql.connectDB(db='tcga1')

	geneN,altType,feature,cutoff = query.split(':')

	cursor.execute('create temporary table t1 select samp_id pId, % value from %s where gene_sym="%s"' % \
		(altTypeH[altType][1],altTypeH[altType][0],geneN))

	cursor.execute('select value from t1')
	valueL = [v for (v,) in cursor.fetchall()]; l = len(valueL)


	recordL = mymysql.dictSelect("SELECT pId,days_followup time,if(days_death is not null,1,0) event,%s value \
		FROM clinical join %s on pId=samp_id and gene_sym='%s'" % (altTypeH[altType][1],altTypeH[altType][0],geneN), cursor)

	threshold = (mymath.percentile(valueL,cutoff[0]), mymath.percentile(valueL,100-cutoff[1]))

	outFile = open('/var/www/html/survival/survival.mvc','w')

	colN = ['pId','time','event','value','label','priority']

	outFile.write('\t'.join(colN)+'\n')

	for r in recordL:

		if r['value'] < threshold[0]:

			label = '"%s %s < B%s%% (%.2f)"' % (geneN,altType,cutoff[0],threshold[0])
			priority = '1'

		elif r['value'] >= threshold[1]:

			label = '"%s %s > T%s%% (%.2f)"' % (geneN,altType,cutoff[1],threshold[1])
			priority = '2'

		else:

			label = '"%s %s Middle"' % (geneN,altType)
			priority = '9'

		outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (r['pId'], r['time'], r['event'], r['value'], label, priority))

	outFile.close()

	ret1 = os.system('Rscript distribution.r /var/www/html/survival/survival.mvc &> /var/www/html/survival/error_distr.txt')
	ret2 = os.system('Rscript survival.r /var/www/html/survival/survival.mvc &> /var/www/html/survival/error_surv.txt')

	return ret1!=0 or ret2!=0


form = cgi.FieldStorage()

if form.has_key('altType'):
	altType = form.getvalue('altType')
else:
	altType = 'METH'

if form.has_key('geneN'):
	geneN = form.getvalue('geneN')
else:
	geneN = 'MGMT'

if form.has_key('cutoff_b'):
	cutoff_b = int(form.getvalue('cutoff_b'))
else:
	cutoff_b = 50

if form.has_key('cutoff_t'):
	cutoff_t = int(form.getvalue('cutoff_t'))
else:
	cutoff_t = 50

if form.has_key('query'):
	query = form.getvalue('query')
else:
	query = 'MGMT:METH::<0.1'

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Survival analysis</title>
</head>'''

error = main(query=query)

if error:
	print 'Error: <pre>%s</pre>' % (open('/var/www/html/survival/error.txt').read(),)
else:
	print '<img src="/survival/distribution.png">'
	print '<img src="/survival/survival_km.png">'

#print "<hr><form method='get'>"
#
#print '''
#Alteration: 
#<select name='altType'>
#<option value='METH' %s>methylation</option>
#<option value='EXPR' %s>expr-array</option>
#<option value='RPKM' %s>expr-RNASeq</option>
#<option value='CNA' %s>CNA</option>
#</select>''' % (('selected' if altType=='METH' else ''),('selected' if altType=='EXPR' else ''),('selected' if altType=='RPKM' else ''),('selected' if altType=='CNA' else ''))
#
#print '''
#<br>Gene: <input type='text' name='geneN' size=10 value='%s'>
#<br>Cut off: bottom <input type='text' name='cutoff_b' size=2 value='%s'>%%, top <input type='text' name='cutoff_t' size=2 value='%s'>%%
#<br><input type='submit' value='Submit'>
#</form>''' % (geneN,cutoff_b,cutoff_t)

print '<hr>'

print '''
<form method='get'>
<textarea name='query' cols='100' rows='5'>%s</textarea><br>
<input type='submit' value='Submit'>
</form>''' % (query,)

print '''</html>'''
