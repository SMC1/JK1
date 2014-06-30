#!/usr/bin/python

import sys, os, re, getopt, math
import mymysql, mybasic


def main(dbN,outputFileN):

	con,cursor = mymysql.connectDB(db=dbN)

	cursor.execute('SELECT distinct gene_sym FROM rpkm_gene_expr')
	geneL = cursor.fetchall()

	cursor.execute('SELECT distinct samp_id FROM rpkm_gene_expr')
	sIdL = cursor.fetchall()
	sIdL = [x for (x,) in sIdL]
	sIdL.sort()

	dataH = {}

	outputFile = open(outputFileN, 'w')
	
	outputFile.write('#1.2\n')
	outputFile.write('%s\t%s\n' % (len(geneL), len(sIdL)))

	for (geneN,) in geneL:

		cursor.execute('SELECT samp_id,rpkm from rpkm_gene_expr where gene_sym="%s"' % geneN)
		results = cursor.fetchall()

		for (sId,value) in results:
			value = '%.3f' % math.log(value+1,2)

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



optL, argL = getopt.getopt(sys.argv[1:],'d:o:',[])

optH = mybasic.parseParam(optL)

main('tcga1','/EQL1/NSL/RNASeq/results/expression/TCGA_GBM_RPKM_lg2.gct')
#main('ircr1','/EQL1/NSL/RNASeq/results/expression/NSL_GBM_RPKM_lg2.gct')
