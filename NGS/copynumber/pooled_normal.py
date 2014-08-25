#!/usr/bin/python

import os, sys, re
import mysetting
from glob import glob

def make_pooled(dirL, outFileN):
	bamFileH = {}
	dnFileL = []
	dnP = 1.0/len(dirL)
	for dir in dirL:
		bamFileN=glob('%s/*_B_*recal.bam' % dir)[0]
		samp_id = re.match('(.*).recal.bam', os.path.basename(bamFileN)).group(1)
		bamFileH[samp_id] = bamFileN

		newFileN = samp_id + '.DN.bam'
		dnFileL.append(newFileN)
		os.system('java -Xmx8g -jar /home/tools/picard-tools-1.73/DownsampleSam.jar P=%s I=%s O=%s CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT' % (dnP, bamFileN, newFileN))
	os.system('java -Xmx8g -jar /home/tools/picard-tools-1.73/MergeSamFiles.jar %s O=%s SO=coordinate AS=true MSD=true USE_THREADING=true CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT' % (' '.join(map(lambda x: 'I=%s' % x, dnFileL)), outFileN))
	os.system('rm -f *.DN.ba*')

def make_pooled_rpkm(dirL, outFileN):
	rpkmH = {}
	N = len(dirL)
	for dir in dirL:
		refFileN = glob('%s/*.rpkm' % dir)[0]
		inFile = open(refFileN)
		header = inFile.readline().rstrip()
		for line in inFile:
			colL = line.rstrip().split('\t')
			locus = colL[0]
			count = int(colL[1])
			rpkm = float(colL[2])
			total = int(colL[3])
			length = int(colL[4])

			if locus not in rpkmH:
				rpkmH[locus] = {'count':count, 'rpkm':rpkm, 'total':total, 'length':length}
			else:
				rpkmH[locus]['count'] += count
				rpkmH[locus]['rpkm'] += rpkm
				rpkmH[locus]['total'] += total
		#line
	#dir

	inFile = open(glob('%s/*.rpkm' % dirL[0])[0])
	inFile.readline()
	outFile = open(outFileN, 'w')
	outFile.write('"geneName"\t"CS_B_pool(avg raw counts)"\t"CS_B_pool(avg RPKM)"\t"CS_B_pool(avg all reads)"\t"gene length (union of all possible exon\'s length)"\n')
	for line in inFile:
		colL = line.rstrip().split('\t')
		locus = colL[0]
		outFile.write('%s\t%s\t%s\t%s\t%s\n' % (locus, rpkmH[locus]['count']/float(N), rpkmH[locus]['rpkm']/float(N), rpkmH[locus]['total']/float(N), rpkmH[locus]['length']))
	outFile.flush()
	outFile.close()

if __name__ == '__main__':
#	make_pooled(mysetting.poolB_DLink, 'DLink_B_pool.recal.bam')
#	make_pooled(mysetting.poolB_SGI, 'SGI_B_pool.recal.bam')
# 20 hapmap sample for cancerscan
	hm20 = map(lambda x: '/EQL6/pipeline/CS_HAPMAP20/' + x, filter(lambda x: 'html' not in x, os.listdir('/EQL6/pipeline/CS_HAPMAP20')))
#	make_pooled(hm20, 'CS_B_pool.recal.bam')
	make_pooled_rpkm(hm20, 'CS_B_pool.rpkm')

