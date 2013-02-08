#!/usr/bin/python

import sys, getopt
import mybasic, mymysql


def main(geneN):

	(con,cursor) = mymysql.connectDB()

	cursor.execute('select samp_id,z_score from array_gene_expr where gene_sym=%s order by z_score desc', geneN)

	results = cursor.fetchall()

	f = sys.stdout

	f.write('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Untitled Document</title>
<style type="text/css">
.verticaltext{
-webkit-transform:rotate(-90deg); writing-mode:tb-rl; -moz-transform:rotate(90deg); -o-transform: rotate(90deg); white-space:nowrap; display:blocking; padding-left:1px;padding-right:1px;padding-top:10px;padding-bottom:10px;
}
</style>
</head>
<body>
''')

	f.write('<div class="verticaltext">test</div>')

	f.write('\n<table>\n')

	f.write('\n<tr>\n<th></th>')

	for row in results:
		f.write('<th><div class="verticaltext">%s</div></th>' % row[0])

	f.write('\n</tr>\n')

	f.write('\n<tr>\n<td>%s</td>' % geneN)

	for row in results:
		f.write('<td>%.1f</td>' % row[1])

	f.write('\n</tr>\n')

	f.write('\n</table>\n')

	f.write('''
</body>
</html>''')

optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], optH['-o'])

main('EGFR')
