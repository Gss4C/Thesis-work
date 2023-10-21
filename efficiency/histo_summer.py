import ROOT 
import argparse
from PhysicsTools.NanoAODTools.postprocessing.Thesis.efficiency.classes_efficiency import *

parser = argparse.ArgumentParser(description = "Threshold computation")
parser.add_argument("-t", "--threshold",
                    type     = int,
                    help     = "Select if use the Threshold of TprimeToTZ_1000_2018 by 10, 5 or 1",
                    required = True)
opt = parser.parse_args()

crabout = json_reader("crabout_files.json")

#iniziare a inserire la definizione dei due histogrammi che poi faccio il draw alla fine
N_bins = 250
h_met_bg      = ROOT.TH1F("MET_pt", "MET_pt", N_bins, 200 ,1200)
#h_met_sig     = ROOT.TH1F("MET_pt", "MET_pt", N_bins, 200 ,1200)

h_high_bg      = ROOT.TH1F("TopHighPt_score2", "TopHighPt_score2", N_bins, 0 ,1)
#h_high_sig     = ROOT.TH1F("TopHighPt_score2", "TopHighPt_score2", N_bins, 200 ,1200)

h_low_bg      = ROOT.TH1F("TopLowPt_scoreDNN", "TopLowPt_scoreDNN", N_bins, 0 ,1)
#h_low_sig     = ROOT.TH1F("TopLowPt_scoreDNN", "TopLowPt_scoreDNN", N_bins, 200 ,1200)
print('inizio lettura dati...')
for cluster in crabout['meta_info']['cluster_background']:
    for index in range(len(crabout[cluster])):
        nome_file_root = crabout['meta_info']['eos_histo_fwdj'] + str(opt.threshold) + "/" + 'Th_' + str(opt.threshold) + "_"+crabout[cluster][index].replace('.txt','.root')
        dataset_name = crabout[cluster][index].replace(".txt", "")
        root_file = ROOT.TFile(nome_file_root, "Open")

        h_high = root_file.Get("TopHighPt_score2")
        h_low  = root_file.Get("TopLowPt_scoreDNN")
        h_met  = root_file.Get("MET_pt")

        h_high_bg.Add(h_high)
        h_low_bg.Add(h_low)
        h_met_bg.Add(h_met)

print('Fine valutazione dei fondi.\nValutazione dei segnali...')
for signal in crabout['meta_info']['cluster_signal']:
    for index in range(len(crabout[cluster])):
        c1 = ROOT.TCanvas()
        c2 = ROOT.TCanvas()
        c3 = ROOT.TCanvas()
        
        nome_file_root = crabout['meta_info']['eos_histo_fwdj'] + str(opt.threshold) + "/" + 'Th_' + str(opt.threshold) + "_"+ crabout[signal][index].replace('.txt','.root')
        dataset_name = crabout[signal][index].replace(".txt", "")
        root_file = ROOT.TFile(nome_file_root, "Open")

        h_high = root_file.Get("TopHighPt_score2")
        h_low  = root_file.Get("TopLowPt_scoreDNN")
        h_met  = root_file.Get("MET_pt")

        ########################
        #    Drawing Histos    #
        ########################
        print("creo 3 histo per ogni segnale...")
        print("Inizio il primo")
        c1.Draw()
        c1.cd()
        h_met_bg.SetLineColor(4)
        h_met_bg.GetXaxis().SetTitle("E [Gev]")
        h_met_bg.SetTitle(str(opt.threshold) + " MET_pt" + dataset_name)
        h_met_bg.Draw('hist')
        print("fatto il background")
        h_met.SetLineColor(2)
        h_met.GetXaxis().SetTitle("E [Gev]")
        h_met.SetTitle(str(opt.threshold) + " MET_pt" + dataset_name)
        h_met.Draw('hist same')
        print('fatto il segnale')
        leg = ROOT.TLegend(0.98,0.9,0.78,0.75)
        leg.SetHeader("Legenda","C")
        leg.AddEntry(h_met_bg, "Background", 'f')
        leg.AddEntry(h_met   , "Signal",     'f')
        leg.Draw()
        print('fatta la legenda')
        c1.SetLogy()
        c1.SaveAs(crabout['meta_info']['eos_histo_fwdj']+"finals/MET_pt_"+ str(opt.threshold) +"_"+ dataset_name+".png")
        print('SUCCESS')

        c2.Draw()
        c2.cd()
        h_high_bg.SetLineColor(4)
        h_high_bg.GetXaxis().SetTitle("Score HighPt")
        h_high_bg.SetTitle(str(opt.threshold) + " high_pt" + dataset_name)
        h_high_bg.Draw('hist')
        h_high.SetLineColor(2)
        h_high.GetXaxis().SetTitle("E [Gev]")
        h_high.SetTitle(str(opt.threshold) + " high_pt" + dataset_name)
        h_high.Draw('hist same')
        leg = ROOT.TLegend(0.98,0.9,0.78,0.75)
        leg.SetHeader("Legenda","C")
        leg.AddEntry(h_high_bg, "Background", 'f')
        leg.AddEntry(h_high   , "Signal",     'f')
        leg.Draw()
        c2.SetLogy()
        c2.SaveAs(crabout['meta_info']['eos_histo_fwdj']+"finals/high_"+ str(opt.threshold) +"_"+ dataset_name+".png")

        c3.Draw()
        c3.cd()
        h_low_bg.SetLineColor(4)
        h_low_bg.GetXaxis().SetTitle("Score LowPt")
        h_low_bg.SetTitle(str(opt.threshold) + " low_pt" + dataset_name)
        h_low_bg.Draw('hist')
        h_low.SetLineColor(2)
        h_low.GetXaxis().SetTitle("E [Gev]")
        h_low.SetTitle(str(opt.threshold) + " low_pt" + dataset_name)
        h_low.Draw('hist same')
        leg = ROOT.TLegend(0.98,0.9,0.78,0.75)
        leg.SetHeader("Legenda","C")
        leg.AddEntry(h_low_bg, "Background", 'f')
        leg.AddEntry(h_low   , "Signal",     'f')
        leg.Draw()
        c3.SetLogy()
        c3.SaveAs(crabout['meta_info']['eos_histo_fwdj']+"finals/low_"+ str(opt.threshold) +"_"+ dataset_name+".png")