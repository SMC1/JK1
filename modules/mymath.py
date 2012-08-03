# mymath

import numpy

def deviation(data,option='median'):

	if option=='mean':
		m = float(numpy.mean(data))
	elif option=='median':
		m = float(numpy.median(data))
	else:
		raise Exception

	results = []

	for d in data:
		results.append(d-m)

	return results


def mad(data): # median absolute deviation

	return numpy.median(map(abs,deviation(data,'median')))
