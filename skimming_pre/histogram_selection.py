import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.eff_sig.efficiency_class import *

percorso  = "/afs/cern.ch/user/j/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/"
L_run2 = 138
variables=["MET_pt"," MET ",100,0,1000]
cuts = ['Boosted_tau32','Boosted_tau32btag','Boosted_deeptag','Boosted_deeptagbtag']

parser = argparse.ArgumentParser(description='Histogram MET_pt plots')
parser.add_argument('-t', '--type',
                    type     = int,
                    help     = '0/1: signal only/signal and background on same plot', 
                    required = True)
options = parser.parse_args()

if options.type == 0:
    for dataset in signal_only_list:
        for cut in cuts:
            weights_histo_name = percorso + "hist_out_" + dataset.name
            weights_histo_file = ROOT.TFile(weights_histo_name, 'Open')
            weight_histo = weights_histo_file.plots.Get('h_genweight')
            n_mc_tot = weight_histo.GetBinContent(1) 
            w = dataset.sigma * L_run2 / (n_mc_tot)

            skim_dataset_file_name = percorso + dataset.name.replace(".root","_Skim.root")
            skimmed_file = ROOT.TFile(skim_dataset_file_name,"Open")
            skimmed_tree = skimmed_file.Events

            c = ROOT.TCanvas()
            houtput = ROOT.TH1F('MET_pt','MET' + dataset.name ,500,0,1000)
            skimmed_tree.Project(houtput.GetName(), 'MET_pt', cut)
            
            houtput.Scale(w)
            c.Draw()
            houtput.Draw()
            #n_mc = houtput.Integral()
            
            c.SaveAs("MET_signal_" + cut + dataset.name.replace(".root", "") + ".png")