import json
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.efficiency.classes_efficiency import *

parser = argparse.ArgumentParser(description = "Threshold")
parser.add_argument("-t", "--threshold",
                    type     = int,
                    help     = "Select threshold, int",
                    required = True)
opt = parser.parse_args()

# FARE ATTENZIONE A PERCORSI DI LETTURA E SCRITTURA CON FWDJ

###################
#    Functions    #
###################
def norm_count_4(dataset_diz, sample_dict, name_string, luminosity):
    output_diz = {}
    sigma = sample_dict[name_string].sigma
    sl = sigma*luminosity

    output_diz['TH_f'] = sl*dataset_diz['TopHigh_fwd']/dataset_diz['weight']
    output_diz['TH']   = sl*dataset_diz['TopHigh']/dataset_diz['weight']
    output_diz['TL_f'] = sl*dataset_diz['TopLow_fwd']/dataset_diz['weight']
    output_diz['TL']   = sl*dataset_diz['TopLow']/dataset_diz['weight']
    return output_diz


every_sig_list = ["TprimeToTZ_1800_2018", "TprimeToTZ_1000_2018", "TprimeToTZ_700_2018"]
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

########################
########################
meta_data = json_reader("crabout_files.json")
datas = json_reader(meta_data['meta_info']['eos_sigp_path_json_fwdj']+'forsig_th_'+ str(opt.threshold)+'.json') 
##########################
#########################

# faccio normalizzazione di conteggi di segnali
#li conservo da qualche parte
signal_diz = {}
print('inizio ciclo dei segnali')
for signal in datas['info']['signals']:
    for dataset in datas[signal]:
        
        for dataset_namestring, tiodio in dataset.items():
            signal_diz[dataset_namestring] = {}
            output_diz = norm_count_4(dataset_diz = dataset[dataset_namestring], 
                                    sample_dict = sample_dict, 
                                    name_string = dataset_namestring, 
                                    luminosity  = luminosity)
            signal_diz[dataset_namestring]['TH_f'] = output_diz['TH_f']
            signal_diz[dataset_namestring]['TH']   = output_diz['TH']
            signal_diz[dataset_namestring]['TL_f'] = output_diz['TL_f']
            signal_diz[dataset_namestring]['TL']   = output_diz['TL']

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
            background_diz[dataset_namestring]['TH_f'] = output_diz['TH_f']
            background_diz[dataset_namestring]['TH']   = output_diz['TH']
            background_diz[dataset_namestring]['TL_f'] = output_diz['TL_f']
            background_diz[dataset_namestring]['TL']   = output_diz['TL']

bg_TH_f = 0
bg_TH   = 0
bg_TL_f = 0
bg_TL   = 0
for bg in every_bg_list:
    bg_TH_f += background_diz[bg]['TH_f']
    bg_TH   += background_diz[bg]['TH']
    bg_TL_f += background_diz[bg]['TL_f']
    bg_TL   += background_diz[bg]['TL']

significance = {}
for signal in every_sig_list:
    significance[signal] = {}
    significance[signal]['TH_f'] = signal_diz[signal]['TH_f']/np.sqrt(bg_TH_f)
    significance[signal]['TH']   = signal_diz[signal]['TH']/np.sqrt(bg_TH)
    significance[signal]['TL_f'] = signal_diz[signal]['TL_f']/np.sqrt(bg_TL_f)
    significance[signal]['TL']   = signal_diz[signal]['TL']/np.sqrt(bg_TL)

## DEVO SOLO DEFINIRE IL PLOTTER
for signal in every_sig_list:
    plotting_data = {}
    plotting_data['TopHighPt'] = [significance[signal]['TH_f'], significance[signal]['TH']]
    plotting_data['TopLowPt']  = [significance[signal]['TL_f'], significance[signal]['TL']]
    df = pd.DataFrame(data=plotting_data, index=['Forward', "Non forward"])

    plt.rcParams["figure.figsize"]    = [8, 5] 
    plt.rcParams["figure.autolayout"] = True 
    plt.title("Significances Th " + str(opt.threshold) + "% "+signal)

    plot = sns.heatmap(df, cmap = 'BuPu', annot=True)
    plt.savefig(meta_data['meta_info']['eos_sigp_path_fwdj'] + str(opt.threshold)+'_Significance_' + signal + '.png')
    plt.close()