#!/usr/bin/python

import getopt, sys
import mybasic

def split(optionH):
	if '-s' in optionH:
		if '-g' in optionH:
			write_both(optionH['-s'], optionH['-g'])
		else:
			write_sam_only(optionH['-s'])
	else:
		if '-g' in optionH:
			write_gsnap_only(optionH['-g'])

def write_both(samFile, gsnapFile):
	if samFile == '':
		samOut = sys.stdout
	else:
		samOut = open(samFile, 'w')
	gsnapOut = open(gsnapFile, 'w')
	for line in sys.stdin:
		if line[0] == '@':
			samOut.write('%s' % line)
		elif line[0] == '#':
			samOut.write('%s' % line[1:])
		else:
			gsnapOut.write('%s' % line)
	samOut.flush()
	samOut.close()
	gsnapOut.flush()
	gsnapOut.close()

def write_sam_only(samFile):
	if samFile == '':
		samOut = sys.stdout
	else:
		samOut = open(samFile, 'w')
	for line in sys.stdin:
		if line[0] == '@':
			samOut.write('%s' % line)
		elif line[0] == '#':
			samOut.write('%s' % line[1:])
	samOut.flush()
	samOut.close()

def write_gsnap_only(gsnapFile):
	gsnapOut = open(gsnapFile, 'w')
	for line in sys.stdin:
		if line[0] not in ['@', '#']:
			gsnapOut.write('%s' % line)
	gsnapOut.flush()
	gsnapOut.close()


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:], 'g:s', [])
	optH = mybasic.parseParam(optL)

	if '-s' in optH or '-g' in optH:
		split(optH)

