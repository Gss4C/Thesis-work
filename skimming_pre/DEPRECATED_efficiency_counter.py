from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 

percorso = "/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/"
nome_file = "tDM_mPhi1000_mChi1_Skim.root"

file_s = ROOT.TFile( percorso + nome_file,"Open")
genw = ROOT.TFile("/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/histOut.root", "Open")
tree_s = file_s.Events


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

genw_plots = genw.plots
histo = genw_plots.Get("h_genweight")
weight = histo.GetBinContent(1)

eff_boost_w_fj = float(boost_w_fj)/weight
eff_boost_wo_fj = float(boost_wo_fj)/weight
eff_res_w_fj = float(res_w_fj)/weight
eff_res_wo_fj = float(res_wo_fj)/weight

print("boost with forward jets=      ", eff_boost_w_fj )
print("boost without forward jets=   ", eff_boost_wo_fj)
print("resolved with forward jets=   ", eff_res_w_fj   )
print("resolved without forward jets=", eff_res_wo_fj  )

epsilon = {}
epsilon["boosted"]=[eff_boost_w_fj*100, eff_boost_wo_fj*100]
epsilon["resolved"]=[eff_res_w_fj*100, eff_res_wo_fj*100]
df = pd.DataFrame(data=epsilon , index=["fwd" , "not_fwd"])
plt.rcParams["figure.figsize"]=[8, 5] 
plt.rcParams["figure.autolayout"]=True 
plt.title("Efficiencies (%)") 
plot = sns.heatmap(df, cmap="summer", annot=True)
plt.savefig("nome.png")