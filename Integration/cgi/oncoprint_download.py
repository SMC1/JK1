#!/usr/bin/python

import cgi, sys

form = cgi.FieldStorage()
xml_value = form.getvalue("xml")
svg_file = open("/var/www/html/tmp/oncoprint_converter.svg", "w")
svg_file.write(xml_value)
svg_file.close()

print 'Content-Disposition: attachment; filename="oncoprint.svg"\r\n\r\n';

download_file = open("/var/www/html/tmp/oncoprint_converter.svg", "r")

for s in download_file.readlines():
	print s

download_file.flush()
download_file.close()
