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
	sid = sampN[:-4]
	print sampN, sid

	cosmicDatFileN = '%s/%s_splice_cosmic.dat' % (baseDir, sampN)
	datFileN = '/EQL1/NSL/RNASeq/results/mutation/%s.dat' % sampN
	if os.path.isfile(cosmicDatFileN):
		prepDB_mutscan.main(sampNamePat=('.{1}(.*)_RSq',''), geneList=[], inFileN=cosmicDatFileN, outFileN=datFileN)

		## import
		(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'],passwd=mysqlH[server]['passwd'],db=dbN,host=mysqlH[server]['host'])
		cursor.execute('DELETE FROM mutation_rsq WHERE samp_id="%s"' % sid)
		cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE mutation_rsq' % datFileN)
		## make sure to update sample_tag that this sample has RNA-Seq
		cursor.execute('SELECT * FROM sample_tag WHERE samp_id="%s" AND tag="RNA-Seq"' % sid)
		results = cursor.fetchall()
		if len(results) < 1:
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="RNA-Seq"' % sid)

def post_rsq2mut(projDirN, server='smc1', dbN='ihlee_test'):
	inDirL = filter(lambda x: os.path.isdir(projDirN+'/'+x), os.listdir(projDirN))
	for inDir in inDirL:
		post_s_rsq2mut(projDirN + '/' + inDir, server=server, dbN=dbN)
	makeDB_mutation_rxsq.main(dbN=dbN)

if __name__ == '__main__':
	post_rsq2mut('/EQL3/pipeline/SGI20131226_rsq2mut', server='smc1', dbN='ircr1')
