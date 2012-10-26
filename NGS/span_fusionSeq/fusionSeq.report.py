#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: fusionSeq.report.py -i (input file dir)'
	sys.exit(0)

inputDirN = optH['-i']

resultF = os.popen('tail -q -n +2 %s/*confidence* | cut -f1,6-9,12-16,19-22,24,28-34' % inputDirN)

print 'fusionType\tgeneName1\tgeneName2\ttranscript1\ttranscript2\tgeneDesc1\tgeneDesc2\tgeneLoc1\tgeneLoc2\tsampleName\tinterReads\tintraReads1\tintraReads2\tSPER\tDASPER\tRESPER'

for line in resultF:

	(interReads,intraReads1,intraReads2,fusionType,transcript1,chrom1,strand1,chrSta1,chrEnd1,transcript2, chrom2,strand2,chrSta2,chrEnd2,sampName,geneName1,geneName2,geneDesc1,geneDesc2,sper,dasper,resper) = \
		line[:-1].split('\t')

	if float(resper) > 1:
		print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (fusionType,geneName1,geneName2,transcript1,transcript2,geneDesc1,geneDesc2, \
			'%s%s:%s-%s' % (strand1,chrom1,chrSta1,chrEnd1),'%s%s:%s-%s' % (strand2,chrom2,chrSta2,chrEnd2), sampName.split('_30nt')[0], interReads,intraReads1,intraReads2,sper,dasper,resper)
