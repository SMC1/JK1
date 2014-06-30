#!/usr/bin/python

import sys
import mymysql

dTypeH = {'CNA':('array_cn','value_log2'), 'Expr':('array_gene_expr_ori','value'), 'RPKM':('rpkm_gene_expr','log2(rpkm+1)')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(inFileName,outFileName):

	(con,cursor) = mymysql.connectDB(db='ircr1')

	inFile = open(inFileName)
	inFile.readline()

	outFile = open(outFileName,'w')
	outFile.write('\t'.join(('dType','geneN','sId_p','sId_r','val_p','val_r','chemo','RT','either'))+'\n')

	for line in inFile:

		(sId_p,chemo,RT) = line[:-1].split('\t')

		if chemo=='NA':
			chemo = 1000
		else:
			chemo = min(int(chemo),1000)

		if RT=='NA':
			RT = 1000
		else:
			RT = min(int(RT),1000)

		for geneN in geneL:

			for dType in dTypeL:

				cursor.execute('select samp_id from sample_tag where tag="pair_P:%s"' % sId_p)
				(sId_r,) = cursor.fetchone()

				cursor.execute('select %s from %s where gene_sym="%s" and samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],geneN,sId_p))
				r_p = cursor.fetchone()

				cursor.execute('select %s from %s where gene_sym="%s" and samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],geneN,sId_r))
				r_r = cursor.fetchone()

				if r_p and r_r:
					outFile.write('%s\t%s\t%s\t%s\t%.2f\t%.2f\t%d\t%d\t%d\n' % (dType,geneN,sId_p,sId_r,r_p[0],r_r[0],chemo,RT,min(chemo,RT)))

	inFile.close()
	outFile.close()
	con.close()

geneL = ['EGFR','CDK4','PDGFRA','MDM2','MDM4','MET','CDK6']+['CDKN2A','CDKN2B','PTEN','CDKN2C','RB1','QKI','NF1']
dTypeL = ['Expr','CNA','RPKM']

main('/EQL1/PrimRecur/paired/time_to_latest_tx.txt','/EQL1/PrimRecur/paired/df_paired_tx.txt')
