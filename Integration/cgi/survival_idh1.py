#!/usr/bin/python

import sys, os, cgi

sys.path.append('/home/jinkuk/JK1/modules')
import mymath, mymysql


altTypeH = {
	'methyl': ('methyl_view', 'fraction','gene_sym'),
	'expr': ('array_gene_expr', 'z_score','gene_sym'),
	'rpkm': ('rpkm_gene_expr', 'log2(rpkm+1)','gene_sym'),
	'cna': ('array_cn', 'value_log2','gene_sym'),
	'pathway': ('array_pathway', 'activity','pathway')
	}


def main(dataN='TCGA_GBM', endPoint='death',  geneN='MGMT', altType='methyl', cutoff=(50,50)):

	colN = ['pId','time','event','value','label','priority']

	con,cursor = mymysql.connectDB(db='tcga1')

	cursor.execute('select samp_id from mutation_normal where gene_symL="IDH1" and ch_aa like "%sR132%s"' % ('%','%'))
	idh1 = [x[0] for x in cursor.fetchall()]

	recordL = mymysql.dictSelect("SELECT pId,days_followup time,if(days_death is not null,1,0) event,%s value \
		FROM clinical join %s on pId=samp_id and %s='%s'" % (altTypeH[altType][1],altTypeH[altType][0],altTypeH[altType][2],geneN), cursor)

	recordL2=[]
	for i in range(len(recordL)):
		if recordL[i]['pId'] in idh1:
			continue
		else:
			recordL2.append(recordL[i])
	recordL = recordL2	
	
#	for r in recordL:
#		if r['pId'] in idh1:
#			recordL.remove(r)

	valueL = [r['value'] for r in recordL]
	l = len(valueL)

	threshold = (mymath.percentile(valueL,cutoff[0]), mymath.percentile(valueL,100-cutoff[1]))

	outFile = open('/var/www/html/tmp/survival.mvc','w')

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

	ret1 = os.system('Rscript distribution.r /var/www/html/tmp/survival.mvc &> /var/www/html/tmp/error_surv.txt')
	ret2 = os.system('Rscript survival.r /var/www/html/tmp/survival.mvc png &>> /var/www/html/tmp/error_surv.txt')
	os.system('Rscript survival.r /var/www/html/tmp/survival.mvc pdf &>> /var/www/html/tmp/error_surv.txt')

	return ret1!=0 or ret2!=0

form = cgi.FieldStorage()

if form.has_key('altType'):
	altType = form.getvalue('altType')
else:
	altType = 'methyl'

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

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Survival analysis</title>
</head>'''

error = main(altType=altType,geneN=geneN,cutoff=(cutoff_b,cutoff_t))

if error:
	print 'Error: <pre>%s</pre>' % (open('/var/www/html/tmp/error_surv.txt').read(),)
else:
	print '<img src="/tmp/distribution.png">'
	print '<img src="/tmp/survival_km.png">'

print "<form method='get'>"

print '''
Alteration: 
<select name='altType'>
<option value='methyl' %s>methyl</option>
<option value='expr' %s>expr-array</option>
<option value='rpkm' %s>expr-RNASeq</option>
<option value='cna' %s>CNA</option>
<option value='pathway' %s>Pathway</option>
</select>''' % \
(('selected' if altType=='methyl' else ''),('selected' if altType=='expr' else ''),('selected' if altType=='rpkm' else ''),('selected' if altType=='cna' else ''),('selected' if altType=='pathway' else ''))

print '''
<br>Gene: <input type='text' name='geneN' size=10 value='%s'>
<br>Cut off: bottom <input type='text' name='cutoff_b' size=2 value='%s'>%%, top <input type='text' name='cutoff_t' size=2 value='%s'>%%
<br><input type='submit' value='Submit'>
</form>''' % (geneN,cutoff_b,cutoff_t)

print '''</html>'''
