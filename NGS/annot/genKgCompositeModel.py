#!/usr/bin/python

import sys, copy
import mygenome


def genKgCompositeModel(outTextFileName,outFaFileName):

	kgH = mygenome.loadKgByChr()

	outTextFile = open(outTextFileName, 'w')
	outFaFile = open(outFaFileName, 'w')

	for chrNum in range(1,23)+['X','Y','M']:
	#for chrNum in [1]:

		chrom = 'chr%s' % chrNum

		txnLocusL_combined = []

		for strand in ['+','-']:

			txnLocusL = [mygenome.locus('%s:%s-%s%s' % (chrom,h['txnSta'],h['txnEnd'],strand),h['kgId']) for h in filter(lambda x: x['strand']==strand, kgH[chrom])]
			n_before = len(txnLocusL)

			txnLocusL = mygenome.mergeLoci(txnLocusL)
			n_after = len(txnLocusL)

			#print chrom, strand, n_before, n_after

			txnLocusL_combined += txnLocusL

		txnLocusL_combined.sort(lambda x,y: cmp(x.chrEnd,y.chrEnd))
		txnLocusL_combined.sort(lambda x,y: cmp(x.chrSta,y.chrSta))

		for txnLoc in txnLocusL_combined:

			exnLocusL = []

			for h in filter(lambda x: x['kgId'] in txnLoc.id, kgH[chrom]):
				for (exnSta,exnEnd) in h['exnList']:
					exnLocusL.append(mygenome.locus('%s:%s-%s%s' % (chrom, exnSta, exnEnd, h['strand'])))

			exnLocusL.sort(lambda x,y: cmp(x.chrEnd,y.chrEnd))
			exnLocusL.sort(lambda x,y: cmp(x.chrSta,y.chrSta))

			exnLocusL = mygenome.mergeLoci(exnLocusL)

			exnStaL = [str(exnLoc.chrSta) for exnLoc in exnLocusL]
			exnEndL = [str(exnLoc.chrEnd) for exnLoc in exnLocusL]

			outTextFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (txnLoc.id,txnLoc.chrom,txnLoc.strand,txnLoc.chrSta,txnLoc.chrEnd,len(exnLocusL),','.join(exnStaL),','.join(exnEndL)))

			outFaFile.write('>%s|%s|%s|%s|%s\n' % (txnLoc.id,txnLoc.chrom,txnLoc.strand,txnLoc.chrSta,txnLoc.chrEnd))

#			for exnLoc in exnLocusL:
#				outFaFile.write(exnLoc.nibFrag())

			txnLocCopy = copy.deepcopy(txnLoc) # print whole txn sequence in positive strand
			txnLocCopy.strand = '+'

			outFaFile.write(txnLocCopy.nibFrag())

			outFaFile.write('\n')

	outTextFile.close()
	outFaFile.close()

genKgCompositeModel('/data1/Sequence/FusionSeq_Data_hg19/knownGeneAnnotationTranscriptCompositeModel.txt','/data1/Sequence/FusionSeq_Data_hg19/knownGeneAnnotationTranscriptCompositeModel.fa')
