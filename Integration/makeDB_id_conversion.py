#!/usr/bin/python

import mymysql

#mymysql.reset_table('id_conversion', '/EQL1/NSL/clinical/id_conversion_20141027.dat', user='cancer', passwd='cancer', db='ircr1', host='localhost')
mymysql.reset_table('id_conversion', '/EQL1/NSL/clinical/id_conversion_20150310.dat', user='cancer', passwd='cancer', db='ircr1', host='localhost')
