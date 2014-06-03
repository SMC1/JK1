#!/usr/bin/python

import mygsnap, re, getopt, mybasic
import sys, os

def make_header(chromFile):
	chrD = {}
	ifile = open(chromFile)
	for line in ifile.readlines():
		cols = line[:-1].rstrip().split('\t')
		chrD[cols[0]] = cols[1]
	ifile.close()

	header = []
	for i in range(1,23):
		header.append('@SQ\tSN:chr%s\tLN:%s' % (i, chrD['chr' + str(i)]))
	for i in ['M', 'X', 'Y']:
		header.append('@SQ\tSN:chr%s\tLN:%s' % (i, chrD['chr' + i]))

	return header

def make_samse(ifileN, ofileN):

	headerL = make_header('/data1/Sequence/ucsc_hg19/hg19.chrom.sizes')
#	ofile = open(ofileN, 'w')
	for header in headerL:
		print header
#		ofile.write('%s\n' % header)

	result = mygsnap.gsnapFile('/pipeline/test_ini_gsnap2sam/S022_single.gsnap',False)
	#result = mygsnap.gsnapFile('/pipeline/test_ini_gsnap2sam/test.gsnap',False)
	#result = mygsnap.gsnapFile('/pipeline/test_ini_gsnap2sam/S022_pair.gsnap',True)

	## for unpaired
	for r in result:

		qname = r.rid()
		flag = 0x0
		rname = '*'
		pos = 0
		mapq = 0
		cigar = ''
		rnext = '*' ## assume --npath=1 (maximum 1 alignment per read)
		pnext = 0 ## assume --npath=1 (maximum 1 alignment per read)
		tlen = 0  ## assume --npath=1 (maximum 1 alignment per read)
		seq = r.seq()
		qual = r.qual()
		extra = 'NH:i:1\tHI:i:1' ## assume --npath=1 (maximum 1 alignment per read)

		if r.nLoci > 1:
			flag = flag | 0x4
			cigar = '*'
			new_cigar = '*'
			extra = ''
			print ('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (qname, flag, rname, pos, mapq, new_cigar, rnext, pnext, tlen, seq, qual, extra))
		else:
			if r.pairRel == '(transloc)':
				match = r.matchL()[0]
				segL = match.getSegInfo()
				mapq = segL[0].mapq
				seq = r.seq()
				qual = r.qual()
				for seg in segL:
					flag = 0x0
					(strand, rname, pos1, pos2) = re.search('([\+\-])(.*):([0-9]+)\.\.([0-9]+)', seg.seg[2]).groups()
					pos = min(int(pos1), int(pos2))
					(cigar,clip) = seg.toCIGAR_trans()
					if clip < 0: ## first half
						seq2 = seq[:clip]
						qual2 = qual[:clip]
					else: ## second half
						seq2 = seq[clip:]
						qual2 = qual[clip:]
					if strand == '-':
						flag = flag | 0x10
						seq2 = mybasic.rc(seq2)
						qual2 = mybasic.rev(qual2)
#					print qname,seg.toCIGAR_trans()
					print ('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (qname, flag, rname, pos, mapq, cigar, rnext, pnext, tlen, seq2, qual2, extra))
			else:
				match = r.matchL()[0] ## assume --npath=1 (maximum 1 alignment per read)

				segL = match.getSegInfo()
				(strand, rname, pos1, pos2) = re.search('([\+\-])(.*):([0-9]+)\.\.([0-9]+)', segL[0].seg[2]).groups()
				pos = min(int(pos1), int(pos2))
				mapq = segL[0].mapq
				seg_nm = segL[0].numSub
				cigar2 = match.toCIGAR()
#				print qname, match.toCIGAR()

				if segL[0].start != '' and segL[0].start != '0':
					cigar = str(segL[0].start) + 'S'

				if strand == '-':
					cigar = str(segL[0].numMatch + segL[0].numSub) + 'M' + cigar
					if segL[0].ins != '' and segL[0].ins != '0':
						cigar = str(segL[0].ins) + 'I' + cigar
				else:
					cigar = cigar + str(segL[0].numMatch + segL[0].numSub) + 'M'
					if segL[0].ins != '' and segL[0].ins != '0':
						cigar = cigar + str(segL[0].ins) + 'I'

				if len(segL) == 1:
					new_cigar = segL[0].toCIGAR(True)
				else:
					new_cigar = segL[0].toCIGAR()
				prev_cigar = new_cigar
				index = 0
				for seg in segL[1:]:
					index = index + 1
					if index == (len(segL) - 1):
						final = True
					else:
						final = False
					rm = re.search('([\+\-])(.*):([0-9]+)\.\.([0-9]+)', seg.seg[2]).groups()

					match = str(seg.numMatch + seg.numSub) + 'M'

					if seg.ins != '' and seg.ins != '0':
						ins = str(seg.ins) + 'I'
					else:
						ins = ''

					if pos == 0 or pos > min(int(rm[2]), int(rm[3])):
						pos = min(int(rm[2]), int(rm[3]))
					if strand == '-':
						dist = int(pos2) - int(rm[2]) - 1
						if dist > 0:
							cigar = match + ins + str(dist) + 'N' + cigar
						else:
							cigar = match + ins + cigar
					else:
						dist = int(rm[2]) - int(pos2) - 1
						if dist > 0:
							cigar = cigar + str(dist) + 'N' + match + ins
						else:
							cigar = cigar + match + ins
					seg_nm = seg_nm + seg.numSub
					pos1 = rm[2]
					pos2 = rm[3]
					cur_cigar = seg.toCIGAR(final)
					if strand == '-':
						if dist > 0 and 'D' not in prev_cigar and 'I' not in prev_cigar:
							new_cigar = cur_cigar + str(dist) + 'N' + new_cigar
						else:
							new_cigar = cur_cigar + new_cigar
					else:
						if dist > 0 and 'D' not in prev_cigar and 'I' not in prev_cigar:
							new_cigar = new_cigar + str(dist) + 'N' + cur_cigar
						else:
							new_cigar = new_cigar + cur_cigar
					prev_cigar = cur_cigar

				if segL[-1].end != '' and segL[-1].end != '0': ## last segment
					if strand == '-':
						cigar = str(segL[-1].end) + 'S' + cigar
					else:
						cigar = cigar + str(segL[-1].end) + 'S'

				extra = extra + ('\tNM:i:%s' % seg_nm)

				if strand == '-':
					flag = flag | 0x10
					seq = mybasic.rc(seq)
					qual = mybasic.rev(qual)

##			print ('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (qname, flag, rname, pos, mapq, cigar, rnext, pnext, tlen, seq, qual, extra))
				print ('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (qname, flag, rname, pos, mapq, cigar2, rnext, pnext, tlen, seq, qual, extra))
#			for line in os.popen('grep -F -w %s /pipeline/test_ini_gsnap2sam/S022_single.sam | cut -f 6' % qname).readlines():
#				print line.rstrip()
#			print ''
#		org_cigars = os.popen('grep -F -w %s /pipeline/test_ini_gsnap2sam/S022_single.sam | cut -f 6' % qname).readlines()
#		org_cigar = map(lambda x: x.rstrip(), org_cigars)
#		if new_cigar not in org_cigar:
#			print qname, new_cigar, org_cigar

def make_sampe(ifile, ofile):
	pass

if __name__ == '__main__':
	make_samse('hhhh', 'oooo')

#	optL, argL = getopt.getopt(sys.argv[1:], 'i:o:', ['paired'])
#	optH = mybasic.parseParam(optL)

#	if '--paired' in optH:
#		make_sampe(optH['-i'], optH['-o'])
#	else:
#		pass
#		make_samse(optH['-i'], optH['-o'])
