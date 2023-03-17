import ROOT

file_ss = ROOT.TFile("/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/tDM_mPhi1000_mChi1_Skim_Sk\
im.root", "Open")
tree_ss = file_ss.Events
file_s  = ROOT.TFile("/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/tDM_mPhi1000_mChi1_Skim.ro\
ot", "Open")
tree_s  = file_s.Events

n_events_s  = float(tree_s.GetEntries())
n_events_ss = float(tree_ss.GetEntries())
n_boosted   = float(tree_ss.GetEntries("Boosted"))
n_resolved  = float(tree_ss.GetEntries("Resolved"))

e_cut_global = n_events_ss/n_events_s
e_boost      = n_boosted/n_events_ss
e_resolv     = n_resolved/n_events_ss
print("Global veto efficiency: ", e_cut_global)
print("Boosted efficiency: ", e_boost)
print("Resolved efficiency: ", e_resolv)
