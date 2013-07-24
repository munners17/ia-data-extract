#! /usr/bin/python

""" Djvu XML to OCRML converter

	A Python utility to transform files
"""

__author__ = "Luis Aguilar"
__email__ = "luis@berkeley.edu"
 
from optparse import OptionParser
import csv
import glob
import pdb
import os
import codecs
import commands
import sys
import StringIO
import requests
from lxml import etree

# initializing global transformer, surround around try/catch or accept as parameter?
transform = etree.XSLT(etree.parse('config/DjVuToCRML.xsl'))

def processDirectory(dir_path):
    """ Process the input directory

	    Process only djvu files that have not been transformed from
	    directory path parameter.
    """
    # extract absolute path from user submitted path value, should put try/catch
    abs_path = os.path.abspath(dir_path)
    # loop through and open/transform djvu files
    for filename in os.listdir(abs_path):
        # establish file path for ocrml file
        ocrml_path = abs_path + '/' + filename.replace('djvu', 'ocrml')
        # only process and create ocrml file if it doesn't already exist
        if filename.endswith("djvu.xml") and not os.path.isfile(ocrml_path):
            _transformDjvu(abs_path, filename, ocrml_path)

def _transformDjvu(abs_path, filename, ocrml_path):
    global transform
    djvu_path = abs_path + '/' + filename
    try:
        f_djvu = codecs.open(djvu_path, "r", 'utf-8')
        f_ocrml = codecs.open(ocrml_path, "w", 'utf-8')
        # check for proper utf character sets
        djvu_xml = etree.XML(f_djvu.read())
        ocrml = transform(djvu_xml)
        f_ocrml.write(unicode(ocrml))
    finally:
        # close the source djvu and destination ocrml files
        f_djvu.close()
        f_ocrml.close()

def _getInput():
    """ Command Line Input Parsing

	    Parse the user input
    """
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='filepath', default='.')
    (option, args) = parser.parse_args()

    if not option.filepath:
	    return parser.error('Djvu file path not given, use --input="path.to.djvu.file.for.download"')

    return {'src': option.filepath}

def main():
    userInput = _getInput()
    processDirectory(userInput['src'])
    # close the transform global?

if __name__ == '__main__':
	main()
