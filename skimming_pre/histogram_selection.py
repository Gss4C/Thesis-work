import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.eff_sig.efficiency_class import *

percorso  = "/afs/cern.ch/user/j/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/"

variables=[("MET_pt"," MET ",100,0,500)]
cuts = [("boosted_deeptag")]
for dataset in signal_only_list:
    #mi piglio Tree->Events
    skim_dataset_file_name = percorso + dataset.name.replace(".root","_Skim.root")
    skimmed_file = ROOT.TFile(skim_dataset_file_name,"Open")
    skimmed_tree = skimmed_file.Events
    var=variables[0]
    cut=cuts[0]
    houtput = ROOT.TH1F(var[0],var[0],var[1],var[2],var[3])
    skimmed_tree.Project(houtput,var[0],cut[0])