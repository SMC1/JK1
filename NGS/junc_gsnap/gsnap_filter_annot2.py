#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap

# only include matches whose segments correspond to exclusively different genes
# prerequisite filters: transloc
# this filter includes annot1 (more rigorous filtering condition than annot1)

def filter_annot2(inFileName,outFileName):

	result = mygsnap.gsnapFile(inFileName,False)
	outFile = open(outFileName, 'w')

	count_all = 0
	count_include = 0

	for r in result:

		if not '(transloc)' in r.pairRel:
			raise Exception

		match = r.matchL()[0]

		geneSetL = []
		isThereEmptySet = False

		for i in range(len(match.segL)):

			rm = re.search('label_[12]:([^,\t]*)',match.segL[i][3])

			if rm:
				geneSetL.append(set([x.split('.exon')[0] for x in rm.group(1).split('|')]))
			else:
				geneSetL.append(set())
				isThereEmptySet = True

		geneSetCommon = geneSetL[0]

		for s in geneSetL[1:]:
			geneSetCommon = geneSetCommon.intersection(s)

		if len(geneSetCommon) == 0 and isThereEmptySet==False:
			outFile.write(r.rawText()+'\n')
			count_include += 1
		else:
			print r.rawText()

		count_all += 1

	print count_include,count_all

optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:

	filter_annot2(optH['-i'], optH['-o'])
