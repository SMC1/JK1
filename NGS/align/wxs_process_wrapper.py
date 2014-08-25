#!/usr/bin/python

import sys, os, glob, getopt
import mybasic, mysetting

mybasic.add_module_path(['utils'])

import link_fqgz_hj

# linking
link_fqgz_hj.link('/EQL1/NSL/WXS/fastq','/EQL1/NSL/WXS/exome_20130529', '.*([0-9]{3})[ITN].*')


# listing directories
dir_list = glob.glob('/EQL1/NSL/WXS/exome_20130529/*')

#for dir_name in dir_list

def main(pbs=False):

	print dir_list, len(dir_list)
	projectName = 'heejin_20'
	os.system('mkdir /var/www/html/pipeline_logs/%s' % projectName)

	for single_dir in dir_list:

		sampN = single_dir.split('/')[-1]

#		if sampN not in ['S012_T_SS']:
#			continue

		print sampN

		if pbs:
			os.system('echo "/usr/bin/python %s/NGS/align/wxs_process_s.py -i %s -n %s" | qsub -N %s -o %s/%s.wxs_process.log -j oe' % \
				(mysetting.SRC_HOME, single_dir, projectName, sampN, single_dir,sampN))

		else:
			os.system('(/usr/bin/python %s/NGS/align/wxs_process_s.py -i %s -n %s) &> %s/%s.wxs_process.log' % \
				(mysetting.SRC_HOME, single_dir, projectName, single_dir,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'p:',[])
optH = mybasic.parseParam(optL)

main(True)
