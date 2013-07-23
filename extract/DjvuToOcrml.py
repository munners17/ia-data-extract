#! /usr/bin/python

""" Djvu XML to OCRML converter

	A Python utility to transform files
"""

__author__ = "Luis Aguilar"
__email__ = "luis@berkeley.edu"
 
from optparse import OptionParser
import csv
import glob
import os
import codecs
import commands
import sys
import StringIO
import requests
from lxml import etree

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

def purgatory():
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

def getInput():
	""" Command Line Input Parsing

		Parse the user input
	"""
	parser = OptionParser()
	parser.add_option('-i', '--input', dest='filepath', default='.')
	(option, args) = parser.parse_args()

	if not option.filepath:
		return parser.error('Djvu file path not given, use --input="path.to.djvu.file.for.download"')

	return {'src': option.filepath}

def processDnldList(path):
    ocrml_file = codecs.open(ocrml_path, "w", 'utf-8')
    
    for i in os.listdir(path):
        if i.endswith("djvu.xml"): 
            print i

def main():
	userInput = getInput()
	processDnldList(userInput['src'])
	#initDnld(dnldList, userInput['utility'])


if __name__ == '__main__':
	main()
