#!/usr/bin/python
## integration into DB (per sample)

import sys, os
import mymysql, mypipe, mybasic
from mysetting import mysqlH
mybasic.add_module_path(['NGS/expression','Integration'])
import rpkm_process, prepDB_rpkm_gene_expr, boxplot_expr_cs_gene

def post_s_rsq2expr(baseDir, server='smc1', dbN='ihlee_test'):
	sampN = baseDir.split('/')[-1]
	sid = sampN[:-4].replace('-','_').replace('.','_') ##drop '_RSq'

	if dbN in ['ihlee_test','ircr1']:
		gctFileN = '/EQL1/NSL/RNASeq/results/expression/%s.gct' % sampN
		datFileN = '/EQL1/NSL/RNASeq/results/expression/%s.dat' % sampN
	else:
		gctFileN = '%s/%s.gct' % (baseDir, sampN)
		datFileN = '%s/%s.dat' % (baseDir, sampN)
	print sampN, gctFileN
	rpkm_process.rpkm_process(inputDirN=baseDir, filePattern='*.rpkm', sampRegex='(.*)_RSq\.rpkm', outputFileN=gctFileN)
	## prep
	prepDB_rpkm_gene_expr.main(inGctFileName=gctFileN, geneList=[], samplePrefix='', outDatFileName=datFileN)
	## import
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
	cursor.execute('DELETE FROM rpkm_gene_expr WHERE samp_id="%s"' % sid)
	cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE rpkm_gene_expr' % datFileN)
	cursor.execute('DROP VIEW IF EXISTS rpkm_gene_expr_lg2')
	cursor.execute('CREATE VIEW rpkm_gene_expr_lg2 AS SELECT samp_id,gene_sym,log2(rpkm+1) AS lg2_rpkm FROM rpkm_gene_expr')
	## make sure to update sample_tag that this sample has RNA-Seq
	cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
	results = cursor.fetchall()
	if len(results) < 1:
		cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)
	
	##draw boxplot
	boxplot_expr_cs_gene.main(sid, '/EQL1/NSL/RNASeq/results/expression')

def post_rsq2expr(projDirN, server='smc1', dbN='ihlee_test', dbText='test', sampL=[]):
	inDirL = filter(lambda x: os.path.isdir(projDirN+'/'+x), os.listdir(projDirN))
	if dbN != 'ircr1':
		mymysql.create_DB(dbN, dbText, server)
	for inDir in inDirL:
		sampN = inDir.split('/')[-1]
		sid = sampN[:-4].replace('.','_').replace('-','_') ## RNASeq sample has '***_RSq'
		if sampL != [] and sid not in sampL:
			continue
		print sampN, sid
		post_s_rsq2expr(projDirN + '/' + inDir, server=server, dbN=dbN)

if __name__ == '__main__':
#	post_s_rsq2expr('/EQL1/pipeline/SGI20131031_rsq2expr/S023_RSq', server='smc1')
#	post_rsq2expr(projDirN='/EQL3/pipeline/SGI20131226_rsq2expr', server='smc1', dbN='ircr1')
#	post_s_rsq2expr('/EQL3/pipeline/SGI20131226_rsq2expr/S633_RSq', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL2/pipeline/SGI20140204_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL2/pipeline/SGI20140219_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL6/pipeline/SCS20140104_rsq2expr', server='smc1', dbN='IRCR_GBM_352_SCS')
#	post_rsq2expr(projDirN='/EQL6/pipeline/SCS20140203_rsq2expr', server='smc1', dbN='IRCR_GBM_363_SCS')
#	post_rsq2expr(projDirN='/EQL6/pipeline/JKM20140314_bulk_rsq2expr', server='smc1', dbN='RC085_LC195_bulk')
#	post_rsq2expr(projDirN='/EQL6/pipeline/JKM20140314_SCS_RM_rsq2expr', server='smc1', dbN='LC_195_SCS')
#	post_rsq2expr(projDirN='/EQL2/pipeline/SGI20140331_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL6/pipeline/SCS20140422_rsq2expr', server='smc1', dbN='IRCR_GBM_412_SCS', dbText='SCS 412')
#	post_rsq2expr(projDirN='/EQL6/pipeline/SGI20140520_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140520_rsq2expr', server='smc1', dbN='ircr1', sampL=['IRCR_GBM12_190'])
#	post_rsq2expr(projDirN='/EQL3/pipeline/SGI20140526_rsq2expr', server='smc1', dbN='ircr1') ## NCI_GBM_827 only
#	post_rsq2expr(projDirN='/EQL3/pipeline/SGI20140602_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL4/pipeline/SGI20140620_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL4/pipeline/SGI20140702_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL4/pipeline/SGI20140710_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL4/pipeline/SGI20140716_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL4/pipeline/SGI20140723_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140804_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140811_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140818_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140821_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140829_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140904_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140922_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20140930_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141013_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141021_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141027_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141027_rsq2expr', server='smc1', dbN='ircr1', sampL=['IRCR_GBM13_352_T01_C01','IRCR_GBM13_352_T02_C01'])
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141031_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141103_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141117_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141126_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141202_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141203_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141211_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141218_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20141222_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20150102_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20150121_rsq2expr', server='smc1', dbN='ircr1')
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20150121_rsq2expr', server='smc1', dbN='ircr1', sampL=['IRCR_GBM12_165','IRCR_GBM14_427','IRCR_GBM14_596','NS05_188','NS10_809','IRCR_GBM11_112','IRCR_GBM11_117','IRCR_GBM13_225'])
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20150206_rsq2expr', server='smc1', dbN='ircr1', sampL=['IRCR_GBM15_677','IRCR_MBT15_204'])
#	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20150206_rsq2expr', server='smc1', dbN='ircr1')
	post_rsq2expr(projDirN='/EQL8/pipeline/SGI20150306_rsq2expr', server='smc1', dbN='ircr1')
