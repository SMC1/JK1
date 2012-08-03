#!/usr/bin/python

import sys, re

if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
else:
	inFileName = '/Data2/RNASeq_SMC1_S02_result_unpaired_proc.txt'
	outFileName = '/Data2/RNASeq_SMC1_S02_result_unpaired_circos.txt'


outFile = open(outFileName, 'w')
inFile = open(inFileName)

cnt = 1

for line in inFile:

	for y in line.split('\t\t'):

		locL = []

		for loc in y.rstrip().split(','):
			locL.append(re.match('([^;]+):([0-9]+)-([0-9]+)([-+])',loc).groups())

		outFile.write('%s\ths%s\t%s\t%s\n' % (cnt,locL[0][0],locL[0][1],locL[-1][2]))

	cnt += 1

#	if cnt > 1000:
#		break

inFile.close()
