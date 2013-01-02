#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def process_bp(inFileName,outFileName,regionL):

	result = mygsnap.gsnapFile(inFileName,True)
	outFile = open(outFileName, 'w')

	outFile.write('browser full knownGene\n')
	outFile.write('track name="%s" visibility=2\n' % inFileName)

	for rL in result:

		if not (rL[0].nLoci==1 and rL[1].nLoci==1 and rL[0].pairRel=='concordant'):
			raise Exception

		locL = [mygenome.locus(rL[0].matchL()[0].segL[0][2]), mygenome.locus(rL[1].matchL()[0].segL[0][2])]

		flag = False

		for loc in locL:
			for region in regionL:
				if loc.overlap(region) > 0:
					flag = True
			
		if flag:

			print '^%s.*%s$\n' % (rL[0].seq(),mybasic.rc(rL[1].seq())),

			for loc in locL:
				outFile.write('%s\t%s\t%s\n' % (loc.chrom,loc.chrSta,loc.chrEnd))


regionL = [('chr7',55040713,55316780)]
#[('chr1',156836213,156836247), ('chr1',156844080,156844321), ('chr1',204951716,204951872), ('chr1',156628715,156628815)]

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	process_bp(optH['-i'], optH['-o'], regionL)
