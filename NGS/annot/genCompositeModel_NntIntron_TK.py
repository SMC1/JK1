#!/usr/bin/python

import sys, copy
import mygenome

# kg, lincRNA
# always "+" strand
# ignore strandedness of transcripts

def genCompositeModel(outTextFileName,outFaFileName,intronSize=100): 

	geneH = mygenome.loadKgByChr()
	geneH = mygenome.loadLincByChr(h=geneH)

	outTextFile = open(outTextFileName, 'w')
	outFaFile = open(outFaFileName, 'w')

	for chrNum in range(1,23)+['X','Y','M']:
	#for chrNum in [1]:

		geneH_byChr = filter(lambda x: x['geneName'] in mygenome.RTK, geneH['chr'+chrNum])

		chrom = 'chr%s' % chrNum

		txnLocusL_combined = []

		for strand in ['+','-']:

			txnLocusL = [mygenome.locus('%s:%s-%s%s' % (chrom,h['txnSta'],h['txnEnd'],strand),h['geneId']) for h in filter(lambda x: x['strand']==strand, geneH_byChr)]
			n_before = len(txnLocusL)

			txnLocusL = mygenome.mergeLoci(txnLocusL)
			n_after = len(txnLocusL)

			#print chrom, strand, n_before, n_after

			txnLocusL_combined += txnLocusL

		txnLocusL_combined.sort(lambda x,y: cmp(x.chrEnd,y.chrEnd))
		txnLocusL_combined.sort(lambda x,y: cmp(x.chrSta,y.chrSta))

		for txnLoc in txnLocusL_combined:

			exnLocusL = []

			for h in filter(lambda x: x['geneId'] in txnLoc.id, geneH_byChr):
				for (exnSta,exnEnd) in h['exnList']:
					exnLocusL.append(mygenome.locus('%s:%s-%s%s' % (chrom, exnSta, exnEnd, h['strand'])))

			exnLocusL.sort(lambda x,y: cmp(x.chrEnd,y.chrEnd))
			exnLocusL.sort(lambda x,y: cmp(x.chrSta,y.chrSta))

			exnLocusL = mygenome.mergeLoci(exnLocusL)

			exnStaL = [str(exnLoc.chrSta) for exnLoc in exnLocusL]
			exnEndL = [str(exnLoc.chrEnd) for exnLoc in exnLocusL]

			outTextFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (txnLoc.id,txnLoc.chrom,txnLoc.strand,txnLoc.chrSta,txnLoc.chrEnd,len(exnLocusL),','.join(exnStaL),','.join(exnEndL)))

			outFaFile.write('>%s|%s|%s|%s|%s\n' % (txnLoc.id,txnLoc.chrom,txnLoc.strand,txnLoc.chrSta,txnLoc.chrEnd))

			for i in range(len(exnLocusL)):

				exnLocCopy = copy.deepcopy(exnLocusL[i])

				exnLocCopy.strand = '+'

				if i > 0:
					exnLocCopy.chrSta -= min(intronSize, int((exnLocusL[i].chrSta - exnLocusL[i-1].chrEnd)/2))

				if i < len(exnLocusL)-1:
					exnLocCopy.chrEnd += min(intronSize, int((exnLocusL[i+1].chrSta - exnLocusL[i].chrEnd)/2))

				outFaFile.write(exnLocCopy.nibFrag())

			outFaFile.write('\n')

	outTextFile.close()
	outFaFile.close()

genCompositeModel('/data1/Sequence/compositeModel_hg19/RTK_50Int.txt','/data1/Sequence/compositeModel_hg19/RTK_50Int.fa',50)
