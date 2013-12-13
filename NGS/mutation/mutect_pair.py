#!/usr/bin/python

import sys, os, re, getopt
import mybasic

MINQ = 15 # minimum base quality score
MIN_T_FRAC = 0.01 # reject if allele fraction < 1% in tumor
MAX_N_READ = 5    # reject if alt read count > 5 in matched normal
MAX_N_FRAC = 0.05 # reject if allele fraction > 5% in matched normal

def main(tumorFileN, normalFileN, outDir, sampN, mem='8g', genome='hg19', pbs=False):
#	print 'Files for %s: %s, %s' % (outPrefix, tumorFileN, normalFileN)
	## command to make this file: b37_cosmic_v54_120711.vcf downloaded from muTect website,
	## awk 'OFS="\t" {if (substr($1, 1, 1)=="#") print $0; else print "chr"$0}' b37_cosmic_v54_120711.vcf > hg19_cosmic_v54_120711.vcf
	## or
	## using cosmic_confirmed_somatic_vxx.vcf generated by JK1/Integration/prepDB_cosmic_annotated.py
	## use fix_chr_cosmic.sh => produces cosmic_confirmed_somatic_vxx.hg19.vcf
	if genome == 'hg19':
		cosmic='/data1/Sequence/cosmic/hg19_cosmic_v54_120711.vcf'
		#cosmic='/data1/Sequence/cosmic/cosmic_confirmed_somatic_v63.hg19.vcf'
		dbsnp='/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'
		ref='/data1/Sequence/ucsc_hg19/hg19.fasta'

	mem_opt = '-Xmx%s' % mem

	outFileN = '%s/%s.mutect' % (outDir, sampN)
	cmd = 'java %s -jar /home/tools/muTect/muTect.jar --analysis_type MuTect --reference_sequence %s --cosmic %s --dbsnp %s' % (mem_opt, ref, cosmic, dbsnp)
	cmd = '%s --input_file:normal %s --input_file:tumor %s --out %s -dt NONE' % (cmd, normalFileN, tumorFileN, outFileN)
	cmd = '%s --tumor_f_pretest %s --min_qscore %s --max_alt_alleles_in_normal_count %s --max_alt_allele_in_normal_fraction %s -nt 10' % (cmd, MIN_T_FRAC, MINQ, MAX_N_READ, MAX_N_FRAC)
	cmd = '(echo "%s"; %s)' % (cmd, cmd)
	print cmd
	if pbs:
		os.system('echo "%s" | qsub -N mutect_%s -o %s.mutect.log' % (cmd, sampN, outDir+'/'+sampN))
	else:
		os.system('%s > %s.mutect.log' % (cmd, outDir+'/'+sampN))

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'t:n:o:s:g:m:p:',[])

	optH = mybasic.parseParam(optL)

	mem = ''
	if '-m' in optH: ## in Mb
		mem = optH['-m']

	pbsB = False
	if optH['-p'] in ['True', 'true']:
		pbsB = True

	if '-g' in optH:
		main(optH['-t'], optH['-n'], optH['-o'], optH['-s'], mem, optH['-g'], pbs=pbsB)
	else:
		main(optH['-t'], optH['-n'], optH['-o'], optH['-s'], mem, 'hg19', pbs=pbsB)

#main('/pipeline/test_ini_gsnap2sam/S022_single.dedup.rg.ra.rc.bam', '/pipeline/test_ini_gsnap2sam/aln/S022_Rsq.dedup.rg.ra.rc.bam', 'test', 50, 4)
#main(tumorFileN='/EQL3/pipeline/SGI20131119_xsq2mut/S14A_T_SS/S14A_T_SS.recal.bam', normalFileN='/EQL3/pipeline/SGI20131119_xsq2mut/S14C_B_SS/S14C_B_SS.recal.bam', outPrefix='S14A_T_SS', mem='10g', pbs=False)
