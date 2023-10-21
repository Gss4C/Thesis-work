#   ISTRUZIONI   #
#Ordine: 4
#Input:  Jsons provenienti da prev
#Output: jsons contenenti tutte le soglie tutte insieme coi nomi dei dataset corretti, uno per ogni threshold scelta
#Prev:   ef_launcher.py
#Next:   sig_launcher.py

import json
import os
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.ef_sig_class import *

#######################
#    Oggetti Utili    #
#######################
qcd = 'QCD'
tp  = 'TP'
tt = 'TT'
zjtnn = 'ZJTNN'

ths = [1,5,10]
numeri_tp = [700, 1000, 1800]
crabout = json_reader('crabout_files.json')

##############
#    MAIN    #
##############
names = []
for threshold in ths:
    single_th = []
    for index in range(1,7): #appendo nomi qcd
        stringa = str(threshold) + "_" +qcd + '_' + str(index) + ".json"
        single_th.append(stringa)
    for index in numeri_tp: #appendo nomi tp
        stringa = str(threshold) + "_" +tp + '_' + str(index) + ".json"
        single_th.append(stringa) 
    for index in range(1,8): #appendo nomi zjtnn
        stringa = str(threshold) + "_" +zjtnn + '_' + str(index) + ".json"
        single_th.append(stringa) 
    for index in range(1,5): #appendo nomi tt
        stringa = str(threshold) + "_" +tt + '_' + str(index) + ".json"
        single_th.append(stringa) 
    names.append(single_th)

for i, th_files_list in enumerate(names):
    temp_dict = {}
    for filename in th_files_list:
        dataset_type = filename.split('_')[1]

        key = f'{dataset_type}'
        if key not in temp_dict:
            temp_dict[key] = []
        path_filename = crabout['meta_info']['eos_sigcounts'] + filename
        with open(path_filename, 'r') as f:
            data = json.load(f)
        
        temp_dict[key].append(data)
        
        temp_dict['info'] = {}
        temp_dict['info']['signals'] = [tp]
        temp_dict['info']['backgrounds'] = [tt, zjtnn, qcd]

    if i == 0:
        saveas_json(temp_dict, crabout['meta_info']['eos_sig_jsons'] +'forsig_th_'+ str(1)+'.json')
    if i == 1:
        saveas_json(temp_dict, crabout['meta_info']['eos_sig_jsons'] +'forsig_th_'+ str(5)+'.json')
    if i == 2:
        saveas_json(temp_dict, crabout['meta_info']['eos_sig_jsons'] +'forsig_th_'+ str(10)+'.json')