#!/usr/bin/python

import mysetting, mymysql
import os

def post_xsq2cn(outFileN, server='smc1', dbN='ircr1'):
	cmd = 'cat %s/*/*cn_gene.dat | python ~/JK1/Integration/prepDB_xsq_cn.py > %s' % (mysetting.wxsCNADir, outFileN)
	os.system(cmd)
	mymysql.reset_table(tableN='xsq_cn', dataFileN=outFileN, user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN, host=mysetting.mysqlH[server]['host'])

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
#	post_xsq2cn('hh_cn')
#	post_xsq2purity('hh_purity')
	post_xsq2cn_corr('hh_cn_corr')
	post_xsq2clonality('hh_clonality')
