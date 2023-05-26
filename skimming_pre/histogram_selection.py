import ROOT
import argparse
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.eff_sig.efficiency_class import *

def weights(path_to_histo, sample):
    L_run2 = 137000
    weights_histo_name = path_to_histo + "hist_out_" + sample.name
    weights_histo_file = ROOT.TFile(weights_histo_name, 'Open')
    weight_histo = weights_histo_file.plots.Get('h_genweight')
    n_mc_tot = weight_histo.GetBinContent(1) 
    w = sample.sigma * L_run2 / (n_mc_tot)
    return w

percorso  = "/afs/cern.ch/user/j/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/"
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
            w = weights(percorso, dataset)

            skim_dataset_file_name = percorso + dataset.name.replace(".root","_Skim.root") #forse questi 3 righi riesco a farli come funzione
            skimmed_file = ROOT.TFile(skim_dataset_file_name,"Open")
            skimmed_tree = skimmed_file.Events

            c = ROOT.TCanvas()
            houtput = ROOT.TH1F('MET_pt','MET ' + dataset.name.replace('.root','') ,100,200,1000)
            skimmed_tree.Project(houtput.GetName(), 'MET_pt', cut) #getname() ??
            
            houtput.Scale(w)
            c.Draw()
            houtput.Draw()
            #n_mc = houtput.Integral()
            c.SaveAs("MET_signal_" + cut + dataset.name.replace(".root", "") + ".png")

if options.type == 1:
    bkg_histos = ROOT.TH1F()

    h_bgsum_tau32 = ROOT.TH1F('MET_pt', 'MET backgrounds', 100,200,1000)
    h_bgsum_tau32b = ROOT.TH1F('MET_pt', 'MET backgrounds', 100,200,1000)
    h_bgsum_deep = ROOT.TH1F('MET_pt', 'MET backgrounds', 100,200,1000)
    h_bgsum_deepb = ROOT.TH1F('MET_pt', 'MET backgrounds', 100,200,1000)
    histo_bgsum_list=[h_bgsum_tau32, h_bgsum_tau32b, h_bgsum_deep, h_bgsum_deepb]

    h_signal_tau32 = ROOT.TH1F('MET_pt', 'MET backgrounds', 100,200,1000)
    h_signal_tau32b = ROOT.TH1F('MET_pt', 'MET backgrounds', 100,200,1000)
    h_signal_deep = ROOT.TH1F('MET_pt', 'MET backgrounds', 100,200,1000)
    h_signal_deepb = ROOT.TH1F('MET_pt', 'MET backgrounds', 100,200,1000)
    histo_signal_list=[h_signal_tau32, h_signal_tau32b, h_signal_deep, h_signal_deepb]
    
    for cut, h_bkgsum, h_signal in zip(cuts, histo_bgsum_list, histo_signal_list):
        print("inizio del processo per il cut "+ cut)
        c = ROOT.TCanvas()
        c.Draw()
        for background in bkg_only_list:
            w = weights(path_to_histo = percorso,
                        sample        = background)

            skim_background_file_name = percorso + background.name.replace(".root","_Skim.root")
            skimmed_file = ROOT.TFile(skim_background_file_name,"Open")
            skimmed_tree = skimmed_file.Events

            h_single_bg = ROOT.TH1F('MET_pt','MET' + background.name ,100,200,1000)
            skimmed_tree.Project(h_single_bg.GetName(), 'MET_pt', cut)

            h_single_bg.Scale(w)
            h_bkgsum.Add(h_single_bg)

        for signal in signal_only_list:
            w = weights(path_to_histo = percorso,
                        sample        = signal)

            skim_signal_file_name = percorso + signal.name.replace(".root","_Skim.root")
            skimmed_file = ROOT.TFile(skim_signal_file_name,"Open")
            skimmed_tree = skimmed_file.Events

            h_signal = ROOT.TH1F('MET_pt','MET' + signal.name ,100,200,1000)
            skimmed_tree.Project(h_signal.GetName(), 'MET_pt', cut)

            h_signal.Scale(w)

            ########################
            #    Drawing Histos    #
            ########################
            h_bkgsum.SetLineColor(2)
            h_bkgsum.SetFillColorAlpha(2,1)
            h_bkgsum.GetXaxis().SetTitle("E [Gev]")
            h_bkgsum.GetYaxis().SetTitle("Scaled Counts/8 GeV")
            h_bkgsum.SetTitle(cut + signal.name.replace('.root',''))

            '''
            max_bkg = h_bkgsum.GetMaximum()
            max_signal = h_signal.GetMaximum()
            max_Y = int(max(max_bkg, max_signal)) + 15
            h_bkgsum.GetYaxis().SetRange(0,max_Y)
            '''
            #h_bkgsum.SetLogy()
            h_bkgsum.Draw('hist')

            #h_signal.GetYaxis().SetRange(0,max_Y)
            h_signal.SetTitle(cut + signal.name.replace('.root',''))
            h_signal.SetLineColor(9)
            h_signal.SetFillColorAlpha(9,0.7)
            #h_signal.SetLogy()
            h_signal.Draw("SAME,hist")

                        
            leg = ROOT.TLegend(0.98,0.9,0.78,0.75) #0.1,0.7,0.4,0.9 #0.98,0.9,0.78,0.75
            leg.SetHeader("Legenda", "C")                         
            leg.AddEntry(h_signal, "signal","f")            
            leg.AddEntry(h_bkgsum, "backgrounds sum","f")
            leg.Draw()

            c.SetLogy()
            c.SaveAs("MET_cutplot_" + cut + signal.name.replace(".root", "") + ".png")