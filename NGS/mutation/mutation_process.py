#!/usr/bin/python

import sys, os, re, getopt, glob

sys.path.append('/home/heejin/JK1/NGS/align')
sys.path.append('/home/heejin/JK1/NGS/mutation')

import mybasic, procPileup_split_batch, mutScan_batch, mutscan_snp_cosmic_batch

def main(baseDir):
	
	current_files_list = []
	compared_files_list = []	
	
	current_files_list = glob.glob(baseDir+'/*')

	outDir = baseDir + '/pileup_proc'

	# Step1 : execute procPileup_batch.py
	# .pileup -> .pileup_proc 
	try :
		procPileup_split_batch.main(baseDir, outDir, '(.*)\.pileup', False) 
	except:
		print('step1 is failed')


	# Step2 : execute mutScan_batch.py
	# .pileup_proc -> .mutscan
	try:
		mutScan_batch.main(outDir, baseDir, False)
	except:
		print('step2 is failed')



	# Step3 : execute mutscan_snp_cosmic_batch.py
	# .mutscan -> cosmic.dat
	try:	
		mutscan_snp_cosmic_batch.main(baseDir)	
	except:
		print('step3 is failed')


#
#	#compose whole log string
#	whole_log_string = '<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head></head><body>' + bwa_string + duplicates_string + realign_string + pileup_string + '</body></html>'
#
#	#write html file
#	html_path = '/var/www/html/'
#
#	file_name = 'pipeline_log_' + sample_name + '.html'
#	#file_name = 'pipeline_log.html'
#	with open(os.path.join(html_path, file_name), 'wb') as temp_file:
#		temp_file.write(whole_log_string)
#		temp_file.close()
#
#	#os.system('chmod 777 %s' % file_name)

optL, argL = getopt.getopt(sys.argv[1:], 'i:', [])

optH = mybasic.parseParam(optL)

baseDir = optH['-i']

main(baseDir)
