#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def loadAnnot(geneL=None):

	refFlatH = mygenome.loadRefFlatByChr()

	eiH = {}
	ei_keyH = {}
	juncInfoH = {}

	for chrom in refFlatH.keys():

		eiH[chrom] = {}
		juncInfoH[chrom] = {}

		refFlatL = refFlatH[chrom]

		for tH in refFlatL:

			if geneL!=None and tH['geneName'] not in geneL:
				continue

			for i in range(len(tH['exnList'])):
				e = tH['exnList'][i][1]
				#eiH[chrom][e] = []
				eiH[chrom][e] = 0
				mybasic.addHash(juncInfoH[chrom], e, '%s:%s:%s/%s' % (tH['geneName'],tH['refSeqId'],i+1,len(tH['exnList'])))

		ei_keyH[chrom] = eiH[chrom].keys()

	return eiH,ei_keyH,juncInfoH


def main(inGsnapFileName,outReportFileName,sampN,geneNL,overlap=10):

	eiH, ei_keyH, juncInfoH = loadAnnot(geneNL)

	print 'Finished loading refFlat'

	result = mygsnap.gsnapFile(inGsnapFileName,False)

	count = 0

	for r in result:

		if r.nLoci != 1:
			continue

		match = r.matchL()[0]

#		if '(transloc)' in r.pairRel or len(match.segL) > 1:
#			continue	

		for seg in match.segL:

#			seg = match.segL[0]
				
			loc = mygenome.locus(seg[2])

			for e in ei_keyH[loc.chrom]:
				
				if loc.chrSta+overlap < e <= loc.chrEnd-overlap:

					#eiH[loc.chrom][e].append(r.seq())
					eiH[loc.chrom][e] += 1

#		count += 1
#
#		if count % 10000 == 0:
#			break

	outReportFile = open(outReportFileName,'w')

	for chrom in ei_keyH.keys():

		for e in ei_keyH[chrom]:

			if eiH[chrom][e]==[]:
				continue

			outReportFile.write('%s\t%s\t%s\t%s\n' % (sampN, '%s:%s' % (chrom,e), ','.join(juncInfoH[chrom][e]), eiH[chrom][e]))
			#outReportFile.write('%s\t%s\t%s\t%s\n' % (sampN, '%s:%s' % (chrom,e), ','.join(juncInfoH[chrom][e]), len(set(eiH[chrom][e]))))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:s:',[])

optH = mybasic.parseParam(optL)

if '-s' in optH:
	sampN = optH['-s']
else:
	sampN = optH['-i']

main(optH['-i'], optH['-o'], sampN, ['EGFR'], 10)
