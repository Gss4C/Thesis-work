
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.skimming_pre.eff_sig.efficiency_class import *
import ROOT
import pandas as pd
import numpy as np
import argparse

'''
info utili per le liste quando conto i bg
Ordine selezioni: [32, 32b, d, db]
Ordine modes: [bf, bnf, rf, rnf]
'''

#################
#   ARGOMENTI   #
#################
parser = argparse.ArgumentParser(description='Plot efficienze e significance')
parser.add_argument('-s', '--sig',
                    type     = int,
                    help     = '1/0: if true, the program will calculate significances and will write a csv which resume everything', 
                    required = True)
options = parser.parse_args()
if options.sig: #creazione variabili per significance
    Sig_1000 = []
    Sig_1100 = []
    Sig_1300 = []
    NCountbg_t32_bf = 0
    NCountbg_t32_bn = 0
    NCountbg_t32_rf = 0
    NCountbg_t32_rn = 0
    NCountbg_t32 = [NCountbg_t32_bf,NCountbg_t32_bn,NCountbg_t32_rf,NCountbg_t32_rn]

    NCountbg_t32b_bf = 0
    NCountbg_t32b_bn = 0
    NCountbg_t32b_rf = 0
    NCountbg_t32b_rn = 0
    NCountbg_t32b = [NCountbg_t32b_bf,NCountbg_t32b_bn,NCountbg_t32b_rf,NCountbg_t32b_rn]

    NCountbg_d_bf = 0
    NCountbg_d_bn = 0
    NCountbg_d_rf = 0
    NCountbg_d_rn = 0
    NCountbg_d = [NCountbg_d_bf,NCountbg_d_bn,NCountbg_d_rf,NCountbg_d_rn]

    NCountbg_db_bf = 0
    NCountbg_db_bn = 0
    NCountbg_db_rf = 0
    NCountbg_db_rn = 0
    NCountbg_db = [NCountbg_db_bf,NCountbg_db_bn,NCountbg_db_rf,NCountbg_db_rn]

for mini_dataset in full_range_signals_list:
    print("\nInizio calcolo efficienza dataset: "+ mini_dataset.name)
    print("Processo al: " + str( float(full_range_signals_list.index(mini_dataset))/len(full_range_signals_list) * 100) + "%")
    
    maledetta_efficienza = efficiency_plot(mini_dataset)
    NCount_t32, NCount_t32b, NCount_d, NCount_db = maledetta_efficienza.efficiency_plotter(significance = options.sig)
    print('-salvataggio files-')

    if options.sig:
        print('calcolo per le significance...')
        
        if full_range_signals_list.index(mini_dataset) == 0:
            Sig_1000 = [NCount_t32, NCount_t32b, NCount_d, NCount_db]
        elif full_range_signals_list.index(mini_dataset) == 1:
            Sig_1100 = [NCount_t32, NCount_t32b, NCount_d, NCount_db]
        elif full_range_signals_list.index(mini_dataset) == 2:
            Sig_1300 = [NCount_t32, NCount_t32b, NCount_d, NCount_db]
        elif full_range_signals_list.index(mini_dataset) >= 2:
            for NCi,NCbg_index in zip(NCount_t32 , range(len(NCountbg_t32))):
                NCountbg_t32[NCbg_index] += NCi
            for NCi,NCbg_index in zip(NCount_t32b , range(len(NCountbg_t32b))):
                NCountbg_t32b[NCbg_index] += NCi
            for NCi,NCbg_index in zip(NCount_d , range(len(NCountbg_d))):
                NCountbg_d[NCbg_index] += NCi
            for NCi,NCbg_index in zip(NCount_db , range(len(NCountbg_db))):
                NCountbg_db[NCbg_index] += NCi
Bg_gigalist = [NCountbg_t32,NCountbg_t32b,NCountbg_d,NCountbg_db]

righe = ['tau32', 'tau32_B', 'deep', 'deep_B']
signal_list = [Sig_1000, Sig_1100, Sig_1300]
signal_names = ['Sig_1000', 'Sig_1100', 'Sig_1300']

for signal,signal_name in zip(signal_list, signal_names):
    sel_mode_Z = {}
    for Bg_sel, Sig_sel, name in zip(Bg_gigalist, signal, righe): #fissata la singola selezione
        temp_list = []
        for bi,si in zip(Bg_sel, Sig_sel):             #fissato il singolo mode
            significance = si/np.sqrt(bi)
            temp_list.append(significance)
            sel_mode_Z[name] = temp_list

    sig_1000_df = pd.DataFrame(data=sel_mode_Z , index=['b_fw', 'b_notfw','r_fw','r_notfw'])
    plt.rcParams["figure.figsize"]=[8, 5] 
    plt.rcParams["figure.autolayout"]=True 
    plt.title("Significances, signal dataset" + signal_name) 
    plot = sns.heatmap(sig_1000_df, cmap= 'BuPu', annot=True)
    plt.savefig('significances/significance_Tprime_'+ signal_name + '.png') 
    plt.close()

numero_files = len(full_range_signals_list) * 4
print('operazione completa: salvati '+ str(numero_files)+ ' file .png')