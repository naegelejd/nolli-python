from __future__ import print_function
import sys

def debug(msg):
    print("(parser): %s" % msg, file=sys.stderr)

def error(msg):
    print("ERROR! (parser): %s" % msg, file=sys.stderr)
