#!/usr/bin/python2.5
 
#Copyright(c)2008 Internet Archive. Software license GPL version 3.
 
# This script downloads the OCR results for the Internet Archive's 
# Bioversity Heritage Library collection. It is meant to show you how to 
# download large datasets from archive.org.
 
# The csv file that drives the downloader can be fetched using the url below. 
# Change the collection parameter in the url to americana or toronto to get the
# bulk of the Internet Archive's scanned books. The advanced search page
# can help you tune the query string for accessing the rest of the collection:
# http://www.archive.org/advancedsearch.php
 
# Multiple downloaders can be run at the same time using the startnum and endnum
# parameters, which will help to speed up the download process.

# Script updated by Luis Aguilar to support file transformations during the download process
 
import csv
import glob
import os
import codecs
import commands
import sys
import StringIO
import requests
from lxml import etree

#download biodiveristy.csv with
#wget 'http://www.archive.org/advancedsearch.php?q=collection%3A%28biodiversity%29+AND+format%3A%28djvu+xml%29&fl%5B%5D=identifier&rows=1000000&fmt=csv&xmlsearch=Search'

# load global file object
csvfile_list = glob.glob('load/*.csv')
reader = csv.reader(open(csvfile_list[0], "rb"))

# load global file transformer
xslt_path = "config/DjVuToCRML.xsl"
djvuToOcr_xsl = open(xslt_path, "r")

# METHOD that uses global xslt to transform djvu xml to ocrml format
def convertDjvuToOcrXML(djvu, path, id):
    djvu_path = "%s/%s_djvu.xml"%(path, id)
    djvu_file = codecs.open(djvu_path, "w", 'utf-8')
    #djvu_file = open(djvu_path, "w")
    ocrml_path = "%s/%s_ocrml.xml"%(path, id)
    ocrml_file = codecs.open(ocrml_path, "w", 'utf-8')
    try:
        #xslt_xml = etree.XML(djvuToOcr_xsl.read())
        xslt_xml = etree.parse(xslt_path)
        transform = etree.XSLT(xslt_xml)
        djvu_xml = etree.XML(djvu)
        # file should already be XML unicode
        djvu_file.write(etree.tostring(djvu_xml, pretty_print=False, encoding=unicode))
        #djvu_file.write(etree.tostring(djvu_xml, pretty_print=False))

        #print str(transform(djvu_xml))
        #djvu_xml = etree.parse(StringIO.StringIO(djvu))
        #djvu_xml = etree.tostring(djvu, encoding='UTF-8')
        ocrml = transform(djvu_xml)
        ocrml_file.write(unicode(ocrml))
    finally:
        djvuToOcr_xsl.close()
        djvu_file.close()
        ocrml_file.close()
    
#MAIN
startnum = 0
#endnum   = 999999
endnum = 2

# the first row is a header
reader.next()

# if you start at somewhere other than the beginning of the csv file, 
#move forward to that startnum 
for i in range(startnum):
    reader.next()

filenum = startnum
 
for row in reader:
    id = row[0]
    dirnum = "%09d" % filenum
    
    print "downloading file #%s, id=%s" % (dirnum, id)
 
    #place 1000 items per directory
    assert filenum<1000000
    parentdir = dirnum[0:3]
    subdir    = dirnum[3:6]
    path = '%s/%s' % (parentdir, subdir)
 
    if not os.path.exists(path):
        os.makedirs(path)

    url = "http://www.archive.org/download/%s/%s_djvu.xml" % (id, id)
    dlpath = "%s/%s_djvu.xml"%(path, id)
 
    if not os.path.exists(dlpath):
        #urllib.urlretrieve(url, dlpath)
        #use rate limiting to be nicer to the cluster
        #(status, output) = commands.getstatusoutput("""wget '%s' -O '%s' --limit-rate=250k --user-agent='IA Bulk Download Script' -q""" % (url, dlpath))
        #assert 0 == status
        
        # new code to download file and hold it for transform
        r = requests.get(url)
        assert r.status_code == 200
                
        #if downloaded so i'll need a code here to call convert function, get it and transform it
        convertDjvuToOcrXML(djvu=r.content, path=path, id=id);
    else:
        print "\talready downloaded, skipping..."
 
    filenum+=1
    if (filenum > endnum):
        sys.exit()
