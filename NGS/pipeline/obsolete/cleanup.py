#!/usr/bin/python

import sys, os
from glob import glob

def main(inputFilePre,inputFileFmt,baseDir,sampN):

	qlogStr = ''

	if glob(baseDir):
		qlogStr += '<b> %s already exists </b></br>' % baseDir
	else:
		ret = os.system('mkdir '+baseDir )

	if ret != 0:
		print '<b> failed to created sample directory </b><br>'
		sys.exit()

	qlogF = open('%s/%s.mkdirln.qlog' % (baseDir,sampN))
	qlogF.write(qlogStr + '<b> created sample directory </b></br>')

	ret1 = os.system('ln -f -s %s.1.%s %s/%s.1.%s' % (inputFilePre,inputFileFmt,baseDir,sampN,inputFileFmt))
	ret2 = os.system('ln -f -s %s.2.%s %s/%s.2.%s' % (inputFilePre,inputFileFmt,baseDir,sampN,inputFileFmt))

	if ret1!=0 or ret2!=0:
		qlogF.write('<b> failed to link input file</b><br>')
		qlogF.close()
		sys.exit(1)

	qlogF.close()

#if __name__ == '__main__':
#	main('')
