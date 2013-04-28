#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN):
	
	sampNameS = set([re.match('.*/(.*).qlog:Normal*',line).group(1).replace('.snp','') for line in os.popen('grep -H "Normal Pileup" %s/*.qlog' % inputDirN)])

	sampNL = list(sampNameS)
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['NS09_671T']:
#			continue

		print sampN

		os.system('python /home/heejin/JK1/NGS/mutation/snp2oncotator.py -i %s/%s.snp -o %s/%s.oncotator' % \
				(inputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/mutation')
