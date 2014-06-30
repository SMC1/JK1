#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mymysql
from mysetting import mysqlH

def main(inDir, outDir, pbs=False, server='smc1'):

	inFileNL = os.listdir(inDir)
	inFileNL = filter(lambda x: re.match('.*\.ngCGH', x), inFileNL)

	print 'Files: %s' % inFileNL

	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'], passwd=mysqlH[server]['passwd'], db='ircr1', host=mysqlH[server]['host'])
	for inFileN in inFileNL:
		sampN = re.match('(.*)\.ngCGH', inFileN).group(1)
		(sid, tag) = re.match('(.*)_(T.{,2})_[STKN]{2}\.ngCGH', inFileN).groups()
		if tag != 'T':
			sid = '%s_%s' % (sid, tag)
		cursor.execute('SELECT tumor_frac FROM xsq_purity WHERE samp_id="%s"' % sid)
		purity = int(cursor.fetchall()[0][0])

		iprefix = '%s/%s' % (inDir,sampN)
		oprefix = '%s/%s' % (outDir,sampN)
		cmd = 'python ~/JK1/NGS/copynumber/cn_corr.py -i %s.ngCGH -o %s.corr.ngCGH -p %s' % (iprefix, oprefix, purity)
		log = '%s.cn_corr.qlog' % (oprefix)
		print cmd
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) &> %s' % (cmd, log))		


if __name__ == '__main__':
	pass
#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])
#
#	optH = mybasic.parseParam(optL)
#
#	main('/EQL1/NSL/exome_bam/purity/test/copynumber','/EQL1/NSL/exome_bam/purity/test/copynumber', False)
