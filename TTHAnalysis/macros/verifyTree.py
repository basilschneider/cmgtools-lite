import ROOT
import os, sys

from ROOT import gROOT
# this script can be used to verify that a friend tree has the same number of entries as the main tree
# (useful to check that all chunks in the friend tree production have been done successfully)
#
# usage: python verifyFTree BIGTREE_DIR DATASET_NAME ...

def openRootOrUrl(myfile):
    _f_t = None
    if os.path.exists(myfile):
        _f_t = ROOT.TFile.Open(myfile)
    elif os.path.exists(myfile+'.url'):
        with open(myfile+'.url','r') as urlf:
            myfile = urlf.readline().replace('\n','')
            if myfile.startswith("root://"):
                _f_t = ROOT.TXNetFile(myfile)
            else:
                _f_t = ROOT.TFile.Open(myfile)
    return _f_t


def checkDset(dset):
    print "running " + dset
    f_t = openRootOrUrl(sys.argv[1]+'/'+dset+'/treeProducerSusyMultilepton/tree.root')
    t_t= None
    n_t = 0
    try:
        t_t = f_t.Get("tree")
        n_t = t_t.GetEntries()
    except Exception:
        print '%s: %s'%(dset, 'ERROR, tree not found '*15+' !!!')
    t_t.MakeClass('myClassT')
    gROOT.LoadMacro("myClassT.C+")
    from ROOT import myClassT
    m_t = myClassT()
    for i in range(n_t,100):
        m_t.GetEntry(i)
    f_t.Close()

if name == "__main__":
    import sys
    dset = read_args()
    sys.exit(checkDset(dset))
