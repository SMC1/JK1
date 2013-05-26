#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inFileName,outFileName,pileupDir):

	inFile = open(inFileName)
	outFile = open(outFileName,'w')

	outFile.write(inFile.readline())

	for line in inFile:

		tokL = line[:-1].split('\t')

		if tokL[-1]==tokL[-2]=='0':
			flag = 0 # Recur
		elif tokL[-3]==tokL[-4]=='0':
			flag = 1 # Prim
		else:
			outFile.write(line)
			continue
			
		rm = re.match('(chr[^:]*):([0-9]*)~([0-9]*)',tokL[2])
		(chrom,chrSta,chrEnd) = rm.groups()

		if int(chrEnd)-int(chrEnd)!=0:
			outFile.write(line)
			continue

		refAllele = tokL[3]
		altAllele = tokL[4]

		#print tokL[1], tokL[2], refAllele, '>', altAllele, tokL[-4:],

		sId = tokL[1].split('-')[1-flag]

		inputFileNL = os.listdir(pileupDir)
		inputFileNL = filter(lambda x: re.match('%s_T_.*_%s\.pileup_proc' % (sId,chrom), x),inputFileNL)

		if len(inputFileNL) > 1:
			inputFileNL = filter(lambda x: not re.match('.*KN.*', x),inputFileNL)

		if len(inputFileNL) != 1:
			print 'Error:', inputFileNL
			raise Exception

		resultL = os.popen('grep -m 1 "^%s:%s," %s/%s' % (chrom,chrSta,pileupDir,inputFileNL[0]), 'r').readlines()

		if len(resultL)==0:
			outFile.write(line)
			continue
		else:
			tL = resultL[0].rstrip().split(',')
			if refAllele != tL[2]:
				sys.exit(1)
			refCount = tL[3]
			altCount = str(tL[4].count(altAllele))
			tokL[-1-flag*2] = refCount
			tokL[-2-flag*2] = altCount
			outFile.write('\t'.join(tokL)+'\n')

		#print tokL[-4:]

	outFile.close()


#optL, argL = getopt.getopt(sys.argv[1:],'i:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH and '-l' in optH:
#
#	main(optH['-i'], optH['-o'], int(optH['-l']))

main('/EQL1/PrimRecur/signif/signif_mutation_pre.txt','/EQL1/PrimRecur/signif/signif_mutation.txt','/EQL1/NSL/exome_bam/mutation/pileup_proc')
