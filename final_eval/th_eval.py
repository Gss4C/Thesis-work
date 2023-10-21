#   ISTRUZIONI   #
#Ordine: 1
#Input:  files output dello skimming
#Output: 'files.root' con histo di score_700/1000/1800 per ogni dataset
#Prev:   NONE
#Next:   th_maker.py

import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.th_class import *
import warnings
import argparse
warnings.filterwarnings("ignore")

###################
#    Arguments    #
###################

parser = argparse.ArgumentParser(description = "Threshold computation")
parser.add_argument("-c", "--cluster",
                    type     = str,
                    help     = "Input the cluster or the txt name dict",
                    required = True)
options = parser.parse_args()

crabout = json_reader("crabout_files.json")
#print('I will compute threshold with the '+ str(options.efficiency) + '%' +' background efficiency')
#bg_efficiency = options.efficiency/100

cluster = options.cluster 
#for cluster in crabout["meta_info"]["cluster_names"]:
print("\nStarting cluster: " + cluster + "\n")
for index in range(len(crabout[cluster])):
    completamento = index/(len(crabout[cluster])) 
    percentuale   = completamento*100
    percentuale_troncata = round(percentuale, 2)
    print("Completamento cluster: " + str(percentuale_troncata) + "%")
    
    batch_files_list = read_and_list(crabout["meta_info"]["parent_path"] + crabout[cluster][index])
    dataset_name  = crabout[cluster][index].replace(".txt","")
    
    root_filename = crabout[cluster][index].replace(".txt",".root")
    print("Elaborazione del dataset: "+ dataset_name)

    N_bins = 250
    h_ds700   = ROOT.TH1F("deepsc_tp700"  + dataset_name, "deepsc_tp700"  + dataset_name , N_bins, 0 ,1)
    h_ds1000  = ROOT.TH1F("deepsc_tp1000" + dataset_name, "deepsc_tp1000" + dataset_name , N_bins, 0 ,1)
    h_ds1800  = ROOT.TH1F("deepsc_tp1800" + dataset_name, "deepsc_tp1800" + dataset_name , N_bins, 0 ,1)
    h_weights = ROOT.TH1F("genweight" + dataset_name, "genweight" + dataset_name, 1, 0, 1)

    histomaker = thrashold_histomaker()
    weight = histomaker.crea_3_histo(batch_files_list = batch_files_list, 
                                     h_ds700  = h_ds700,
                                     h_ds1000 = h_ds1000,
                                     h_ds1800 = h_ds1800,
                                     dataset_name  = dataset_name)
    h_weights.SetBinContent(1, weight)

    rfile = ROOT.TFile(crabout["meta_info"]["eos_path"]+'thresholds/scores_histos/' + root_filename, "RECREATE")
    h_ds700.Write()
    h_ds1000.Write()
    h_ds1800.Write()
    h_weights.Write()
    rfile.Close()
    print('DONE')