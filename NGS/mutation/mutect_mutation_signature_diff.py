#!/usr/bin/python

import sys, os, re
import mybasic, mysetting
mybasic.add_module_path(['NGS/pipeline'])
import mypipe

def diff_batch(trioFileN, tidL=[]):
	bamDirL = mysetting.wxsBamDirL
	trioH = mypipe.read_trio(trioFileN, bamDirL, tidL)

	for tid in trioH:
		if tidL != [] and tid not in tidL:
			continue
		if trioH[tid]['Normal'] == [] or trioH[tid]['prim_id'] == [] or trioH[tid]['recur_id'] == []:
			continue

		datH = {}
		for ref in ['C','T']:
			for alt in ['A','C','G','T']:
				if alt == ref:
					continue
				mut = '%s>%s' % (ref, alt)
				for a in ['A','C','G','T']:
					for b in ['A','C','G','T']:
						context = a + ref + b
						datH[(mut, context)] = {'prim':0.0, 'recur':0.0, 'delta':0.0}
					#for b
				#for a
			#for alt
		#for ref

		print tid, trioH[tid]['prim_id'], trioH[tid]['recur_id']
		for rid in trioH[tid]['recur_id']:
			pid = trioH[tid]['prim_id'][0]
			p_file = '/EQL3/pipeline/somatic_mutation/%s/%s.mutation_signature.txt' % (pid,pid)
			r_file = '/EQL3/pipeline/somatic_mutation/%s/%s.mutation_signature.txt' % (rid,rid)

			if os.path.isfile(p_file) and os.path.isfile(r_file):
				print p_file
				inFile = open(p_file, 'r')
				inFile.readline()
				for line in inFile:
					colL = line.rstrip().split('\t')
					mut = colL[1]
					context = colL[2]
					frac = float(colL[3])/float(colL[5])
					datH[(mut,context)]['prim'] = frac
				#for line
				inFile.close()
				print r_file
				inFile = open(r_file, 'r')
				inFile.readline()
				for line in inFile:
					colL = line.rstrip().split('\t')
					mut = colL[1]
					context = colL[2]
					frac = float(colL[3])/float(colL[5])
					datH[(mut,context)]['recur'] = frac
				#for line
				inFile.close()

#				ofileN = '/EQL3/pipeline/somatic_mutation/%s/%s.mutation_signature_diff.txt' % (rid,rid)
#				outFile = open(ofileN, 'w')
#				outFile.write('prim_id\trecur_id\tmutation\tcontext\tp_frac\tr_frac\tdelta\n')
#				for key in datH:
#					(mut, context) = key
#					datH[key]['delta'] = datH[key]['recur'] - datH[key]['prim']
#					outFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (pid, rid, mut, context, datH[key]['prim'], datH[key]['recur'], datH[key]['delta']))
#				outFile.flush()
#				outFile.close()
				os.system('Rscript %s/NGS/mutation/mutect_mutation_signature_diff_plot.R %s %s' % (mysetting.SRC_HOME, pid, rid))
			#if

if __name__ == '__main__':
	tidL = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','26','27','28','33','35','36','37','39','41','42','43','44','46','47','49','55','57','58','63','71','74','78','82','87','99','117','124']
	diff_batch('/EQL1/NSL/clinical/trio_info.txt', tidL=tidL)
