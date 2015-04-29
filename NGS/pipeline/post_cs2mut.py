#!/usr/bin/python

import sys, os, re
import mysetting, mymysql, mybasic
from glob import glob

def main(datFileN, server='smc1', dbN='CancerSCAN'):
	mybasic.add_module_path(['NGS/mutation','Integration'])

	import vep_batch, makeDB_mutation_rxsq
	print mysetting.CSmutDir+'/*CS'
	vep_batch.main(glob(mysetting.CSmutDir+'/*CS'), postfixL=['.mutect_filter.vcf','.mutect_single_filter.vcf','.indels_filter.vcf','.indels_single_filter.vcf'], fork=True)

	os.system('cat %s/*CS/*filter_vep.dat | /usr/bin/python %s/Integration/prepDB_mutation_cancerscan.py > %s' % (mysetting.CSmutDir, mysetting.SRC_HOME, datFileN))
	mymysql.reset_table(tableN='mutation_cs', dataFileN=datFileN, user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN,host=mysetting.mysqlH[server]['host'])

	(con, cursor) = mymysql.connectDB(user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN,host=mysetting.mysqlH[server]['host'])
	sampNL = filter(lambda x: os.path.isdir(mysetting.CSmutDir+'/'+x), os.listdir(mysetting.CSmutDir))
	for sampN in sampNL:
		id = '_'.join(sampN.split('_')[:-2])
		postfix = sampN.split('_')[-2]
		if postfix == 'B':
			continue
		if postfix != 'T':
			id = '%s_%s' % (id, postfix)
		cursor.execute('''DELETE FROM sample_tag WHERE samp_id="%s" AND tag="XSeq_CS"''' % id)
		cursor.execute('''INSERT INTO sample_tag SET samp_id="%s",tag="XSeq_CS"''' % id)



if __name__ == '__main__':
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140723.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140730.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140806.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140822.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140826.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140828.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140829.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140915.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20140925.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20141105.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20141119.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20141219.dat', server='smc1', dbN='CancerSCAN')
#	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20150104.dat', server='smc1', dbN='CancerSCAN')
	main(datFileN='/EQL1/NSL/WXS/results/mutation/mutation_CS_20150226.dat', server='smc1', dbN='CancerSCAN')
