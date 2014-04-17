#!/usr/bin/python

import sys, os, getopt, re
import mybasic

def main(inSegFileName, inMutFileName, outFileName, tFrac):

	inFile = open(inMutFileName)
	inFile.readline()

	header = inFile.readline()[:-1].split('\t')

	chrIdx = header.index('contig')
	posIdx = header.index('position')
	al_ref_idx = header.index('ref_allele')
	al_alt_idx = header.index('alt_allele')
	refIdx = header.index('t_ref_count')
	altIdx = header.index('t_alt_count')
	judgeIdx = header.index('judgement')

	inSegFileMem = [line[:-1].split('\t') for line in open(inSegFileName) if line[:-1].split('\t')[0] != 'ID']
	
	outFile = open(outFileName, 'w')

	for line in inFile:
		
		mutL = line[:-1].split('\t')

		chr = mutL[chrIdx]
		pos = mutL[posIdx]
		al_ref = mutL[al_ref_idx]
		al_alt = mutL[al_alt_idx]
		ref = mutL[refIdx]
		alt = mutL[altIdx]

		r = alt
		tot = int(ref)+int(alt)

		t_cn = None

		for (id, chrom, loc_start, loc_end, num_mark, seg_mean) in inSegFileMem:

			if chrom != chr:
				continue

			if int(loc_start) <= int(pos) <= int(loc_end):
				t_cn = (2**float(seg_mean)) *2

		try:
			f = (float(r)/float(tot)) * (t_cn/(float(tFrac)/100))
			f = min(1,round(f,3))
		except:
			f = 'ND'

		outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (chr, pos, al_ref, al_alt, ref, alt, mutL[judgeIdx], t_cn, f))
	outFile.flush()
	outFile.close()

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:], 's:i:o:p:')

	optH = mybasic.parseParam(optL)

	main(optH['-s'],optH['-i'],optH['-o'],optH['-p'])

