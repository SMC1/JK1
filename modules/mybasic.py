import types, string

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



