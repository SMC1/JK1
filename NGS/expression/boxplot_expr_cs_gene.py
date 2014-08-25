#!/usr/bin/python

import os, sys, re
import mymysql, mysetting

def main(samp_id, outDir):
	(con, cursor) = mymysql.connectDB()
	cursor.execute('SELECT * FROM rpkm_gene_expr WHERE (samp_id LIKE "S%%" OR samp_id LIKE "%%GBM%%" OR samp_id = "%s") AND gene_sym IN (SELECT * FROM common.cs_gene)' % samp_id )

	result = cursor.fetchall()
	tmpOut = '%s/tmp_%s' % (outDir, samp_id)
	tmp = open(tmpOut, 'w')
	for res in result:
		(sid, gene_sym, rpkm) = res
		tmp.write('%s\t%s\t%s\n' % (sid, gene_sym, rpkm))
	tmp.flush()
	tmp.close()

	for fmt in ['pdf','png']:
		outN = '%s/%s_CS_expr.%s' % (outDir, samp_id, fmt)
		cmd = 'Rscript %s/NGS/expression/boxplot_expr_cs_gene.R %s %s %s' % (mysetting.SRC_HOME, tmpOut, samp_id, outN)
		os.system(cmd)
	os.system('rm -f %s' % tmpOut)

if __name__ == '__main__':
#	for sid in ['IRCR_GBM14_446','IRCR_GBM14_445','IRCR_GBM14_458','IRCR_GBM14_459_T01','IRCR_GBM14_366']:
	for sid in ['IRCR_GBM14_431','IRCR_LC14_320']:
		main(sid, '/EQL1/NSL/RNASeq/results/expression')
