from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 

file_s = ROOT.TFile("/afs/cern.ch/user/j/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/TprimeToTZM1800_Skim", "Open")
getent = ROOT.TFile("/eos/user/o/oiorio/samples/ttdm/TprimeToTZM1800.root'", "Open") 
tree_s = file_s.Events
tree_get = getent.Events
#/home/iorio/public/tDM/tDM_mPhi1000_mChi1.root

boost_w_fj  = 0
boost_wo_fj = 0
res_w_fj    = 0
res_wo_fj   = 0

for event in range(tree_s.GetEntries()):
    
    tree_s.GetEntry(event)
    jets   = Collection(tree_s, "Jet")
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

print("boost with forward jets=      ", float(boost_w_fj)/tree_get.Events.GetEntries() )
print("boost without forward jets=   ", float(boost_wo_fj)/tree_get.Events.GetEntries())
print("resolved with forward jets=   ", float(res_w_fj)/tree_get.Events.GetEntries()   )
print("resolved without forward jets=", float(res_wo_fj)/tree_get.Events.GetEntries()  )

epsilon = {}
epsilon["boosted"]=[boost_w_fj*100, boost_wo_fj*100]
epsilon["boosted"]=[res_w_fj*100, res_wo_fj*100]
df = pd.DataFrame(data=epsilon , index=["fwd" , "not_fwd"])
plt.rcParams["figure.figsize"]=[8, 5] 
plt.rcParams["figure.autolayout"]=True 
plt.title("Efficiencies (%)") 
plot = sns.heatmap(epsilon, cmap="crest", annot=True)
