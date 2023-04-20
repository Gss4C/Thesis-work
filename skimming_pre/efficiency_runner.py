
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.efficiency_class import *
import ROOT
import pandas as pd
import numpy as np
import datetime
import argparse
#####################
#   Temporary doc   #
#####################
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
                    help     = 'True/False: if true, the program will calculate significances and will write a csv which resume everything', 
                    required = True)
options = parser.parse_args()
# Servono per le significance
if options.sig:
    '''
    Bi_t32  = 0
    Bi_t32b = 0
    Bi_d    = 0
    Bi_db   = 0
'''
    B_sing  = []
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

for mini_dataset in datasets_list:
    print("\nInizio calcolo efficienza dataset: "+ mini_dataset.name)
    print("Processo al: " + str( float(datasets_list.index(mini_dataset))/len(datasets_list) * 100) + "%")
    
    maledetta_efficienza = efficiency_plot(mini_dataset)
    NCount_t32, NCount_t32b, NCount_d, NCount_db = maledetta_efficienza.efficiency_plotter(significance = options.sig)
    print('-salvataggio files-')

    if options.sig:
        print('calcolo per le significance...')
        creation_time = datetime.datetime.now()
        
        if datasets_list.index(mini_dataset) == 0:
            Sig_1000 = [NCount_t32, NCount_t32b, NCount_d, NCount_db]
        elif datasets_list.index(mini_dataset) == 1:
            Sig_1100 = [NCount_t32, NCount_t32b, NCount_d, NCount_db]
        elif datasets_list.index(mini_dataset) == 2:
            Sig_1300 = [NCount_t32, NCount_t32b, NCount_d, NCount_db]
        elif datasets_list.index(mini_dataset) >= 2:
            for NCi,NCbg_index in zip(NCount_t32 , range(len(NCountbg_t32))):
                NCountbg_t32[NCbg_index] += NCi
            for NCi,NCbg_index in zip(NCount_t32b , range(len(NCountbg_t32b))):
                NCountbg_t32b[NCbg_index] += NCi
            for NCi,NCbg_index in zip(NCount_d , range(len(NCountbg_d))):
                NCountbg_d[NCbg_index] += NCi
            for NCi,NCbg_index in zip(NCount_db , range(len(NCountbg_db))):
                NCountbg_db[NCbg_index] += NCi

Bg_gigalist = [NCountbg_t32,NCountbg_t32b,NCountbg_d,NCountbg_db]

# per ogni selezione (nelle liste Gb_gigalist e Sig_1X00) devo cacciare quattro efficienze
#segnale 1000
righe = ['tau32', 'tau32_B', 'deep', 'deep_B']
sel_mode_Z = {}
for Bg_sel, Sig_sel, names in zip(Bg_gigalist, Sig_1000, righe): #fissata la singola selezione
    temp_list = []
    for bi,si in zip(Bg_sel, Sig_sel):             #fissato il singolo mode
        significance = si/np.sqrt(bi)
        temp_list.append(significance)
        sel_mode_Z[name] = temp_list

sig_1000_df = pd.DataFrame(data=sel_mode_Z , index=['t32', 't32_b','deep','deep_b'])
plt.rcParams["figure.figsize"]=[8, 5] 
plt.rcParams["figure.autolayout"]=True 
plt.title("Significances, dataset M=1000") 
plot = sns.heatmap(sig_1000_df, cmap= 'BuPu', annot=True)
plt.savefig("significances/significance_Tprime_1000.png") 
plt.close()

#segnale 1100
righe = ['tau32', 'tau32_B', 'deep', 'deep_B']
sel_mode_Z = {}
for Bg_sel, Sig_sel, names in zip(Bg_gigalist, Sig_1300, righe): #fissata la singola selezione
    temp_list = []
    for bi,si in zip(Bg_sel, Sig_sel):             #fissato il singolo mode
        significance = si/np.sqrt(bi)
        temp_list.append(significance)
        sel_mode_Z[name] = temp_list

sig_1300_df = pd.DataFrame(data=sel_mode_Z , index=['t32', 't32_b','deep','deep_b'])
plt.rcParams["figure.figsize"]=[8, 5] 
plt.rcParams["figure.autolayout"]=True 
plt.title("Significances, dataset M=1000") 
plot = sns.heatmap(sig_1300_df, cmap= 'BuPu', annot=True)
plt.savefig("significances/significance_Tprime_1100.png") 
plt.close()

#segnale 1300
righe = ['tau32', 'tau32_B', 'deep', 'deep_B']
sel_mode_Z = {}
for Bg_sel, Sig_sel, names in zip(Bg_gigalist, Sig_1300, righe): #fissata la singola selezione
    temp_list = []
    for bi,si in zip(Bg_sel, Sig_sel):             #fissato il singolo mode
        significance = si/np.sqrt(bi)
        temp_list.append(significance)
        sel_mode_Z[name] = temp_list

sig_1300_df = pd.DataFrame(data=sel_mode_Z , index=['t32', 't32_b','deep','deep_b'])
plt.rcParams["figure.figsize"]=[8, 5] 
plt.rcParams["figure.autolayout"]=True 
plt.title("Significances, dataset M=1000") 
plot = sns.heatmap(sig_1300_df, cmap= 'BuPu', annot=True)
plt.savefig("significances/significance_Tprime_1300.png") 
plt.close()


#commentare questo sotto
'''
significances = {}
righe = ['tau32', 'tau32_B', 'deep', 'deep_B']
for sig1, sig2, sig3, bkg, name in zip(Sig_1000, Sig_1100, Sig_1300, B_sing, righe):
    significance_1 = sig1/np.sqrt(bkg)
    significance_2 = sig2/np.sqrt(bkg)
    significance_3 = sig3/np.sqrt(bkg)
    significances[name] = [significance_1, significance_2, significance_3]

significance_dataframe = pd.DataFrame(data=significances , index=['TprimeBToTZ_M_1000', 'TprimeBToTZ_M_1100', 'TprimeBToTZ_M_1300'])
significance_final     = significance_dataframe.transpose()
significance_final.to_csv('significances/signinificance_'+
                            str(creation_time.year) + '-' +
                            str(creation_time.month) + '-' +
                            str(creation_time.day) + '-' +
                            str(creation_time.microsecond)+
                            ".csv")
'''

numero_files = len(datasets_list) * 4
print('operazione completa: salvati '+ str(numero_files)+ ' file .png')