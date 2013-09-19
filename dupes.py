"""For deleting duplicates in the index
UNFINISHED (or run in interactive mode and do the rest manually)
"""
import shelve, os

import ir_objs_stops

if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.realpath("__file__"))
    par_dir = os.path.abspath(os.path.join(this_dir, os.pardir))
    docs_shelf = shelve.open(os.path.join(par_dir, "doc_stops"))

    docs_list = sorted([(doc.title, docnum) for (docnum, doc) in docs_shelf.items()])
