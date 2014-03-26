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
RSQPattern=('(.*)_RSq','')

def post_rsq2skip(dirN, server='smc1', dbN='ihlee_test', sampL=[]):
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
	cursor.execute('ALTER TABLE splice_normal CHANGE COLUMN samp_id samp_id char(63)')
	cursor.execute('ALTER TABLE splice_normal_loc1 CHANGE COLUMN samp_id samp_id char(63)')
	cursor.execute('ALTER TABLE splice_normal_loc2 CHANGE COLUMN samp_id samp_id char(63)')
	cursor.execute('CREATE TEMPORARY TABLE splice_normal_tmp LIKE splice_normal')
	sampNL = filter(lambda x: os.path.isdir(dirN + '/' + x), os.listdir(dirN))
	for sampN in sampNL:
		baseDir = dirN + '/' + sampN
		sid = sampN[:-4].replace('.','_').replace('-','_') ## RNASeq sample has '***_RSq'
		if sampL != [] and sid not in sampL:
			continue
		print sampN, sid
		## make sure to update sample_tag that this sample has RNA-Seq
		cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
		results = cursor.fetchall()
		if len(results) < 1:
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)

		normal_report = glob('%s/%s*normal_report.txt' % (baseDir, sampN))[0]
		if dbN in ['ihlee_test','ircr1']:
			splice_normal = '%s/exonSkip_normal/splice_normal_%s.dat' % (BASE, sampN)
		else:
			splice_normal = '%s/splice_normal_%s.dat' % (baseDir, sampN)
		prepDB_splice_normal.main(sampNamePat=RSQPattern, inFileN=normal_report, outFileN=splice_normal)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE splice_normal_tmp' % splice_normal)

		skip_report_annot = glob('%s/%s*_splice_exonSkip_report_annot.txt' % (baseDir, sampN))[0]
		if dbN in ['ihlee_test','ircr1']:
			splice_skip_txt = '%s/exonSkip/splice_skip_%s.txt' % (BASE, sampN)
		else:
			splice_skip_txt = '%s/splice_skip_%s.txt' % (baseDir, sampN)
		exonSkip_summarize.exonSkip_summarize_s(inFileN=skip_report_annot, minPos=1, outFileN=splice_skip_txt)
		if dbN in ['ihlee_test','ircr1']:
			splice_skip_dat = '%s/exonSkip/splice_skip_%s.dat' % (BASE, sampN)
		else:
			splice_skip_dat = '%s/splice_skip_%s.dat' % (baseDir, sampN)
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

def post_rsq2fusion(dirN, server='smc1', dbN='ihlee_test', sampL=[]):
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
	sampNL = filter(lambda x: os.path.isdir(dirN + '/' + x), os.listdir(dirN))
	for sampN in sampNL:
		baseDir = dirN + '/' + sampN
		sid = sampN[:-4].replace('.','_').replace('-','_') ## RNASeq sample has '***_RSq'
		if sampL != [] and sid not in sampL:
			continue
		print sampN, sid
		## make sure to update sample_tag that this sample has RNA-Seq
		cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
		results = cursor.fetchall()
		if len(results) < 1:
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)

		fusion_report_annot = glob('%s/%s*_splice_transloc_annot1.report_annot.txt' % (baseDir, sampN))[0]
		if dbN in ['ihlee_test','ircr1']:
			splice_fusion_txt = '%s/fusion/splice_fusion_%s.txt' % (BASE, sampN)
		else:
			splice_fusion_txt = '%s/splice_fusion_%s.txt' % (baseDir, sampN)
		fusion_summarize.fusion_summarize_s(inputFileN=fusion_report_annot, minNPos=1, outFileN=splice_fusion_txt)
		if dbN in ['ihlee_test','ircr1']:
			splice_fusion_dat = '%s/fusion/splice_fusion_%s.dat' % (BASE, sampN)
		else:
			splice_fusion_dat = '%s/splice_fusion_%s.dat' % (baseDir, sampN)
		prepDB_splice_fusion.main(inGctFileName=splice_fusion_txt, minNPos=1, sampNamePat=RSQPattern, geneList=[], outFileN=splice_fusion_dat)
		cursor.execute('DELETE FROM splice_fusion WHERE samp_id="%s"' % sid)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" IGNORE INTO TABLE splice_fusion' % splice_fusion_dat)
		cursor.execute('DELETE FROM splice_fusion WHERE gene_sym1 LIKE "HLA-%" AND gene_sym2 LIKE "HLA-%"')
	makeDB_splice_AF.fusion(dbN=dbN, cursor=cursor)

def post_rsq2eiJunc(dirN, server='smc1', dbN='ihlee_test', sampL=[]):
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
	sampNL = filter(lambda x: os.path.isdir(dirN + '/' + x), os.listdir(dirN))
	for sampN in sampNL:
		baseDir = dirN + '/' + sampN
		sid = sampN[:-4].replace('.','_').replace('-','_') ## RNASeq sample has '***_RSq'
		if sampL != [] and sid not in sampL:
			continue
		print sampN, sid
		## make sure to update sample_tag that this sample has RNA-Seq
		cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
		results = cursor.fetchall()
		if len(results) < 1:
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)
		ei_dat = glob('%s/%s*ei.dat' % (baseDir, sampN))[0]
		if dbN in ['ihlee_test','ircr1']:
			splice_eiJunc_txt = '%s/eiJunc/splice_eiJunc_%s_ft.txt' % (BASE, sampN)
		else:
			splice_eiJunc_txt = '%s/splice_eiJunc_%s_ft.txt' % (baseDir, sampN)
		ei_junc_filter.main(overlap=10, minNReads=1, inFileN=ei_dat, outFileN=splice_eiJunc_txt)
		if dbN in ['ihlee_test','ircr1']:
			splice_eiJunc_dat = '%s/eiJunc/splice_eiJunc_%s.dat' % (BASE, sampN)
		else:
			splice_eiJunc_dat = '%s/splice_eiJunc_%s.dat' % (baseDir, sampN)
		prepDB_splice_eiJunc.main(minNReads=1, sampNamePat=RSQPattern, geneList=[], inFileN=splice_eiJunc_txt, outFileN=splice_eiJunc_dat)
		cursor.execute('DELETE FROM splice_eiJunc WHERE samp_id="%s"' % sid)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" IGNORE INTO TABLE splice_eiJunc' % splice_eiJunc_dat)
	makeDB_splice_AF.eiJunc(dbN=dbN, cursor=cursor)

def main(dirH, server='smc1', dbN='ihlee_test', sampL=[]):
	post_rsq2skip(dirH['skip'], server=server, dbN=dbN, sampL=sampL)
	post_rsq2fusion(dirH['fusion'], server=server, dbN=dbN, sampL=sampL)
	post_rsq2eiJunc(dirH['eiJunc'], server=server, dbN=dbN, sampL=sampL)


if __name__ == '__main__':
#	dirH = {'eiJunc':'/EQL3/pipeline/SGI20131226_rsq2eiJunc', 'fusion':'/EQL3/pipeline/SGI20131226_rsq2fusion', 'skip':'/EQL3/pipeline/SGI20131226_rsq2skip'}
#	dirH = {'eiJunc':'/EQL2/pipeline/SGI20140204_rsq2eiJunc', 'fusion':'/EQL2/pipeline/SGI20140204_rsq2fusion', 'skip':'/EQL2/pipeline/SGI20140204_rsq2skip'}
#	dirH = {'eiJunc':'/EQL2/pipeline/SGI20140219_rsq2eiJunc', 'fusion':'/EQL2/pipeline/SGI20140219_rsq2fusion', 'skip':'/EQL2/pipeline/SGI20140219_rsq2skip'}
#	dirH = {'eiJunc':'/EQL6/pipeline/SCS20140203_rsq2eiJunc', 'fusion':'/EQL6/pipeline/SCS20140203_rsq2fusion', 'skip':'/EQL6/pipeline/SCS20140203_rsq2skip'}
	dirH = {'eiJunc':'/EQL6/pipeline/JKM20140314_bulk_rsq2eiJunc', 'fusion':'/EQL6/pipeline/JKM20140314_bulk_rsq2fusion', 'skip':'/EQL6/pipeline/JKM20140314_bulk_rsq2skip'}

#	main(dirH, server='smc1', dbN='ircr1')
#	main(dirH, server='smc1', dbN='ircr1', sampL=['S633'])
#	main(dirH, server='smc1', dbN='IRCR_GBM_352_SCS')
#	main(dirH, server='smc1', dbN='IRCR_GBM_363_SCS')
	main(dirH, server='smc1', dbN='RC085_LC195_bulk')
