#!/usr/bin/python

import sys, os
import mymysql
from mysetting import mysqlH

moduleL = ['Integration'] ## DIRECTORY
homeDir = os.popen('echo $HOME','r').read().rstrip()

for module in moduleL:
	sys.path.append('%s/JK1/%s' % (homeDir,module))
import prepDB_mutscan, makeDB_mutation_rxsq

def post_s_rsq2mut(baseDir, server='smc1', dbN='ihlee_test'):
	sampN = baseDir.split('/')[-1]
	sid = sampN[:-4].replace('.','_').replace('-','_')
	print sampN, sid

	cosmicDatFileN = '%s/%s_splice_cosmic.dat' % (baseDir, sampN)
	if dbN in ['ihlee_test','ircr1']:
		datFileN = '/EQL1/NSL/RNASeq/results/mutation/%s.dat' % sampN
	else:
		datFileN = '%s/%s.dat' % (baseDir, sampN)
	if os.path.isfile(cosmicDatFileN):
		prepDB_mutscan.main(sampNamePat=('(.*)_(RSq)',''), geneList=[], inFileN=cosmicDatFileN, outFileN=datFileN)

		## import
		(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
		cursor.execute('DELETE FROM mutation_rsq WHERE samp_id="%s"' % sid)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE mutation_rsq' % datFileN)
		## make sure to update sample_tag that this sample has RNA-Seq
		cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
		results = cursor.fetchall()
		if len(results) < 1:
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)

def post_rsq2mut(projDirN, idL=[], server='smc1', dbN='ihlee_test'):
	inDirL = filter(lambda x: os.path.isdir(projDirN+'/'+x), os.listdir(projDirN))
	for inDir in inDirL:
		if idL != [] and inDir not in idL:
			continue
		post_s_rsq2mut(projDirN + '/' + inDir, server=server, dbN=dbN)
	makeDB_mutation_rxsq.main(dbN=dbN)

if __name__ == '__main__':
#	post_rsq2mut('/EQL3/pipeline/SGI20131226_rsq2mut', server='smc1', dbN='ircr1')
#	post_s_rsq2mut('/EQL3/pipeline/SGI20131226_rsq2mut/S633_RSq', server='smc1', dbN='ircr1')
#	post_rsq2mut('/EQL2/pipeline/SGI20140204_rsq2mut', server='smc1', dbN='ircr1')
#	post_rsq2mut('/EQL2/pipeline/SGI20140219_rsq2mut', server='smc1', dbN='ircr1')
#	post_rsq2mut(projDirN='/EQL6/pipeline/SCS20140104_rsq2mut', server='smc1', dbN='IRCR_GBM_352_SCS')
#	post_rsq2mut(projDirN='/EQL6/pipeline/SCS20140203_rsq2mut', server='smc1', dbN='IRCR_GBM_363_SCS')
#	post_rsq2mut(projDirN='/EQL6/pipeline/JKM20140314_bulk_rsq2mut', server='smc1', dbN='RC085_LC195_bulk')
#	post_rsq2mut(projDirN='/EQL6/pipeline/JKM20140314_SCS_RM_rsq2mut', server='smc1', dbN='LC_195_SCS')
#	post_rsq2mut(projDirN='/EQL2/pipeline/SGI20140331_rsq2mut', server='smc1', dbN='ircr1')
#	post_rsq2mut(projDirN='/EQL6/pipeline/SCS20140422_rsq2mut', server='smc1', dbN='IRCR_GBM_412_SCS')
#	post_rsq2mut(projDirN='/EQL3/pipeline/SGI20140526_rsq2mut', server='smc1', dbN='ircr1')
#	post_rsq2mut(projDirN='/EQL3/pipeline/SGI20140520_rsq2mut', server='smc1', dbN='ircr1')
	post_rsq2mut(projDirN='/EQL3/pipeline/SGI20140602_rsq2mut', server='smc1', dbN='ircr1')
