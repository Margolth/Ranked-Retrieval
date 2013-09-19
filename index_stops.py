"""This module builds an index from the indicated directory.  The
directory must be in a similar format to the Reuters database (which
this program was designed for).
"""
from __future__ import division
import sys
import glob
import os
import shelve
from collections import defaultdict
from math import log, sqrt

from ir_objs_stops import *

if len(sys.argv) != 4:
    sys.exit("usage: index.py [source_folder] [term_shelf] [doc_shelf]")

source_folder = sys.argv[1]
##sgm_file = sys.argv[1]
terms_file = sys.argv[2]
docs_file = sys.argv[3]
print "Retrieving files..."
sgms = glob.glob(os.path.join(source_folder, "*.sgm"))
terms = shelve.open(terms_file, writeback=True)
all_docs = shelve.open(docs_file, writeback=True)
docnum = len(all_docs) + 1
try:
    stops = terms["STOPWORDS"]
except KeyError:
    answer =  raw_input("Stopwords not found, continue without stopwords (y/n)?")
    if answer.lower() in "no":
        sys.exit("So sorry, better luck next time!")
print "Getting documents..."
for sgm_file in sgms:
    docs = get_docs(sgm_file, stops)
    for doc in docs:
        doc.docid = docnum
        all_docs[str(docnum)] = doc
        for term in doc.terms.keys():
            if not term in terms:
                terms[term] = set(str(docnum))
            terms[term].add(str(docnum))
        docnum += 1

print "Getting normalization factors..."
#Calculate and store the normalization factor for the new documents
for all_term in terms.keys():
    if all_term.isupper():
        continue
    for doc in docs:
        freq = all_docs[str(doc.docid)].terms[all_term]
        all_docs[str(doc.docid)].magnitude += 0 if freq <= 0 else ((1+log(freq, 2))*log((len(all_docs)/len(terms[all_term])), 2)) ** 2
        
#store = open(pickle_file, 'wb')
#cPickle.dump(all_docs, store)
#store.close()
terms.close()
all_docs.close()
print "done."
