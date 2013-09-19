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

print "Retrieving files..."
this_dir = os.path.dirname(os.path.realpath("__file__"))
terms = shelve.open(os.path.join(this_dir, "postings_stops"))
docs_list = shelve.open(os.path.join(this_dir, "doc_stops"), writeback=True)
##docnum = len(docs_list) + 1

print "Getting normalization factors..."
#Calculate and store the normalization factor for the new documents

for doc in docs_list.keys():
    for all_term in docs_list[doc].terms.keys():
        if len(docs_list[doc].terms) == 0:
            print doc + " has no terms."
        elif docs_list[doc].magnitude == 0:
            log_freq = docs_list[doc].log_terms[all_term]
            docs_list[doc].magnitude += 0 if docs_list[doc].terms[all_term] <= 0 else log_freq*log((len(docs_list)/len(terms[all_term])), 2) ** 2

#store = open(pickle_file, 'wb')
#cPickle.dump(all_docs, store)
#store.close()
terms.close()
docs_list.close()
print "done."
