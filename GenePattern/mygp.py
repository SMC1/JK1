def parseParam(optL):

	h = {}

	for (k,v) in optL:
		h[k] = v

	return h


def stripPath(path):

	tmp = path.split('/')[-1].split('att_')[-1]

	rIdx = tmp.rfind('.')

	if rIdx != -1:
		return (tmp[:rIdx], tmp[rIdx+1:])
	else:
		return (tmp, '')
