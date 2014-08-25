#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mymysql, mysetting

def main(inDir, outDir, cnDir, pbs=False, server='smc1'):

	inFileNL = os.listdir(inDir)
	inFileNL = filter(lambda x: not re.match('(.*)\.union_pos\.mutect$', x), filter(lambda x: re.match('(.*)\.mutect$', x), inFileNL))

	print 'Files: %s' % inFileNL

	(con, cursor) = mymysql.connectDB(user=mysetting.mysqlH[server]['user'], passwd=mysetting.mysqlH[server]['passwd'], db='ircr1', host=mysetting.mysqlH[server]['host'])
	for inFileN in inFileNL:
		sampN = re.match('(.*)\.mutect', inFileN).group(1)
		(sid, postfix) = re.match('(.*)_(T.{,2})_[STKN]{2}\.mutect', inFileN).groups()
		if postfix != 'T':
			sid = '%s_%s' % (sid, postfix)
		cursor.execute('SELECT tumor_frac FROM xsq_purity WHERE samp_id="%s"' % sid)
		result = cursor.fetchall()
		if len(result) > 0 and result[0][0] != 'ND':
			purity = int(result[0][0])
			iprefix = '%s/%s' % (inDir, sampN)
			oprefix = '%s/%s' % (outDir, sampN)
			segFile = '%s/%s/%s.ngCGH.seg' % (cnDir, sampN, sampN)
			if os.path.isfile(segFile) and not os.path.isfile('%s.mutect_cl.dat' % (oprefix)):
				cmd = '/usr/bin/python %s/NGS/mutation/mut_clonality.py -s %s -i %s.mutect -o %s.mutect_cl.dat -p %s' % (mysetting.SRC_HOME, segFile, iprefix, oprefix, purity)
				log = '%s.mutect_cl.log' % (oprefix)

				if pbs:
					os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
				else:
					os.system('(%s) &> %s' % (cmd, log))
			else:
				print "Missing copy number segmentation file!"
				sys.exit(1)

if __name__ == '__main__':
	main('/EQL3/pipeline/somatic_mutect', '/EQL3/pipeline/somatic_mutect', '/EQL3/pipeline/CNA', False, 'smc1')
