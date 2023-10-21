#   ISTRUZIONI   #
#Ordine: 2
#Input:  Output precedente
#Output: Istogrammi con tutti i fondi + threshold in file json
#Prev:   th_eval.py
#Next:   ef_launcher.py

import ROOT
import json
import argparse
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.th_class import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


parser = argparse.ArgumentParser(description = "Threshold computation")
parser.add_argument("-e", "--efficiency",
                    type     = int,
                    help     = "INT - misID percentage",
                    required = True)
opt = parser.parse_args()
efficiency = float(opt.efficiency)/100.0

crabout     = json_reader("crabout_files.json")
bg_datasets = ["ZJTNN_3","ZJTNN_4","ZJTNN_5","ZJTNN_6","ZJTNN_7","TT_1","TT_2","TT_3","TT_4","QCD_1","QCD_2","QCD_3","QCD_4","QCD_5","QCD_6"]

h_tot_700  = ROOT.TH1F("Score TP-700", "Score TP-700", N_bins, 0 ,1)
h_tot_1000 = ROOT.TH1F("Score TP-1000", "Score TP-1000", N_bins, 0 ,1)
h_tot_1800 = ROOT.TH1F("Score TP-1800", "Score TP-1800", N_bins, 0 ,1)

for i, dataset in enumerate(bg_datasets): #nel mio dict dataset is un file.txt
    print('Starting background scaled total histogram...')
    #aprire file root
    root_filename = crabout['meta_info']['eos_path'] + 'thresholds/scores_histos/'+ crabout[dataset][0].replace('.txt','.root')
    dataset_name  = crabout[dataset][0].replace('.txt', '')
    
    print('Opening dataset ' + dataset_name)
    completation = round(i/len(bg_datasets) *100, 2)
    print('Completation: ' + str(completation) + '%')

    rfile = ROOT.TFile(root_filename)

    h_700    = rfile.Get('deepsc_tp700'  + dataset_name)
    h_1000   = rfile.Get('deepsc_tp1000' + dataset_name)
    h_1800   = rfile.Get('deepsc_tp1800' + dataset_name)
    h_weight = rfile.Get('genweight' + dataset_name)
    genweight = h_weight.GetBinContent(1)

    sigma_dataset = sample_dict[dizionario_per_samples[dataset]].sigma
    scale_factor  = sigma_dataset * luminosity/genweight

    h_700.Scale(scale_factor)
    h_1000.Scale(scale_factor)
    h_1800.Scale(scale_factor)

    h_tot_700.Add(h_700)
    h_tot_1000.Add(h_1000)
    h_tot_1800.Add(h_1800)
    
    rfile.Close()

print('Histograms COMPLETE\nSaving files...')
new_rfile = ROOT.TFile(crabout['meta_info']['eos_path'] + 'thresholds/thresholds_histos_bg/histos_for_threshold_'+str(opt.efficiency)+'.root', "RECREATE")
h_tot_700.Write()
h_tot_1000.Write()
h_tot_1800.Write()
new_rfile.Close()
print('SUCCESS\nThreshold evaluation...')

finder_700  = threshold_evalutator(histo = h_tot_700)
finder_1000 = threshold_evalutator(histo = h_tot_1000)
finder_1800 = threshold_evalutator(histo = h_tot_1800)

th_700,  epsilon_700  = finder_700.threshold_F_seeker(bg_efficiency = efficiency)
th_1000, epsilon_1000 = finder_1000.threshold_F_seeker(bg_efficiency = efficiency)
th_1800, epsilon_1800 = finder_1800.threshold_F_seeker(bg_efficiency = efficiency)

output = {}
output['th_700'] = th_700
output['th_1000'] = th_1000
output['th_1800'] = th_1800

saveas_json(output, crabout['meta_info']['eos_path']+'thresholds/thresholds_' + str(opt.efficiency) + '.json')