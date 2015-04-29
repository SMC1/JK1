#!/usr/bin/python

import os, re, sys
import mysetting
from glob import glob

def batch(outDirN, inDirL=[], sampL=[], server='smc1'):
	if inDirL == []:
		inDirL = mysetting.wxsMutscanDirL
	for dir in inDirL:
		mutscanFileL = filter(lambda x: 'bak' not in x, map(lambda x: x.rstrip(), os.popen('find %s -name *SS.mutscan' % dir).readlines()))
		for file in mutscanFileL:
			sid = re.match('(.*).mutscan', os.path.basename(file)).group(1)
			if sid in ['S4C_B_SS','S6C_B_SS']:##bad quality
				continue
			cmd = '/usr/bin/python %s/NGS/quality/identity.py -s %s -i %s > %s/%s.snp_signature' % (mysetting.SRC_HOME, sid, file, outDirN,sid)
			log = '%s/%s.identity.log' % (outDirN, sid)
			if not os.path.isfile(log):
#				if sid[0] != 'L' and sid[0] != 'R':
#					continue
				print cmd
				
				os.system('echo "%s" | qsub -q %s -N identity_%s -o %s -j oe' % (cmd, server, sid, log))
	if inDirL == []:
		inDirL = mysetting.rsqMutscanDirL
	for dir in inDirL:
		mutscanFileL = filter(lambda x: 'bak' not in x, map(lambda x: x.rstrip(), os.popen('find %s -name *RSq_splice.mutscan' % dir).readlines()))
		for file in mutscanFileL:
			sid = re.match('(.*)_splice.mutscan', os.path.basename(file)).group(1)

			cmd = '/usr/bin/python %s/NGS/quality/identity.py -s %s -i %s > %s/%s.snp_signature' % (mysetting.SRC_HOME, sid, file, outDirN,sid)
			log = '%s/%s.identity.log' % (outDirN, sid)
			if not os.path.isfile(log):
				print sid, file
				os.system('echo "%s" | qsub -N identity_%s -o %s -j oe' % (cmd, sid, log))

if __name__ == '__main__':
	batch(outDirN='/EQL3/pipeline/identity', server='smc1')
#	batch(outDirN='/EQL5/pipeline/CRC_identity', inDirL=glob('/EQL5/pipeline/*xsq2mut'))
