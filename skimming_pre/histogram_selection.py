import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.eff_sig.efficiency_class import *

percorso  = "/afs/cern.ch/user/j/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/"

for dataset in signal_only_list:
    skim_dataset_file_name = percorso + dataset.name.replace(".root","_Skim.root")
    skimmed_file = ROOT.TFile(skim_dataset_file_name,"Open")
    skimmed_tree = skimmed_file.Events