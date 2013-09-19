"""A support module for representing a document in a retrieval system.
"""
from math import log
from nltk.probability import FreqDist
from nltk.tokenize import wordpunct_tokenize as wpt
from nltk.stem import PorterStemmer

import rlib


class Document(object):
    def __init__(self, title, raw, stopwords=set()):
        self.title = title
        self.raw = raw
        self.stops = stopwords
        self.docid = 0
        self.tokens = self._tokenize()
        self.stemmer = PorterStemmer()
        self.terms = self._get_terms()
        self.log_terms = self._log_terms()
        self.magnitude = 0
    
    def _tokenize(self):
        """Takes the raw terms and returns the tokenized contents"""
        return wpt(self.raw)
                
    def _get_terms(self):
        """Gets a freqdist of the standardized terms from the list of tokens
        Developer's note: this is where I would put stopwords
        """
        stems = []
        for token in self.tokens:
            if (not token.isalnum()) or (token in self.stops) or (token.isdigit()):
                continue
            stemmed = self.stemmer.stem(token)
            stems.append(stemmed.lower())
        return FreqDist(stems)
    
    def _log_terms(self):
        return dict((term, (1+log(freq, 2))) for term, freq in self.terms.items())
    
    def __len__(self):
        """This returns the number of terms in the document. NOT the size of it.
        """
        return len(self.terms)

def get_docs(compilation, stopwords=set()):
    """Takes in a compilation (i.e. sgm file) and outputs a list of documents from that file.
    """
    l_article = rlib.read_rfile(compilation)
    trees = []
    file_docs = []
    for article in l_article:
        clean = article.lstrip()
        if clean[:4] == "<REU":
            trees.append(rlib.xml_tree(clean))
    for tree in trees:
#        try:
#            news_id = tree.attrib['NEWID']
#        except:
#            news_id = ""
        try:
            title = tree.find('.//TITLE').text
        except:
            title = ""
        try:
            body = tree.find('.//BODY').text
        except:
            body = ""
        
        file_docs.append(Document(title, body, stopwords))
        
    return file_docs
        
