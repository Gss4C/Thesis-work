from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT

file_s = ROOT.TFile("/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/tDM_mPhi1000_mChi1_Skim.root", "Open")
tree_s = file_s.Events
#/home/iorio/public/tDM/tDM_mPhi1000_mChi1.root

boost_w_fj  = 0
boost_wo_fj = 0
res_w_fj    = 0
res_wo_fj   = 0

for event in range(tree_s.GetEntries()):
    
    tree_s.GetEntry(event)
    jets   = Collection(tree_s, "Jet")
    #TR     = Collection(tree_s, "TopRes")
    BST    = False
    RSL    = False
    is_fwd = False

    if(tree_s.Boosted):
        BST = True
    if(tree_s.Resolved and not tree_s.Boosted):
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

print("boost with forward jets=      ", float(boost_w_fj)/1000 )
print("boost without forward jets=   ", float(boost_wo_fj)/1000)
print("resolved with forward jets=   ", float(res_w_fj)/1000   )
print("resolved without forward jets=", float(res_wo_fj)/1000  )
