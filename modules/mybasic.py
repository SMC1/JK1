import types, string, bisect

def parseParam(optL):

	h = {}

	for (k,v) in optL:
		h[k] = v

	return h

def incHash(h,key,val=1):

	### incHash: fewfwef

	try:
		h[key] += val
	except:
		h[key] = val


def addHash(h,key,val):

	try:
		h[key].append(val)
	except:
		h[key] = [val]


def pushHash(h,key,val):

	try:
		h[key].add(val)
	except:
		h[key] = set([val])


def rev(seq):

	if not isinstance(seq,types.StringType):
		print "error: string type required!"
		print type(seq)
		sys.exit(1)

	seq_rev = ""

	for i in range(0,len(seq)):
		seq_rev = seq[i] + seq_rev

	return seq_rev


def compl(seq, seqType):

	if not isinstance(seq,types.StringType):
		print "error in mybio.compl: string type required!"
		print "you entered:%s" % (seq,)
		print type(seq)
		sys.exit(1)

	seq_ret = seq.upper()

	if seqType == 'RNA':
		tab = string.maketrans('ATUGCRYSW-','UAACGYRSW-')
	else:
		tab = string.maketrans('ATUGCRYSW-','TAACGYRSW-')
	
	seq_ret = seq_ret.translate(tab)

	return seq_ret


def rc(seq,type='DNA'):

	if not isinstance(seq,types.StringType):
		print "error: string type required!"
		sys.exit(1)

	seq = rev(seq)
	seq = compl(seq,type)

	return seq


def parse_vcf_info(tag):
	termL = tag.split(';')
	infoH = {}
	for term in termL:
		if '=' in term:
			[key,val] = term.split('=')
			infoH[key] = val
		else:
			infoH[key] = True
	return(infoH)

def left_align_var(chrom,pos,ref,alt):
	len_tail = -1 * min(len(ref)-1, len(alt)-1)
	if alt[0]==ref[0] and alt[len_tail:] == ref[len_tail:]:
		alt = alt[:len_tail]
		ref = ref[:len_tail]
		return (chrom,pos,ref,alt)

	if len(ref)==len(alt) and ref[:-1]==alt[:-1]:
		pos = pos + len(ref) - 1
		ref = ref[-1:]
		alt = alt[-1:]
		return (chrom,pos,ref,alt)

	max_n = min(len(ref), len(alt))
	for i in range(max_n,0,-1):
		if alt[:i] == ref[:i]:
			alt = alt[(i-1):]
			ref = ref[(i-1):]
			pos = pos + i - 1
			return (chrom,pos,ref,alt)

	#otherwise, do nothing
	return (chrom,pos,ref,alt)

def index(a, x): ## a: sorted number array
	## locate leftmost value exactly equal to x
	i = bisect.bisect_left(a, x)
	if i != len(a) and a[i] == x:
		return i
	return -1
