#!/usr/bin/python

import sys, os, re
import mymysql

def summarize_TMZ(inMUTECT, inMUTSCAN, outFileN=''):
	inFile = open(inMUTECT, 'r')

	dataH = {}
	for line in inFile:
		if 'samp_id' in line:
			continue
		colL = line.rstrip().split('\t')
		id = colL[0]
		mut = colL[1]
		context = colL[2]
		cnt = int(colL[3])
		tail = context[-1]

		if mut == 'C>T' and tail in ['C','T']: ## TMZ mutation
			if id not in dataH:
				dataH[id] = {'mutect':{'TMZ':0, 'nonTMZ':0}, 'mutscan':{'TMZ':0, 'nonTMZ':0}, 'Norm':True}
			dataH[id]['mutect']['TMZ'] += cnt
		else: ##non-TMZ mutation
			if id not in dataH:
				dataH[id] = {'mutect':{'TMZ':0, 'nonTMZ':0}, 'mutscan':{'TMZ':0, 'nonTMZ':0}, 'Norm':True}
			dataH[id]['mutect']['nonTMZ'] += cnt
	##for line

	inFile = open(inMUTSCAN, 'r')
	for line in inFile:
		if 'samp_id' in line:
			continue
		colL = line.rstrip().split('\t')
		id = colL[0]
		ro = re.match('(.*)_T_[ST]S', id)
		if not ro:
			continue
		id = ro.group(1)
		mut = colL[1]
		context = colL[2]
		cnt = int(colL[3])
		tail = context[-1]

		if mut == 'C>T' and tail in ['C','T']: ## TMZ mutation
			if id not in dataH:
				dataH[id] = {'mutect':{'TMZ':0, 'nonTMZ':0}, 'mutscan':{'TMZ':0, 'nonTMZ':0}, 'Norm':False}
			dataH[id]['mutscan']['TMZ'] += cnt
		else: ##non-TMZ mutation
			if id not in dataH:
				dataH[id] = {'mutect':{'TMZ':0, 'nonTMZ':0}, 'mutscan':{'TMZ':0, 'nonTMZ':0}, 'Norm':False}
			dataH[id]['mutscan']['nonTMZ'] += cnt
	if outFileN == '':
		outFile = sys.stdout
	else:
		outFile = open(outFileN, 'w')
	
	(con, cursor) = mymysql.connectDB(db='ircr1')
	outFile.write('SID\tTMZ:mutect\tnonTMZ:mutect\tTMZ:mutscan\tnonTMZ:mutscan\tNormal\tMGMT:exp\n')
	for id in dataH:
		outFile.write('%s' % id)
		for prog in ['mutect','mutscan']:
			for var in ['TMZ','nonTMZ']:
				outFile.write('\t%s' % dataH[id][prog][var])
		cursor.execute('select rpkm from rpkm_gene_expr where gene_sym="MGMT" and samp_id="%s"' % id)
		results = cursor.fetchone()
		mgmt_exp = -1
		if results:
			mgmt_exp = results[0]
		outFile.write('\t%s\t%s\n' % (dataH[id]['Norm'], mgmt_exp))

if __name__ == '__main__':
	summarize_TMZ('/EQL1/NSL/WXS/results/mutation/mutation_signature_mutect_20140227.txt', '/EQL1/NSL/WXS/results/mutation/mutation_signature_mutscan_20140227.txt', '/EQL1/NSL/WXS/results/mutation/mutation_signature_TMZ_20140227.txt')
