#!/usr/bin/python

import sys, os, cgi

sys.path.append('/home/jinkuk/JK1/modules')
import mymath, mymysql


#altTypeH = {
#	'methyl': ('methyl_view', 'fraction'),
#	'expr': ('array_gene_expr', 'z_score'),
#	'rpkm': ('rpkm_gene_expr', 'log2(rpkm+1)'),
#	'cna': ('array_cn', 'value_log2')
#	}


CIMP = ['TCGA-12-0827','TCGA-02-0010','TCGA-02-0014','TCGA-02-0028','TCGA-02-0058','TCGA-02-0080','TCGA-02-0114','TCGA-06-0128','TCGA-06-0129','TCGA-02-2483','TCGA-06-1805','TCGA-06-2570','TCGA-06-5417','TCGA-06-6389','TCGA-12-0818','TCGA-14-1456','TCGA-14-1458','TCGA-14-1821','TCGA-14-4157','TCGA-16-0849','TCGA-16-0850','TCGA-16-1460','TCGA-19-1788','TCGA-19-2629','TCGA-26-1442','TCGA-26-5133','TCGA-27-2521','TCGA-28-1756','TCGA-32-4208']

def main(dataN='TCGA_GBM', endPoint='death',  geneN='EGFR', altType='2-7', cutoff=(50,50)):

	colN = ['pId','time','event','value','label','priority']

	con,cursor = mymysql.connectDB(db='tcga1')

	cursor.execute('create temporary table t1 select distinct samp_id pId from splice_normal')

	cursor.execute('create temporary table t2 \
		select pId, nReads/(nReads+nReads_w1) af from t1 left join splice_skip_AF on pId=samp_id and gene_sym="EGFR" and delExons like "%2-7%"')

	cursor.execute('update t2 set af=0 where af is null')

	recordL = mymysql.dictSelect("SELECT pId,days_followup time,if(days_death is not null,1,0) event, af value \
		FROM clinical join t2 using (pId)", cursor)

#	valueL = [r['value'] for r in recordL]
#	l = len(valueL)

	threshold = (0.01,0.01)

	outFile = open('/var/www/html/tmp/survival.mvc','w')

	outFile.write('\t'.join(colN)+'\n')

	for r in recordL:
		
		r['value'] = float(r['value'])

		if r['value'] < threshold[0]:

			label = '"%s %s < %.2f"' % (geneN,altType,threshold[0])
			priority = '1'

		elif r['value'] >= threshold[1]:

			label = '"%s %s > %.2f"' % (geneN,altType,threshold[1])
			priority = '2'

		else:

			label = '"%s %s Middle"' % (geneN,altType)
			priority = '9'

		if r['pId'] not in CIMP:
			outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (r['pId'], r['time'], r['event'], r['value'], label, priority))

	outFile.close()

	ret1 = os.system('Rscript distribution.r /var/www/html/tmp/survival.mvc png &> /var/www/html/tmp/error_distr.txt')
	ret2 = os.system('Rscript survival.r /var/www/html/tmp/survival.mvc png &> /var/www/html/tmp/error_surv.txt')

	return ret1!=0 or ret2!=0

#form = cgi.FieldStorage()
#
#if form.has_key('altType'):
#	altType = form.getvalue('altType')
#else:
#	altType = 'methyl'
#
#if form.has_key('geneN'):
#	geneN = form.getvalue('geneN')
#else:
#	geneN = 'MGMT'
#
#if form.has_key('cutoff_b'):
#	cutoff_b = int(form.getvalue('cutoff_b'))
#else:
#	cutoff_b = 50
#
#if form.has_key('cutoff_t'):
#	cutoff_t = int(form.getvalue('cutoff_t'))
#else:
#	cutoff_t = 50

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Survival analysis</title>
</head>'''

error = main()
#error = main(altType=altType,geneN=geneN,cutoff=(cutoff_b,cutoff_t))

if error:
	print 'Error: <pre>%s</pre>' % (open('/var/www/html/tmp/error_distr.txt').read(),)
	print 'Error: <pre>%s</pre>' % (open('/var/www/html/tmp/error_surv.txt').read(),)
else:
	print '<img src="/tmp/distribution.png">'
	print '<img src="/tmp/survival_km.png">'

#print "<form method='get'>"
#
#print '''
#Alteration: 
#<select name='altType'>
#<option value='methyl' %s>methyl</option>
#<option value='expr' %s>expr-array</option>
#<option value='rpkm' %s>expr-RNASeq</option>
#<option value='cna' %s>CNA</option>
#</select>''' % (('selected' if altType=='methyl' else ''),('selected' if altType=='expr' else ''),('selected' if altType=='rpkm' else ''),('selected' if altType=='cna' else ''))
#
#print '''
#<br>Gene: <input type='text' name='geneN' size=10 value='%s'>
#<br>Cut off: bottom <input type='text' name='cutoff_b' size=2 value='%s'>%%, top <input type='text' name='cutoff_t' size=2 value='%s'>%%
#<br><input type='submit' value='Submit'>
#</form>''' % (geneN,cutoff_b,cutoff_t)

print '''</html>'''
