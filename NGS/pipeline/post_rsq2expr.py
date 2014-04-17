#!/usr/bin/python
## integration into DB (per sample)

import sys, os
import mymysql
from mysetting import mysqlH

moduleL = ['NGS/expression', 'Integration'] ## DIRECTORY
homeDir = os.popen('echo $HOME','r').read().rstrip()

for module in moduleL:
	sys.path.append('%s/JK1/%s' % (homeDir,module))

import rpkm_process, prepDB_rpkm_gene_expr

def post_s_rsq2expr(baseDir, server='smc1', dbN='ihlee_test'):
	sampN = baseDir.split('/')[-1]
	sid = sampN[:-4]

	gctFileN = '/EQL1/NSL/RNASeq/results/expression/%s.gct' % sampN
	datFileN = '/EQL1/NSL/RNASeq/results/expression/%s.dat' % sampN
	print sampN, gctFileN
	rpkm_process.rpkm_process(inputDirN=baseDir, filePattern='*.rpkm', sampRegex='S(.*)_RSq\.rpkm', outputFileN=gctFileN)
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

def post_rsq2expr(projDirN, server='smc1', dbN='ihlee_test'):
	inDirL = filter(lambda x: os.path.isdir(projDirN+'/'+x), os.listdir(projDirN))
	for inDir in inDirL:
		post_s_rsq2expr(projDirN + '/' + inDir, server=server, dbN=dbN)

if __name__ == '__main__':
#	post_s_rsq2expr('/EQL1/pipeline/SGI20131031_rsq2expr/S023_RSq', server='smc1')
	post_rsq2expr(projDirN='/EQL3/pipeline/SGI20131226_rsq2expr', server='smc1', dbN='ircr1')