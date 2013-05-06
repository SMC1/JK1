#!/usr/bin/python

import sys
import mymysql

dTypeH = {'CNA':('array_cn','value_log2'), 'Expr':('array_gene_expr','z_score')}
dbH = {'tcga1':'TCGA-GBM', 'ircr1':'IRCR-GBM'}

def main(geneN,dType,dbN,outFileDir=None,pairedOnly=False):

	if outFileDir:
		if pairedOnly and dbN=='ircr1':
			outFile = open('%s/%s_%s_%s_paired.dst2' % (outFileDir,geneN,dType,dbH[dbN]),'w')
		else:
			outFile = open('%s/%s_%s_%s.dst2' % (outFileDir,geneN,dType,dbH[dbN]),'w')
	else:
		outFile = sys.stdout

	(con,cursor) = mymysql.connectDB(db=dbN)

	if dbN == 'ircr1':
		cursor.execute('create temporary table t_paired_prim select distinct samp_id from sample_tag where substring(tag,1,6)="pair_R"')
		cursor.execute('create temporary table t_recur select distinct samp_id from sample_tag where substring(tag,1,6)="pair_P"')
	elif dbN == 'tcga1':
		cursor.execute('create temporary table t_recur select distinct samp_id from sample_tag where tag="Recur"')
	else:
		raise Exception

	if pairedOnly and dbN=='ircr1':
		cursor.execute('select %s from %s where gene_sym="%s" and samp_id in (select samp_id from t_paired_prim)' % (dTypeH[dType][1],dTypeH[dType][0],geneN))
	else:
		cursor.execute('select %s from %s where gene_sym="%s" and samp_id not in (select samp_id from t_recur)' % (dTypeH[dType][1],dTypeH[dType][0],geneN))

	prim = [str(x) for (x,) in cursor.fetchall()]

	cursor.execute('select %s from %s where gene_sym="%s" and samp_id in (select samp_id from t_recur)' % (dTypeH[dType][1],dTypeH[dType][0],geneN))
	recur = [str(x) for (x,) in cursor.fetchall()]

	outFile.write('%s-%s-%s-Prim\t%s\n' % (geneN,dType,dbN,len(prim)))
	outFile.write(','.join(prim)+'\n')
	outFile.write('\n')

	outFile.write('%s-%s-%s-Recur\t%s\n' % (geneN,dType,dbN,len(recur)))
	outFile.write(','.join(recur)+'\n')
	outFile.write('\n')

	con.close()

for geneN in ['EGFR','CDK4','CDK6','PDGFRA','MET','MDM2','MDM4']+['CDKN2A','CDKN2B','CDKN2C','PTEN','RB1','NF1','QKI']:
	for dType in ['Expr','CNA']:
		for dbN in ['tcga1','ircr1']:
			main(geneN,dType,dbN,'/EQL1/NSL/PrimRecur/unpaired')
