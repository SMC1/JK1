#!/usr/bin/python

import sys, os, glob, getopt
import mybasic, mysetting

def main(inDirName,pbs=False):

	# listing directories
	dir_list = glob.glob('%s/*' % inDirName)
	
	print dir_list, len(dir_list)

	#for dir_name in dir_list
	
	for single_dir in dir_list:

		sampN = single_dir.split('/')[-1]

#		if sampN not in ['S012_T_SS']:
#			continue

		print sampN

		if pbs:
			os.system('echo "mkdir %s/pileup_proc;\
			chmod a+w %s; \
			/usr/bin/python %s/NGS/mutation/mutation_process.py -i %s" | qsub -N %s -o %s/%s.mutation_process.log -j oe' % \
				(single_dir, single_dir, mysetting.SRC_HOME, single_dir, sampN, single_dir,sampN))

		else:
			os.system('(mkdir %s/pileup_proc; \
			chmod a+w %s; \
			/usr/bin/python %s/NGS/mutation/mutation_process.py -i %s) &> %s/%s.mutation_process.log' % \
				(single_dir, single_dir, mysetting.SRC_HOME, single_dir, single_dir,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'p:',[])
optH = mybasic.parseParam(optL)

main('/EQL1/NSL/WXS/exome_20130529',True)
