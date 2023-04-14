from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.efficiency_class import *
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd #mi servono qua?
#import argparse

'''
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-t','--type',
                    type     = int,
                    default  = 2
                    help     = 'type an int for the heatmap type: 1. (fwd, n_fwd) vs (boost_old, resolved), \n 2. full heatmap: (fwd, n_fwd) vs (resolved, 4 different boost)', 
                    required = True)
parser.add_argument('-f','--full', 
                    help='Full heatmap: (fwd, n_fwd) vs (resolved, 4 * boost)', 
                    required=True)
args = vars(parser.parse_args())

if args["type"] == 1:
    for dataset in dataset_list:
        efficiencyer = efm(dataset)
        efficiencyer.efficiency_plotter()
if args['type'] == 2:
'''
for mini_dataset in datasets_list:
    print("\nInizio calcolo efficienza dataset: "+ mini_dataset.name)
    print("Processo al: " + str( float(datasets_list.index(mini_dataset))/len(datasets_list) * 100) + "%")
    maledetta_efficienza = efficiency_plot(mini_dataset)
    maledetta_efficienza.efficiency_plotter()
    print('-salvataggio files-')
numero_files = len(datasets_list) * 4
print('operazione completa: salvati '+ str(numero_files)+ ' file .png')
