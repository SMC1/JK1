#!/usr/bin/python

import sys, getopt, re, glob
import mybasic

def main(inFileDir,outFileName,geneNL=[]):

	outFile = open(outFileName,'w')

	registry = []

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

		for line in inFile:

			name,value = line.rstrip().split('\t')
			geneN = name[:name.find('_')]
			loc = name[name.find('_')+1:]

			if value=='N/A':
				continue

			for g in geneN.split(';'):
				if geneNL==[] or g in geneNL:
					outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (platform,sId,pId,TN,g,loc,value))

	inFileNameL = glob.glob('%s/*HumanMethylation*' % (inFileDir,))
	inFileNameL.sort(lambda x,y: cmp(x,y))

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

		for line in inFile:

			tokL = line.rstrip().split('\t')

			geneN = tokL[3]
			loc = '%s:%s' % tuple(tokL[4:6])
			value = tokL[2]

			if value=='NA':
				continue

			for g in geneN.split(';'):
				if geneNL==[] or g in geneNL:
					outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (platform,sId,pId,TN,g,loc,value))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/TCGA/GBM/methyl','/EQL1/TCGA/GBM/methyl/methyl_loc_MGMT.dat',['MGMT'])
