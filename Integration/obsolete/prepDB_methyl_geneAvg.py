#!/usr/bin/python

import sys, getopt, re, glob, numpy
import mybasic

def main(inFileDir,outFileName):

	outFile = open(outFileName,'w')

	registry = []

	inFileNameL = glob.glob('%s/*HumanMethylation*' % (inFileDir,))
	inFileNameL.sort(lambda x,y: cmp(y,x))

	for inFileName in inFileNameL:

		sId = inFileName[inFileName.index('TCGA-'):inFileName.index('TCGA-')+28]

		if sId in registry:
			continue

		registry.append(sId)
	
		pId = sId[:12]

		if int(sId[13:15])<10:
			TN = 'T'
		else:
			TN = 'N'

		if 'HumanMethylation450' in inFileName:
			platform = 'Infinium450k'
		else:
			platform = 'Infinium27k'

		print sId, platform

		inFile = open(inFileName)
		line = inFile.readline()

		inFile.readline()

		geneH = {}

		for line in inFile:

			tokL = line.rstrip().split('\t')

			geneN = tokL[3]
			value = tokL[2]

			if not geneN or value=='NA':
				continue

			mybasic.addHash(geneH,geneN,float(value))

		for geneN,valueL in geneH.iteritems():

			v = numpy.mean(valueL)

			for g in geneN.split(';'):
				outFile.write('%s\t%s\t%s\t%s\t%s\t%.2f\n' % (platform,sId,pId,TN,g,v))

	inFileNameL = glob.glob('%s/*OMA002*' % (inFileDir,))
	platform = 'GoldenGate3k'

	for inFileName in inFileNameL:

		inFile = open(inFileName)
		line = inFile.readline()

		sId = line.rstrip().split('\t')[1]

		if sId in registry:
			continue

		registry.append(sId)

		pId = sId[:12]

		if int(sId[13:15])<10:
			TN = 'T'
		else:
			TN = 'N'

		inFile.readline()

		print sId, platform

		geneH = {}

		for line in inFile:

			name,value = line.rstrip().split('\t')
			geneN = name[:name.find('_')]
			loc = name[name.find('_')+1:]

			if not geneN or value=='N/A':
				continue

			mybasic.addHash(geneH,geneN,float(value))

		for geneN,valueL in geneH.iteritems():

			for g in geneN.split(';'):
				outFile.write('%s\t%s\t%s\t%s\t%s\t%.2f\n' % (platform,sId,pId,TN,g,v))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/TCGA/GBM/methyl','/EQL1/TCGA/GBM/methyl/methyl.dat')
