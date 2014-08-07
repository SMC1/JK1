#!/usr/bin/python

import mysetting, mymysql
import os

def post_xsq2cn(outFileN, platform='', server='smc1', dbN='ircr1'):
	if platform == 'CS':
		cmd = 'cat %s/*/*%s.cn_gene.dat | python ~/JK1/Integration/prepDB_xsq_cn.py > %s' % (mysetting.CScnaDir, platform, outFileN)
	else:
		cmd = 'cat %s/*/*%s.cn_gene.dat | python ~/JK1/Integration/prepDB_xsq_cn.py > %s' % (mysetting.wxsCNADir,platform, outFileN)
	os.system(cmd)
	if platform == 'SS':
		tableN = 'xsq_cn'
	elif platform == 'CS':
		tableN = 'cs_cn'
	else:
		sys.stderr.write('illegal platform name: %s' % platform)
		sys.exit(1)

	mymysql.reset_table(tableN=tableN, dataFileN=outFileN, user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN, host=mysetting.mysqlH[server]['host'])

	## add samp_id if missing
	(con, cursor) = mymysql.connectDB(user=mysetting.mysqlH[server]['user'], passwd=mysetting.mysqlH[server]['passwd'], db=dbN, host=mysetting.mysqlH[server]['host'])
	cursor.execute('SELECT DISTINCT samp_id FROM %s' % tableN)
	sIdL = [x for (x,) in cursor.fetchall()]
	cursor.execute('SELECT DISTINCT samp_id FROM sample_tag WHERE tag like "XSeq_%s%%"' % platform)
	refL = [x for (x,) in cursor.fetchall()]
	for sid in sIdL:
		if sid not in refL:
			pl = platform
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="XSeq_%s"' % (sid, pl))


def post_xsq2purity(outFileN, server='smc1', dbN='ircr1'):
	cmd = 'cat %s/*/*tumor_frac.txt | python ~/JK1/Integration/prepDB_xsq_purity.py > %s' % (mysetting.wxsPurityDir, outFileN)
	os.system(cmd)
	mymysql.reset_table(tableN='xsq_purity', dataFileN=outFileN, user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN, host=mysetting.mysqlH[server]['host'])

def post_xsq2cn_corr(outFileN, server='smc1', dbN='ircr1'):
	cmd = 'cat %s/*/*corr.cn_gene.dat | python ~/JK1/Integration/prepDB_xsq_cn.py > %s' % (mysetting.wxsCNAcorrDir, outFileN)
	os.system(cmd)
	mymysql.reset_table(tableN='xsq_cn_corr', dataFileN=outFileN, user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN, host=mysetting.mysqlH[server]['host'])

def post_xsq2clonality(outFileN, server='smc1', dbN='ircr1'):
	cmd = 'python ~/JK1/Integration/prepDB_xsq_clonality.py > %s' % outFileN
	os.system(cmd)
	mymysql.reset_table(tableN='xsq_clonality', dataFileN=outFileN, user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN, host=mysetting.mysqlH[server]['host'])
	
if __name__ == '__main__':
#	post_xsq2cn('/EQL1/NSL/WXS/results/CNA/CS_CNA_20140603.dat', platform='CS', server='smc1', dbN='CancerSCAN')
#	post_xsq2cn('/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140610.dat', platform='SS', server='smc1', dbN='ircr1')
#	post_xsq2purity('/EQL1/NSL/WXS/results/Purity/XSQ_Purity_20140610.dat',server='smc1', dbN='ircr1')
#	post_xsq2cn_corr('/EQL1/NSL/WXS/results/CNA/XSQ_CNCORR_20140610.dat', server='smc1', dbN='ircr1')
#	post_xsq2clonality('/EQL1/NSL/WXS/results/XSQ_clonality_20140610.dat', server='smc1', dbN='ircr1')
#	post_xsq2cn('/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140616.dat', platform='SS', server='smc1', dbN='ircr1')
#	post_xsq2purity('/EQL1/NSL/WXS/results/Purity/XSQ_Purity_20140616.dat',server='smc1', dbN='ircr1')
#	post_xsq2cn_corr('/EQL1/NSL/WXS/results/CNA/XSQ_CNCORR_20140616.dat', server='smc1', dbN='ircr1')
#	post_xsq2clonality('/EQL1/NSL/WXS/results/XSQ_clonality_20140616.dat', server='smc1', dbN='ircr1')
#	post_xsq2cn('/EQL1/NSL/WXS/results/CNA/CS_CNA_20140619.dat', platform='CS', server='smc1', dbN='CancerSCAN')
#	post_xsq2cn('/EQL1/NSL/WXS/results/CNA/CS_CNA_20140731.dat', platform='CS', server='smc1', dbN='CancerSCAN')
	post_xsq2cn('/EQL1/NSL/WXS/results/CNA/CS_CNA_20140806.dat', platform='CS', server='smc1', dbN='CancerSCAN')
