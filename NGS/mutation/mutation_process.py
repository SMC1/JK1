#!/usr/bin/python

import sys, os, re, getopt, glob

sys.path.append('/home/heejin/JK1/NGS/align')
sys.path.append('/home/yenakim/JK1/NGS/mutation')

import mybasic, procPileup_split_batch, mutScan_batch, mutscan_snp_cosmic_batch

def main(baseDir, projectName):
	
	current_files_list = []
	compared_files_list = []	
	current_files_list = glob.glob(baseDir+'/*')

	outDir = baseDir + '/pileup_proc'
	
	# compose log string
	html_head_string = '<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head></head><body>'

	# prep html file
	html_path = '/var/www/html/pipeline_logs/' + projectName + '/'
	file_name_split = baseDir.split('/S')
	sample_name = 'S' + file_name_split[1]
	file_name = 'pipeline2_log_' + sample_name + '.html'
	# create .html file
	with open(os.path.join(html_path, file_name), 'wb') as log_file:
		log_file.write(html_head_string)
	log_file.close()

	# change mod and open log_file again
	os.system('chmod 755 %s%s' % (html_path, file_name))
	log_file_name = html_path + file_name
	log_file = open(log_file_name, 'w')

	#----------------------------------------------------------------------------------------------------------------
	# Step5 : execute procPileup_batch.py
	# .pileup -> .pileup_proc 
	try :
		procPileup_split_batch.main(baseDir, outDir, '(.*)\.pileup', False) 
		log_file.write('<b> Step5 is starting ... </b><br>')
	except:
		log_file.write('<b> Step5 is failed </b><br>')
		sys.exit()

	# write procPileup_log string
	# read qlog file and write to .html
	procPileup_log = outDir + '/' + sample_name + '.pileup_proc.log'
	pileup_logfile_size = os.stat(procPileup_log).st_size
	if pileup_logfile_size == 0:
		log_file.write('no error has occured <br>')
	else:
		procPileup_log_file = open(procPileup_log, 'r')
		for procPileup_log_line in procPileup_log_file:
			log_file.write(procPileup_log_line)
			log_file.write('<br>')
		procPileup_log_file.close()
	log_file.write('<br><br>')

	# compose string var - list of files that proc Pileup step has created
	outdir_files_list = glob.glob(outDir+'/*')
	procPileup_str = '<b>step5 - pileup proc successfully created files below : </b><br>'
	for i in range(len(outdir_files_list)):
		outdir_file_item = '--' + str(i) + '.' + str(outdir_files_list[i]) + '<br>'
		procPileup_str += outdir_file_item
	procPileup_str += '<hr>'
	log_file.write(procPileup_str)
	log_file.flush()

	#----------------------------------------------------------------------------------------------------------------
	# Step6 : execute mutScan_batch.py
	# .pileup_proc -> .mutscan
	try:
		mutScan_batch.main(outDir, baseDir, False)
		log_file.write('<b> Step6 is starting ... </b><br>')
	except:
		log_file.write('<b> Step6 is failed </b><br>')
		sys.exit()
	
	# write mutScan log string
	# read qlog file and write to .html
	mutScan_log = baseDir + '/' + sample_name + '.mutscan.log'
	mutScan_logfile_size = os.stat(mutScan_log).st_size
	if mutScan_logfile_size == 0:
		log_file.write('no error has occured <br>')
	else :
		mutScan_log_file = open(mutScan_log, 'r')
		for mutScan_log_line in mutScan_log_file:
			log_file.write(mutScan_log_line)
			log_file.write('<br>')
		mutScan_log_file.close()
	log_file.write('<br><br>')
	
	# compose string var - list of files that mutScan step has created
	tmp_files_list = []
	compared_files_list = []
	tmp_files_list = glob.glob(baseDir + '/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list

	mutScan_str = '<b>step6 - mutScan successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		mutScan_file_item = '-- ' + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		mutScan_str += mutScan_file_item
	mutScan_str += '<hr>'
	log_file.write(mutScan_str)
	log_file.flush()

	#----------------------------------------------------------------------------------------------------------------
	# Step7 : execute mutscan_snp_cosmic_batch.py
	# .mutscan -> cosmic.dat
	try:	
		mutscan_snp_cosmic_batch.main(baseDir)
		log_file.write('<b> Step7 is starting ... </b><br>')
	except:
		log_file.write('<b> Step7 is failed </b><br>')
		sys.exit()	
	
	# write cosmic log string
	# read log file and write to .html
	cosmic_log = baseDir + '/' + sample_name + '.cosmic.log'
	cosmic_logfile_size = os.stat(cosmic_log).st_size
	if cosmic_logfile_size == 0:
		log_file.write('no error has occured <br>')
	else :
		cosmic_log_file = open(cosmic_log, 'r')
		for cosmic_log_line in cosmic_log_file:
			log_file.write(cosmic_log_line)
			log_file.write('<br>')
		cosmic_log_file.close()
	log_file.write('<br><br>')
	
	# compose string var - list of files that mutScan step has created
	tmp_files_list = []
	compared_files_list = []
	tmp_files_list = glob.glob(baseDir + '/*')
	compared_files_list = [file for file in tmp_files_list if file not in current_files_list]
	current_files_list = tmp_files_list

	cosmic_str = '<b>step7 - mutScan snp cosmic successfully created files below : </b><br>'
	for i in range(len(compared_files_list)):
		cosmic_file_item = '-- ' + str(i) + '.' + str(compared_files_list[i]) + '<br>'
		cosmic_str += cosmic_file_item
	cosmic_str += '<hr>'
	log_file.write(cosmic_str)
	log_file.flush()
	#---------------------------------------------------------------------------------------------------------------

	log_file.close()


if __name__ == '__main__':

#optL, argL = getopt.getopt(sys.argv[1:], 'i:n:', [])
#optH = mybasic.parseParam(optL)
#baseDir = optH['-i']
#projectName = optH['-n']
#main(baseDir, projectName)

	main('/home/yenakim/YN/linked_fq/S780_T_SS', 'test_cases')
