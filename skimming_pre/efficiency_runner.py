
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.efficiency_class import *
import ROOT
import pandas as pd
import numpy as np
import datetime
import argparse

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
    Bi_t32  = 0
    Bi_t32b = 0
    Bi_d    = 0
    Bi_db   = 0
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
            Sig_1300.append(NCount_t32)
            Sig_1300.append(NCount_t32b)
            Sig_1300.append(NCount_d)
            Sig_1300.append(NCount_db)
        elif datasets_list.index(mini_dataset) >= 2:
            Bi_t32  += NCount_t32
            Bi_t32b += NCount_t32b
            Bi_d    += NCount_d
            Bi_db   += NCount_db
        ## fine funzione significance
B_sing.append(Bi_t32)
B_sing.append(Bi_t32b)
B_sing.append(Bi_d)
B_sing.append(Bi_db)

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

numero_files = len(datasets_list) * 4
print('operazione completa: salvati '+ str(numero_files)+ ' file .png')