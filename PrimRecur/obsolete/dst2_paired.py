#!/usr/bin/python

import sys
import mymysql

dTypeH = {'CNA':('array_cn','value_log2'), 'Expr':('array_gene_expr','z_score')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(geneN,dType,dbN='ircr1',outFileDir=None):

	if outFileDir:
		outFile = open('%s/%s_%s_%s_paired.dst2' % (outFileDir,geneN,dType,dbH[dbN]),'w')
	else:
		outFile = sys.stdout

	(con,cursor) = mymysql.connectDB(db=dbN)

	cursor.execute('select distinct samp_id from sample_tag where substring(tag,1,6)="pair_R"')
	sIdL_prim = [x for (x,) in cursor.fetchall()]

	vL = []; sIdL_pair = []

	for sId_p in sIdL_prim:

		cursor.execute('select samp_id from sample_tag where tag="pair_P:%s"' % sId_p)
		(sId_r,) = cursor.fetchone()

		cursor.execute('select %s from %s where gene_sym="%s" and samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],geneN,sId_p))
		r_p = cursor.fetchone()

		cursor.execute('select %s from %s where gene_sym="%s" and samp_id="%s"' % (dTypeH[dType][1],dTypeH[dType][0],geneN,sId_r))
		r_r = cursor.fetchone()

		if r_p and r_r:
			vL.append("%.2f" % (r_r[0]-r_p[0],))
			sIdL_pair.append((sId_p,sId_r))

	outFile.write('%s-%s-%s\t%s\n' % (geneN,dType,dbN,len(sIdL_pair)))
	outFile.write(','.join(vL)+'\n')
	outFile.write(','.join(['%s_%s' % (x,y) for (x,y) in sIdL_pair])+'\n')

	con.close()

for geneN in ['EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4']+['CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI']:
	for dType in ['Expr','CNA']:
		main(geneN,dType,'ircr1','/EQL1/NSL/PrimRecur/paired')
