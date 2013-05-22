#!/usr/bin/python

import sys, getopt
import mybasic

def main(inFileName, inSnpFileName, outFileName):

	nameL = ('chrom','position','tumor_reads1','tumor_reads2','normal_reads1','normal_reads2')
	
	inSnpFile = open(inSnpFileName)
	
	headerL = inSnpFile.readline()[:-1].split('\t')
	
	idxH = dict([(x, headerL.index(x)) for x in nameL])

	dataH = {}
	
	for line in inSnpFile:

		valueL = line[:-1].split('\t')

		chrN = valueL[idxH['chrom']]
		pos = valueL[idxH['position']]

		key = (chrN,pos)

		n_ref_count = valueL[idxH['normal_reads1']]
		n_alt_count = valueL[idxH['normal_reads2']]

		t_ref_count = valueL[idxH['tumor_reads1']]
		t_alt_count = valueL[idxH['tumor_reads2']]

		dataH[key] = (n_ref_count,n_alt_count, t_ref_count,t_alt_count)

	inFile = open(inFileName)

	outFile = open(outFileName,'w')

	h = inFile.readline()
	header = inFile.readline()

	outFile.write('%s%s\tn_ref_count\tn_alt_count\tt_ref_count\tt_alt_count\n' % (h,header[:-1]))

	for line in inFile:

		dataL = line[:-1].split('\t')

		chr = dataL[4]
		chr = 'chr%s' % dataL[4]
		start = dataL[5]

		count = dataH[(chr,start)]

		outFile.write('%s\t%s\t%s\t%s\t%s\n' % (line[:-1],count[0],count[1],count[2],count[3]))

#		if somatic != 'Somatic':
#			continue
#
#		obsL = obs.split('/')
#		
#		for i in range(len(obsL)):
#			outFile.write('%s\t%s\t%s\t%s\t%s\n' % (chr,start,end,ref,obsL[i]))

optL, argL = getopt.getopt(sys.argv[1:],'i:s:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-s' in optH and '-o' in optH:
	main(optH['-i'],optH['-s'],optH['-o'])
