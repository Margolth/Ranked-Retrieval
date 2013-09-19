# Sample code for converting Reuters 21578 .sgm files into xml element trees 
# using lxml etree module in python

import re
import StringIO
from xml.etree.ElementTree import ElementTree

# regular expressions matching illegal strings:
# matches strings of the form "&#3;"
re_amp = re.compile("&#[0123456789]+;")

# reads in a reuters.sgm file
# returns a list of articles (each is a long string including newline chars but missing the final </REUTERS> tag
# used as a separator string for articles)
def read_rfile(rfile):
    s_rfile = open(rfile)
    # first line just refers to the DTD file
    dtd = s_rfile.readline()
    # remaining lines are multiple reuters articles with <REUTERS ...  as the root tag
    rfile_string = s_rfile.read()
    l_article = rfile_string.split("</REUTERS>")
    
    s_rfile.close()
    return(l_article)

# xml_tree should be run on every article string produced by read_rfile
# it removes bad characters and replaces the final tag.
# It returns an element tree that can be manipulated by the etree methods
def xml_tree(raw):
    clean = re.sub(re_amp, "", raw)
    # restore the closing tag we removed during the split
    clean = clean + "</REUTERS>\n"
    tree = ElementTree().parse(StringIO.StringIO(clean))
    return(tree)

# test the code on a small subset of a reuters file
def test_rfile():
    rfile = "test.sgm"
    #rfile = "reut2-000.sgm"
    l_article = read_rfile(rfile)
    print "Length of article list: %i" % len(l_article)
    l_tree = []
    for article in l_article:
        article = article.lstrip()
        if article[0:4] == "<REU":
            l_tree.append(xml_tree(article))

    n = 1
    for tree in l_tree:
        # example of pretty printing entire xml tree
        print etree.tostring(tree, pretty_print=True)
        print "\n\n"
        try:
            # example of getting an attribute of the root element
            docid = tree.getroot().get('NEWID')
        except:
            print "ERROR: no docid for article: %i" % n
            docid = "0"
        try:
            # example of getting the text for an element tag that occurs once
            # somewhere in the tree
            title = tree.find('.//TITLE').text
        except:
            title = ""
        try:
            body = tree.find('.//BODY').text
        except:
            body = ""
        print "DOC: %s" % docid
        print "TITLE: %s" % title
        print "BODY: %s" % body
        
        n += 1
    return(l_tree)



