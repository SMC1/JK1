#!/usr/bin/python
## postprocessing for RNA-Seq pipelines : rsq2skip, rsq2fusion, rsq2eiJunc
## handles 3 pipeline at the same time: no need to run 3 times after each pipeline

from glob import glob
import sys, os
import mymysql
from mysetting import mysqlH
from datetime import datetime
from warnings import filterwarnings
from warnings import resetwarnings

moduleL = ['NGS/splice_gsnap/skipping','NGS/splice_gsnap/fusion','NGS/splice_gsnap/ei_junc','Integration'] ## DIRECTORY
homeDir = os.popen('echo $HOME','r').read().rstrip()

for module in moduleL:
	sys.path.append('%s/JK1/%s' % (homeDir,module))
import makeDB_splice_AF
import prepDB_splice_normal, exonSkip_summarize, prepDB_splice_skip
import fusion_summarize, prepDB_splice_fusion
import ei_junc_filter, prepDB_splice_eiJunc

BASE='/EQL1/NSL/RNASeq/results'
RSQPattern=('.{1}(.*)_RSq','S')

def post_rsq2skip(dirN, server='smc1', dbN='ihlee_test'):
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
	cursor.execute('CREATE TEMPORARY TABLE splice_normal_tmp LIKE splice_normal')
	sampNL = filter(lambda x: os.path.isdir(dirN + '/' + x), os.listdir(dirN))
	for sampN in sampNL:
		baseDir = dirN + '/' + sampN
		sid = sampN[:-4] ## RNASeq sample has '***_RSq'
		## make sure to update sample_tag that this sample has RNA-Seq
		cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
		results = cursor.fetchall()
		if len(results) < 1:
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)

		normal_report = glob('%s/%s*normal_report.txt' % (baseDir, sampN))[0]
		splice_normal = '%s/exonSkip_normal/splice_normal_%s.dat' % (BASE, sampN)
		prepDB_splice_normal.main(sampNamePat=RSQPattern, inFileN=normal_report, outFileN=splice_normal)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE splice_normal_tmp' % splice_normal)

		skip_report_annot = glob('%s/%s*_splice_exonSkip_report_annot.txt' % (baseDir, sampN))[0]
		splice_skip_txt = '%s/exonSkip/splice_skip_%s.txt' % (BASE, sampN)
		exonSkip_summarize.exonSkip_summarize_s(inFileN=skip_report_annot, minPos=1, outFileN=splice_skip_txt)
		splice_skip_dat = '%s/exonSkip/splice_skip_%s.dat' % (BASE, sampN)
		prepDB_splice_skip.main(inFileName=splice_skip_txt, minNPos=1, sampNamePat=RSQPattern, geneList=[], outFileName=splice_skip_dat)
		cursor.execute('DELETE FROM splice_skip WHERE samp_id="%s"' % sid)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" IGNORE INTO TABLE splice_skip' % splice_skip_dat)
	
	cursor.execute('ALTER TABLE splice_normal DISABLE KEYS')
	cursor.execute('INSERT INTO splice_normal SELECT * FROM splice_normal_tmp')
	cursor.execute('ALTER TABLE splice_normal ENABLE KEYS')
	cursor.execute('ALTER TABLE splice_normal_loc1 DISABLE KEYS')
	cursor.execute('DELETE FROM splice_normal_loc1 WHERE samp_id in (SELECT DISTINCT samp_id FROM splice_normal_tmp)')
	cursor.execute('INSERT INTO splice_normal_loc1 SELECT samp_id,loc1,sum(nReads) nReads_w1 FROM splice_normal_tmp GROUP BY samp_id,loc1')
	cursor.execute('ALTER TABLE splice_normal_loc1 ENABLE KEYS')
	cursor.execute('ALTER TABLE splice_normal_loc2 DISABLE KEYS')
	cursor.execute('DELETE FROM splice_normal_loc2 WHERE samp_id in (SELECT DISTINCT samp_id FROM splice_normal_tmp)')
	cursor.execute('INSERT INTO splice_normal_loc2 SELECT samp_id,loc2,sum(nReads) nReads_w2 FROM splice_normal_tmp GROUP BY samp_id,loc2')
	cursor.execute('ALTER TABLE splice_normal_loc2 ENABLE KEYS')
	makeDB_splice_AF.skip(dbN=dbN, cursor=cursor)
	cursor.execute('DROP TEMPORARY TABLE IF EXISTS splice_normal_tmp')

def post_rsq2fusion(dirN, server='smc1', dbN='ihlee_test'):
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
	sampNL = filter(lambda x: os.path.isdir(dirN + '/' + x), os.listdir(dirN))
	for sampN in sampNL:
		baseDir = dirN + '/' + sampN
		sid = sampN[:-4] ## RNASeq sample has '***_RSq'
		## make sure to update sample_tag that this sample has RNA-Seq
		cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
		results = cursor.fetchall()
		if len(results) < 1:
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)

		fusion_report_annot = glob('%s/%s*_splice_transloc_annot1.report_annot.txt' % (baseDir, sampN))[0]
		splice_fusion_txt = '%s/fusion/splice_fusion_%s.txt' % (BASE, sampN)
		fusion_summarize.fusion_summarize_s(inputFileN=fusion_report_annot, minNPos=1, outFileN=splice_fusion_txt)
		splice_fusion_dat = '%s/fusion/splice_fusion_%s.dat' % (BASE, sampN)
		prepDB_splice_fusion.main(inGctFileName=splice_fusion_txt, minNPos=1, sampNamePat=RSQPattern, geneList=[], outFileN=splice_fusion_dat)
		cursor.execute('DELETE FROM splice_fusion WHERE samp_id="%s"' % sid)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" IGNORE INTO TABLE splice_fusion' % splice_fusion_dat)
		cursor.execute('DELETE FROM splice_fusion WHERE gene_sym1 LIKE "HLA-%" AND gene_sym2 LIKE "HLA-%"')
	makeDB_splice_AF.fusion(dbN=dbN, cursor=cursor)

def post_rsq2eiJunc(dirN, server='smc1', dbN='ihlee_test'):
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
	sampNL = filter(lambda x: os.path.isdir(dirN + '/' + x), os.listdir(dirN))
	for sampN in sampNL:
		baseDir = dirN + '/' + sampN
		sid = sampN[:-4] ## RNASeq sample has '***_RSq'
		## make sure to update sample_tag that this sample has RNA-Seq
		cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
		results = cursor.fetchall()
		if len(results) < 1:
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)
		ei_dat = glob('%s/%s*ei.dat' % (baseDir, sampN))[0]
		splice_eiJunc_txt = '%s/eiJunc/splice_eiJunc_%s_ft.txt' % (BASE, sampN)
		ei_junc_filter.main(overlap=10, minNReads=1, inFileN=ei_dat, outFileN=splice_eiJunc_txt)
		splice_eiJunc_dat = '%s/eiJunc/splice_eiJunc_%s.dat' % (BASE, sampN)
		prepDB_splice_eiJunc.main(minNReads=1, sampNamePat=RSQPattern, geneList=[], inFileN=splice_eiJunc_txt, outFileN=splice_eiJunc_dat)
		cursor.execute('DELETE FROM splice_eiJunc WHERE samp_id="%s"' % sid)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" IGNORE INTO TABLE splice_eiJunc' % splice_eiJunc_dat)
	makeDB_splice_AF.eiJunc(dbN=dbN, cursor=cursor)

def main(dirH, server='smc1', dbN='ihlee_test'):
#	post_rsq2skip(dirH['skip'], server=server, dbN=dbN)
#	post_rsq2fusion(dirH['fusion'], server=server, dbN=dbN)
	post_rsq2eiJunc(dirH['eiJunc'], server=server, dbN=dbN)


if __name__ == '__main__':
	dirH = {'eiJunc':'/EQL3/pipeline/SGI20131226_rsq2eiJunc', 'fusion':'/EQL3/pipeline/SGI20131226_rsq2fusion', 'skip':'/EQL3/pipeline/SGI20131226_rsq2skip'}

	main(dirH, server='smc1', dbN='ircr1')
