#!/usr/bin/python

import sys, os, glob, getopt
import mybasic

sys.path.append('/home/heejin/JK1/utils')

import link_fqgz_hj

# linking
link_fqgz_hj.link('/EQL1/NSL/WXS/fastq','/EQL1/NSL/WXS/exome_20130529', '.*([0-9]{3})[ITN].*')


# listing directories
dir_list = glob.glob('/EQL1/NSL/WXS/exome_20130529/*')

#for dir_name in dir_list

def main(pbs=False):

	print dir_list, len(dir_list)

	for single_dir in dir_list:

		sampN = single_dir.split('/')[-1]

#		if sampN not in ['S012_T_SS']:
#			continue

		print sampN

		if pbs:
			os.system('echo "python ~/JK1/NGS/align/wxs_process_s.py -i %s" | qsub -N %s -o %s/%s.wxs_process.log -j oe' % \
				(single_dir, sampN, single_dir,sampN))

		else:
			os.system('(python ~/JK1/NGS/align/wxs_process_s.py -i %s) &> %s/%s.wxs_process.log' % \
				(single_dir, single_dir,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'p:',[])
optH = mybasic.parseParam(optL)

main(True)
