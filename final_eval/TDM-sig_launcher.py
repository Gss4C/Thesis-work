#   ISTRUZIONI   #
#Ordine: 5
#Input:  Jsons provenienti da prev
#Output: Heatmap VIOLA delle significance
#Prev:   sig_recluster.py
#Next:   

import json
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.ef_sig_class import *

parser = argparse.ArgumentParser(description = "Threshold")
parser.add_argument("-t", "--threshold",
                    type     = int,
                    help     = "Select threshold, int",
                    required = True)
opt = parser.parse_args()


###################
#    Functions    #
###################
def norm_count_4(dataset_diz, sample_dict, name_string, luminosity):
    output_diz = {}
    sigma = sample_dict[name_string].sigma
    sl = sigma*luminosity

    output_diz['th_700'] = sl*dataset_diz['th_700']/dataset_diz['weight']
    output_diz['th_700_fwd'] = sl*dataset_diz['th_700_fwd']/dataset_diz['weight']
    output_diz['th_1000'] = sl*dataset_diz['th_1000']/dataset_diz['weight']
    output_diz['th_1000_fwd'] = sl*dataset_diz['th_1000_fwd']/dataset_diz['weight']
    output_diz['th_1800'] = sl*dataset_diz['th_1800']/dataset_diz['weight']
    output_diz['th_1800_fwd'] = sl*dataset_diz['th_1800_fwd']/dataset_diz['weight']

    return output_diz


every_sig_list = ["tDM_mPhi50_mChi1_2018", "tDM_mPhi500_mChi1_2018", "tDM_mPhi1000_mChi1_2018"] #TOPP
every_bg_list  = [
    "QCDHT_2000toInf_2018",
    "QCDHT_1500to2000_2018",
    "QCDHT_1000to1500_2018",
    "QCDHT_700to1000_2018",
    "QCDHT_500to700_2018",
    "QCDHT_300to500_2018",
    "ZJetsToNuNu_HT200to400_2018",
    "ZJetsToNuNu_HT400to600_2018",
    "ZJetsToNuNu_HT600to800_2018",
    "ZJetsToNuNu_HT800to1200_2018",
    "ZJetsToNuNu_HT1200to2500_2018",
    "ZJetsToNuNu_HT2500toInf_2018",
    "TT_Mtt1000toInf_2018",
    "TT_Mtt700to1000_2018",
    "TT_hadr_2018",
    "TT_semilep_2018"
]

##############
#    MAIN    #
##############
luminosity = 137000 #bp^-1
meta_data = json_reader("crabout_files.json")
datas = json_reader(meta_data['meta_info']['eos_sig_jsons']+'TDM_forsig_th_'+ str(opt.threshold)+'.json') 

# faccio normalizzazione di conteggi di segnali
#li conservo da qualche parte
signal_diz = {}
print('inizio ciclo dei segnali')
for signal in datas['info']['TDM_signals']:
    for dataset in datas[signal]: #qui sono nel segnale
        for dataset_namestring, tiodio in dataset.items():
            signal_diz[dataset_namestring] = {}
            output_diz = norm_count_4(dataset_diz = dataset[dataset_namestring], 
                                    sample_dict = sample_dict, 
                                    name_string = dataset_namestring, 
                                    luminosity  = luminosity)
            signal_diz[dataset_namestring]['th_700'] = output_diz['th_700']
            signal_diz[dataset_namestring]['th_700_fwd'] = output_diz['th_700_fwd']
            signal_diz[dataset_namestring]['th_1000'] = output_diz['th_1000']
            signal_diz[dataset_namestring]['th_1000_fwd'] = output_diz['th_1000_fwd']
            signal_diz[dataset_namestring]['th_1800'] = output_diz['th_1800']
            signal_diz[dataset_namestring]['th_1800_fwd'] = output_diz['th_1800_fwd']

background_diz = {}
print('inizio ciclo dei fondi')
for background in datas['info']['backgrounds']:
    for dataset in datas[background]:

        for dataset_namestring, ammazzatipython in dataset.items():
            background_diz[dataset_namestring] = {}
            output_diz = norm_count_4(dataset_diz = dataset[dataset_namestring], 
                                      sample_dict = sample_dict, 
                                      name_string = dataset_namestring, 
                                      luminosity  = luminosity)
            background_diz[dataset_namestring]['th_700'] = output_diz['th_700']
            background_diz[dataset_namestring]['th_700_fwd'] = output_diz['th_700_fwd']
            background_diz[dataset_namestring]['th_1000'] = output_diz['th_1000']
            background_diz[dataset_namestring]['th_1000_fwd'] = output_diz['th_1000_fwd']
            background_diz[dataset_namestring]['th_1800'] = output_diz['th_1800']
            background_diz[dataset_namestring]['th_1800_fwd'] = output_diz['th_1800_fwd']

#setting dei counters a 0
bg_th_700 = 0
bg_th_700_fwd = 0
bg_th_1000 = 0
bg_th_1000_fwd = 0
bg_th_1800 = 0
bg_th_1800_fwd = 0


for bg in every_bg_list:

    bg_th_700      += background_diz[bg]['th_700']
    bg_th_700_fwd  += background_diz[bg]['th_700_fwd']
    bg_th_1000     += background_diz[bg]['th_1000']
    bg_th_1000_fwd += background_diz[bg]['th_1000_fwd']
    bg_th_1800     += background_diz[bg]['th_1800']
    bg_th_1800_fwd += background_diz[bg]['th_1800_fwd']

significance = {}
for signal in every_sig_list:
    significance[signal] = {}
    significance[signal]['th_700'] = signal_diz[signal]['th_700']/np.sqrt(bg_th_700)
    significance[signal]['th_700_fwd'] = signal_diz[signal]['th_700_fwd']/np.sqrt(bg_th_700_fwd)
    significance[signal]['th_1000'] = signal_diz[signal]['th_1000']/np.sqrt(bg_th_1000)
    significance[signal]['th_1000_fwd'] = signal_diz[signal]['th_1000_fwd']/np.sqrt(bg_th_1000_fwd)
    significance[signal]['th_1800'] = signal_diz[signal]['th_1800']/np.sqrt(bg_th_1800)
    significance[signal]['th_1800_fwd'] = signal_diz[signal]['th_1800_fwd']/np.sqrt(bg_th_1800_fwd)


## DEVO SOLO DEFINIRE IL PLOTTER
for signal in every_sig_list:
    plotting_data = {}
    plotting_data['score 700']  = [significance[signal]['th_700_fwd'], significance[signal]['th_700']]
    plotting_data['score 1000'] = [significance[signal]['th_1000_fwd'], significance[signal]['th_1000']]
    plotting_data['score 1800'] = [significance[signal]['th_1800_fwd'], significance[signal]['th_1800']]
    df = pd.DataFrame(data = plotting_data, index=['Forward', "Non forward"])

    plt.rcParams["figure.figsize"]    = [8, 5] 
    plt.rcParams["figure.autolayout"] = True 
    plt.title("Significances Th " + str(opt.threshold) + "% "+signal)

    plot = sns.heatmap(df, cmap = 'BuPu', annot=True, annot_kws={"fontsize":15})
    plt.savefig(meta_data['meta_info']['eos_sig'] + 'TDM_' +str(opt.threshold)+'_Significance_' + signal + '.png')
    plt.close()