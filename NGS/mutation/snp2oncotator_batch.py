#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting


def main(inputDirN, outputDirN, format):
	
	sampNameS = set([re.match('.*/(.*).qlog:Normal*',line).group(1).replace('.snp','') for line in os.popen('grep -H "Normal Pileup" %s/*.qlog' % inputDirN)])

	sampNL = list(sampNameS)
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		if sampN not in ['S050_T_SS','S532_T_SS','S602_T_SS']:
			continue

		print sampN

		if format == 'oncotator':
			os.system('/usr/bin/python %s/NGS/mutation/snp2oncotator.py -i %s/%s.snp -o %s/%s_oncotator.txt' % \
					(mysetting.SRC_HOME, inputDirN,sampN, outputDirN,sampN))

		if format == 'cravat':
			os.system('/usr/bin/python %s/NGS/mutation/snp2cravat.py -i %s/%s.snp -s %s -o %s/%s_cravat.txt' % \
					(mysetting.SRC_HOME, inputDirN,sampN, sampN, outputDirN,sampN))

		if format == 'sift':
			os.system('/usr/bin/python %s/NGS/mutation/snp2sift.py -i %s/%s.snp -o %s/%s_sift.txt' % \
					(mysetting.SRC_HOME, inputDirN,sampN, outputDirN,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:f:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/mutation/cravat','cravat')
