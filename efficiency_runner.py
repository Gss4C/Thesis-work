from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.efficiency_class import *
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd #mi servono qua?
import argparse

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

#crearmi qui una lista nuova per i dataset skimmed col minisample

maledetta_efficienza = efficiency_plot(ZJetsToNuNu_HT_600To800)
maledetta_efficienza.efficiency_plotter()

'''for dataset in dataset_list:
        efficiencyer = efm(dataset)
        efficiencyer.efficiency_plotter()'''