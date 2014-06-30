#!/usr/bin/python

import os, sys
import mysetting
from glob import glob

def main(dirL, outFileName):
	datH = {}
	inFileL = []
	for dir in dirL:
		fname = glob('%s/*_B_*.rpkm' % dir)[0]
		inFileL.append(fname)
		inFile = open(fname, 'r')
		inFile.readline()
		for line in inFile:
			colL = line.rstrip().split('\t')
			key = colL[0]
			cnt = int(colL[1])
			rpkm = float(colL[2])
			length = int(colL[4])
			
			if key in datH:
				datH[key]['cnt'] = min(datH[key]['cnt'], cnt)
				datH[key]['rpkm'] += rpkm
				datH[key]['n'] += 1
				if datH[key]['len'] != length:
					print key,datH[key]['len'],length
					sys.exit(1)
			else:
				datH[key] = {'cnt': cnt, 'rpkm': rpkm, 'n': 1, 'len':length}
	
	outFile = open(outFileName, 'w')
	outFile.write('# %s pooled samples:\n' % len(inFileL))
	outFile.write('# %s\n' % ','.join(inFileL))
	outFile.write('locus\tmin_count\tavg(RPKM)\tTotal_reads\tlength\n')
	for key in datH:
		if datH[key]['n'] < len(dirL): ## anything missing?
			print key
			sys.exit(1)
		else:
			outFile.write('%s\t%s\t%s\tNA\t%s\n' % (key, datH[key]['cnt'], datH[key]['rpkm']/float(datH[key]['n']),datH[key]['len']))
	sampN = os.path.dirname(outFileName).split('/')[-1]
	logFile = open('%s/%s.PooledRPKM.qlog' % (os.path.normpath(os.path.dirname(outFileName)), sampN), 'w')
	logFile.write('%s pooled samples:\n' % len(inFileL))
	logFile.write('%s\n' % ','.join(inFileL))
	logFile.flush()
	logFile.close()

if __name__ == '__main__':
#	main(map(lambda x: baseDir + '/' + x, dirL), baseDir + '/poolB/SGI_B_pool.rpkm')
#	main(map(lambda x: baseDir + '/' + x, dirL), baseDir + '/poolB/DNALink_B_pool.rpkm')
	pass
