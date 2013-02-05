#!/usr/bin/python

import sys
import mygsnap



if len(sys.argv) >= 3:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
else:
	inFileName = '/Data2/RNASeq_SMC1_S02_result.txt'
	outFileName = '/Data2/RNASeq_SMC1_S02_result.bed'

matchCutOff = 90
chrom = 'chr21'

dataL = []

result = mygsnap.gsnapFile(inFileName)

for rL in result:

	for i in (0,1):

		if rL[i].nLoci!=1 or '(transloc)' in rL[i].pairRel:
			continue

		mergedLocusL = rL[i].matchL()[0].mergedLocusL()

		if len(mergedLocusL)!=1:
			continue

		l = mergedLocusL[0]
		nMatch = rL[i].matchL()[0].numMatch(rL[i].seq())

		if nMatch>=matchCutOff or (rL[i].pairRel=='concordant' and nMatch>=matchCutOff-10):

			if chrom=='' or l.chrom==chrom:
				dataL.append((l.chrom,l.chrSta,l.chrEnd,nMatch,l.strand))

dataL.sort(lambda x,y: cmp(x[1],y[1]))

outFile = open(outFileName, 'w')

outFile.write('browser position chr21:9827449-9827550\n')
outFile.write('track name="chr21" description="SMC2_02" color=0,128,0 visibility=4\n')

for i in range(len(dataL)):
	outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (dataL[i][:3]+(i+1,)+dataL[i][3:]))

outFile.close()
