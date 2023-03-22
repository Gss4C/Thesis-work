from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT

file_ss = ROOT.TFile("/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/tDM_mPhi1000_mChi1_Skim_Sk\
im.root", "Open")
tree_ss = file_ss.Events

'''file_s  = ROOT.TFile("/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/tDM_mPhi1000_mChi1_Skim.ro\
ot", "Open")
tree_s  = file_s.Events

n_events_s  = float(tree_s.GetEntries())
n_events_ss = float(tree_ss.GetEntries())
e_cut_global = n_events_ss/n_events_s
print("Global veto efficiency: ", e_cut_global)'''

xor_boost   = 0
xor_res     = 0
boost_w_fj  = 0
boost_wo_fj = 0
res_w_fj    = 0
res_wo_fj   = 0

def xor_counting(tree):
    xor_boost = 0
    xor_res   = 0
    if(tree.Boosted and not(tree.Resolved)):
        xor_boost += 1
    elif(tree.Resolved and not(tree.Boosted)):
        xor_res   += 1
    return xor_boost, xor_res


for event in range(tree_ss.GetEntries()):
    tree_ss.GetEntry(event)

    jets = Collection(tree_ss, "Jet")
    TR   = Collection(tree_ss, "TopRes")
    #Boost = Object(tree_ss, "Boosted")
    #Res = Object(tree_ss, "Resolved")
    #xor_boost , xor_res = xor_counting(tree_ss)

    BST          = False
    RSL          = False
    there_is_fwd = False

    if(tree_ss.Boosted):
        BST = True
    if(tree_ss.Resolved and not tree_ss.Boosted):
        RSL = True

    for jet in jets:
        if jet.isForward and jet.isGood:
            there_is_fwd = True
    ## Counting ##
    if BST:
        if there_is_fwd:
            boost_w_fj  += 1
        else:
            boost_wo_fj += 1
    if RSL:
        if there_is_fwd:
            res_w_fj  += 1
        else:
            res_wo_fj += 1

#print("n boost events= ", xor_boost)
#print("n resolved events= ", xor_res)
print("n boost with forward jets= ", boost_w_fj)
print("n boost without forward jets=", boost_wo_fj)
print("n resolved with forward jets=", res_w_fj)
print("n resolved without forward jets=", res_wo_fj)
