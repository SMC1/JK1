#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome
import bisect


def loadAnnot(geneL=[]):

	refFlatH = mygenome.loadRefFlatByChr()

	eiH = {}
	ei_keyH = {}
	juncInfoH = {}

	for chrom in refFlatH.keys():

		eiH[chrom] = {}
		juncInfoH[chrom] = {}

		refFlatL = refFlatH[chrom]

		for tH in refFlatL:

			if geneL!=[] and tH['geneName'] not in geneL:
				continue

			for i in range(len(tH['exnList'])):

				if tH['strand'] == '+':
					pos = tH['exnList'][i][1]
					e_num = i+1
				else:
					pos = tH['exnList'][i][0]
					e_num = len(tH['exnList'])-i

				mybasic.addHash(juncInfoH[chrom], pos, '%s%s:%s:%s/%s' % (tH['strand'], tH['geneName'], tH['refSeqId'], e_num, len(tH['exnList'])))
				eiH[chrom][pos] = 0

		ei_keyH[chrom] = eiH[chrom].keys()
		ei_keyH[chrom].sort()

	ei_cntH = {}
	for chrom in juncInfoH.keys():
		ei_cntH[chrom] = {}
		i = 0
		for pos in sorted(juncInfoH[chrom].keys()):
			i += 1
			ei_cntH[chrom][pos] = i

	return eiH,ei_keyH,juncInfoH,ei_cntH

def find_le(a, x):
	## find rightmost value less than or equal to x in sorted array a
	i = bisect.bisect_right(a, x)
	if i:
		return a[i-1]
	else:
		return -1

def findCut(cntH, keyH, pos):
	val = find_le(keyH, pos)
	if val < 0:
		return 0
	else:
		return cntH[val]

def main(inGsnapFileName,outReportFileName,sampN,geneNL=[],overlap=10):

	eiH, ei_keyH, juncInfoH, ei_cntH = loadAnnot(geneNL)

	print 'Finished loading refFlat'

	result = mygsnap.gsnapFile(inGsnapFileName,False)

	count = 0

	for r in result:

		if r.nLoci != 1:
			continue

		match = r.matchL()[0]

		for seg in match.segL:

			loc = mygenome.locus(seg[2])

			if loc.chrSta + overlap > loc.chrEnd - overlap:
				continue

			cnt_s = findCut(ei_cntH[loc.chrom], ei_keyH[loc.chrom], loc.chrSta + overlap - 1)
			cnt_e = findCut(ei_cntH[loc.chrom], ei_keyH[loc.chrom], loc.chrEnd - overlap)
			if cnt_e < 1: ## no junction overlaps
				continue
			elif cnt_s != cnt_e: # overlapping junction exists
				pos_min = bisect.bisect_right(ei_keyH[loc.chrom], loc.chrSta + overlap - 1) - 1
				pos_max = bisect.bisect_right(ei_keyH[loc.chrom], loc.chrEnd - overlap)
				for pos in range(pos_min, pos_max):
					if loc.chrSta+overlap <= ei_keyH[loc.chrom][pos] <= loc.chrEnd-overlap:
						eiH[loc.chrom][ei_keyH[loc.chrom][pos]] += 1

#		count += 1
#
#		if count % 10000 == 0:
#			print count

	outReportFile = open(outReportFileName,'w')

	for chrom in ei_keyH.keys():

		for e in ei_keyH[chrom]:

			if eiH[chrom][e]==[]:
				continue

			outReportFile.write('%s\t%s\t%s\t%s\n' % (sampN, '%s:%s' % (chrom,e), ','.join(juncInfoH[chrom][e]), eiH[chrom][e]))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:s:',[])

optH = mybasic.parseParam(optL)

if '-s' in optH:
	sampN = optH['-s']
else:
	sampN = optH['-i']

#main(optH['-i'], optH['-o'], sampN, ['EGFR'], 10)
#main(optH['-i'], optH['-o'], sampN, ['MET', 'PDGFRA', 'RET', 'EGFR', 'EPHA1', 'EPHA2', 'EPHA3', 'EPHA4', 'EPHA5', 'EPHA6', 'EPHA7', 'EPHA8', 'EPHA10', 'FGFR1', 'FGFR2', 'FGFR3', 'FGFR4', 'FLT1', 'FLT3', 'FLT4'], 10)
main(optH['-i'], optH['-o'], sampN, [], 10)
