#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap

# exclude matches that contain a same gene for all split ends

def filter_annot(inFileName,outFileName):

	result = mygsnap.gsnapFile(inFileName,False)
	outFile = open(outFileName, 'w')

	count_all = 0
	count_include = 0

	for r in result:

		if not '(transloc)' in r.pairRel:
			raise Exception

		match = r.matchL()[0]

		for i in range(len(match.segL)):

			rm = re.match('.*label_[0-9]:([^,\t]*).*',seg[3])

			if rm:
				geneSet.intersection(set([x.split('.exon')[0] for x in rm.group(1).split('|')]))
			else:
				geneSet = set()

			if i == 0:
				commonGeneSet = geneSet
			else:
				commonGeneSet = commonGeneSet.intersection(geneSet)

			if len(commonGeneSet) == 0:
				outFile.write(r.rawText()+'\n')
				count_include += 1
			else:
				print r.rawText()

		count_all += 1

	print count_include,count_all

optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	filter_annot(optH['-i'], optH['-o'])
