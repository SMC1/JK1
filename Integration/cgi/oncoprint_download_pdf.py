#!/usr/bin/python

import cgi, sys
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

form = cgi.FieldStorage()
xml_value = form.getvalue("xml2")
svg_file = open("/var/www/html/tmp/oncoprint_converter.svg", "w")
svg_file.write(xml_value)
svg_file.close()

print 'Content-Disposition: attachment; filename="oncoprint.pdf"\r\n\r\n';
#print 'Content-Type: application/pdf \r\n\r\n';

drawing = svg2rlg("/var/www/html/tmp/oncoprint_converter.svg")
renderPDF.drawToFile(drawing, "/var/www/html/tmp/oncoprint_converter.pdf")

download_file = open("/var/www/html/tmp/oncoprint_converter.pdf", "r").read()
print download_file

download_file.flush()
download_file.close()
