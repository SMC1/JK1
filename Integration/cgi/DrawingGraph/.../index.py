#!/usr/bin/python

import cgi

print "Content-type: text/html\r\n\r\n";

print '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>FIXME</title>
<!--
<link rel="stylesheet" type="text/css" href="FIXME" />
<script type="text/javascript" src="FIXME"></script>
<style type="text/css">
/* <![CDATA[ */
/* ]]> */
</style>
-->
</head>
<body>

     <form method='get' action='Main.py'>
        <select name='dbN'>
            <option value ='ircr1' name='dbN'>IRCR GBM</option>
            <option value ='tcga1' name='dbN'>TCGA GBM</option>
            <option value ='ccle1' name='dbN'>CCLE</option>
        </select>
        <input type='text' name='geneN'>
        <input type='text' name='items'>
        <input type='submit' value='Submit'>
    </form>

    <div id="oncoprint"></div>

</body>
<script type="text/javascript" src="/js/d3.v2.min.js"></script>
<script src="/js/jquery.min.js"></script>
<script src="/js/jquery-ui-1.8.14.custom.min.js"></script>
<script src="/js/MemoSort.js"></script>
<script src="/js/oncoprint.js"></script>
<script src="/js/QueryGeneData.js"></script>
<script src="/js/oncoprint_demo.js"></script>
</html> '''
