"""Back end of the ranked retrieval querying"""
from __future__ import division
from collections import defaultdict
from math import log, sqrt

from ir_objs_stops import *


def rank_query(query_doc, term_dict, docs_list):
    """Ranks the query (in the form of a Document) against the docs_list
    (according to the term_dict).

    @return: originally a dict of matched docs whose keys are titles, and
    values the input argument for more_like_this() function,
    but instead is currently a sorted list of (score, docid) tuples    
    """
    docs_from_query = set()
    query_tf_idfs = {}
    doc_tf_idfs = defaultdict(dict)
    scores = defaultdict(float)
    magnitude = defaultdict(float)

    #First, go through the query to collect all the related documents
    #and get the appropriate tf-idfs.    
    for term, freq in query_doc.terms.items():
        if not term in term_dict:
            continue
        docs_from_query.update(term_dict[term])
        query_tf_idfs[term] = 0 if freq <= 0 else (1+log(freq, 2))*log((len(docs_list)/len(term_dict[term])), 2)
    
    docs_from_query.discard("0")
    #Now that we have all the related documents and query tf-idfs, we can score the documents
    for doc in docs_from_query:
        for term in query_doc.terms.keys():
            freq = docs_list[doc].terms[term]
            doc_tf_idfs[str(doc)][term] = 0 if freq <= 0 else (1+log(freq, 2))*log((len(docs_list)/len(term_dict[term])), 2)
            scores[str(doc)] += query_tf_idfs[term] * doc_tf_idfs[str(doc)][term]
    
    #Finally we need the normalization factor
#    for all_term in term_dict.keys():
#        for doc in docs_from_query:
#            freq = docs_list[doc].terms[all_term]
#            magnitude[str(doc)] += 0 if freq <= 0 else ((1+log(freq, 2))*log((len(docs_list)/len(term_dict[all_term])), 2)) ** 2
            
    return sorted([((scores[str(doc)]/sqrt(docs_list[str(doc)].magnitude)), doc) for doc in docs_from_query], reverse=True)
