#!/usr/bin/python

import sys, os, re, getopt
import mymysql, mybasic


def main(outputFileN):

	con,cursor = mymysql.connectDB(db='ircr1')

	cursor.execute('SELECT distinct gene_sym FROM rpkm_gene_expr_lg2')
	geneL = cursor.fetchall()

	cursor.execute('SELECT distinct samp_id FROM rpkm_gene_expr_lg2')
	sIdL = cursor.fetchall()
	sIdL = [x for (x,) in sIdL]
	sIdL.sort()

	dataH = {}

	outputFile = open(outputFileN, 'w')
	
	outputFile.write('#1.2\n')
	outputFile.write('%s\t%s\n' % (len(geneL), len(sIdL)))

	for (geneN,) in geneL:

		cursor.execute('SELECT samp_id,lg2_rpkm from rpkm_gene_expr_lg2 where gene_sym="%s"' % geneN)
		results = cursor.fetchall()

		for (sId,value) in results:
			value = '%.4f' % value

			try:
				dataH[geneN].update({sId: value})
			except:
				dataH[geneN] = {sId: value}

	outputFile.write('NAME\tDescription\t%s\n' % '\t'.join(sIdL))

	geneNL = dataH.keys()
	geneNL.sort()

	for geneN in geneNL:

		outputFile.write('%s\t' % geneN)

		for sId in sIdL:
			outputFile.write('\t%s' % dataH[geneN][sId])
		outputFile.write('\n')



optL, argL = getopt.getopt(sys.argv[1:],'i:o:e:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/RNASeq/results/expression/NSL_GBM_RPKM_118_lg2.gct')
