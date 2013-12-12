#!/usr/bin/python

import sys, getopt, re, os
import mybasic

def main(inDirName, outDirName):

	inFileNL = os.listdir(inDirName)
	inFileNL = filter(lambda x: re.match('hudsonalpha.*.Paired_LogR.txt', x), inFileNL)

	for inFileName in inFileNL:

		print inFileName

		inFile = open(inDirName+'/'+inFileName)

		header = inFile.readline()[:-1].split('\t')
		inFile.readline()

		sIdL = header[3:]
		tIdxL = []

		for i in range(len(sIdL)):

			sId = sIdL[i]
			
			if int(sId[13:15]) < 10:
				tIdxL.append(i)

		for	i in tIdxL:

			print sIdL[i]

			outFileName = '%s.%s' % (sIdL[i],inFileName)
			outFile = open(outDirName+'/'+outFileName,'w')
			outFile.write('probe\tchrs\tpos\t%s\n' % sIdL[i])

			inFile = open(inDirName+'/'+inFileName)
			inFile.readline()
			inFile.readline()
			
			for line in inFile:

				dataL = line[:-1].split('\t')

				id = dataL[0]
				chrs = dataL[1]
				pos = dataL[2]

				valL = dataL[3:]
				val = valL[i]

				outFile.write('%s\t%s\t%s\t%s\n' % (id,chrs,pos,val))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	main(optH['-i'],optH['-o'])

main('/EQL1/TCGA/GBM/array_cn/CNV_SNP_Array/HAIB__HumanHap550/Level_2','/EQL1/TCGA/GBM/array_cn/CNV_SNP_Array/HAIB__HumanHap550/Level_2')
