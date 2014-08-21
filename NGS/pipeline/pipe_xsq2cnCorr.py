#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mymysql
from glob import glob
from mysetting import mysqlH

## SYSTEM CONFIGURATION

from mypipe import storageBase
from mypipe import apacheBase

def main(inputFilePathL, projectN, clean=False, pbs=False, server='smc1'):
	storageBase = os.path.dirname(mypipe.prepare_baseDir(projectN, mkdir=False)) + '/'
	apacheBase = storageBase

	if glob(storageBase+projectN):
		print ('File directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (storageBase,projectN, storageBase,projectN))
		print('File directory: created')
	
	if glob(apacheBase+projectN):
		print ('Log directory: already exists')
	else:
		os.system('mkdir %s/%s; \
			chmod a+w %s/%s' % (apacheBase,projectN, apacheBase,projectN))
		print('Log directory: created')


	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'], passwd=mysqlH[server]['passwd'], db='ircr1', host=mysqlH[server]['host'])
	for inputFileP in inputFilePathL:

		inputFileN = inputFileP.split('/')[-1]
		sampN = re.match('(.*)\.ngCGH', inputFileN).group(1)
		(sid, tag) = re.match('(.*)_([XCT].{0,2})_.*\.ngCGH', inputFileN).groups()
		if tag != 'T':
			sid = '%s_%s' % (sid, tag)

		cursor.execute('SELECT tumor_frac FROM xsq_purity WHERE samp_id="%s"' % (sid))
		results = cursor.fetchall()
		if len(results) > 0 and results[0][0] != 'ND': ##Of samples for which purity was calculated
			if any(sid in x for x in os.listdir('/EQL3/pipeline/CNA_corr')): # only those for which corrected cn were not calculated, yet
				continue
			print sid
			cmd = 'python ~/JK1/NGS/pipeline/pipe_s_xsq2cnCorr.py -i %s -n %s -p %s -c %s -s %s' % (inputFileP, sampN, projectN, False, server)
			print cmd
			if pbs:
				log = '%s/%s.Xsq_cnCorr.qlog' % (storageBase+projectN+'/'+sampN,sampN)
				os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
			else:
				log = '%s/%s.Xsq_cnCorr.qlog' % (storageBase+projectN,sampN)
				os.system('(%s) 2> %s' % (cmd, log))

main(glob('/EQL3/pipeline/CNA/*/*.ngCGH'), projectN='CNA_corr', clean=False, pbs=True, server='smc1')
