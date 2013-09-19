"""This program is designed to go along with the ranked retrieval
program by Theo Margolis.

Adds the given word to the stopwords incorporated in the
associated index.
"""
import os
import shelve

this_dir = os.path.dirname(os.path.realpath("__file__"))
terms = shelve.open(os.path.join(this_dir, "postings_stops"))
stops = terms["STOPWORDS"]
stopset = set(stops)

stopset.add(raw_input("Word to add: "))

terms["STOPWORDS"] = frozenset(stopset)
terms.close()
print "Word added."
