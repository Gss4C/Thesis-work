from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from tabulate import tabulate
import ROOT

file_ss = ROOT.TFile("/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/tDM_mPhi1000_mChi1_Skim_Sk\
im.root", "Open")
tree_ss = file_ss.Events

boost_w_fj  = 0
boost_wo_fj = 0
res_w_fj    = 0
res_wo_fj   = 0

for event in range(tree_ss.GetEntries()):
    
    tree_ss.GetEntry(event)
    jets   = Collection(tree_ss, "Jet")
    #TR     = Collection(tree_ss, "TopRes")
    BST    = False
    RSL    = False
    is_fwd = False

    if(tree_ss.Boosted):
        BST = True
    if(tree_ss.Resolved and not tree_ss.Boosted):
        RSL = True

    for jet in jets:
        if jet.isForward and jet.isGood:
            is_fwd = True
    ## Counting ##
    if BST:
        if is_fwd:
            boost_w_fj  += 1
        else:
            boost_wo_fj += 1
    if RSL:
        if is_fwd:
            res_w_fj  += 1
        else:
            res_wo_fj += 1

print(tabulate([['Forward', boost_w_fj, res_w_fj], ['Not Forward', boost_wo_fj, res_wo_fj]], 
               headers=['Boosted', 'Resolved']))

print("n boost with forward jets= ", boost_w_fj)
print("n boost without forward jets=", boost_wo_fj)
print("n resolved with forward jets=", res_w_fj)
print("n resolved without forward jets=", res_wo_fj)
