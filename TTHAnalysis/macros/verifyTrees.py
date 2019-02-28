import ROOT
import os, sys

from ROOT import gROOT
# this script can be used to verify that a friend tree has the same number of entries as the main tree
# (useful to check that all chunks in the friend tree production have been done successfully)
#
# usage: python verifyFTree BIGTREE_DIR DATASET_NAME ...

import signal

def sig_handler(signum, frame):
    #deal with the signal.. 
    print "segfault"
signal.signal(signal.SIGSEGV, sig_handler)  

dsets = sys.argv[2:]
if len(sys.argv)<3:
    dsets = [d.replace('evVarFriend_','').replace('.root','') for d in os.listdir(sys.argv[1]) if ('evVarFriend' in d and 'chunk' not in d)]

import subprocess as sp

for dset in dsets:
    p = sp.Popen(["python", "verifyTree.py", dset], stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = p.communicate()
    result = p.returncode
    print result
    print '%s: %s'%(dset,'OK' if result==0 else 'ERROR '*15+' !!!')    
    
#    print '%s: %d - %d : %s'%(dset,n_t,n_f,'OK' if n_t==n_f else 'ERROR '*15+' !!!')

