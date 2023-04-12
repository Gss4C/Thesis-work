from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.efficiency_class import classic_efficiency_make as efm
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd #mi servono qua?
import argparse

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-c','--classic',
                    help='Standard heatmap: (fwd, n_fwd) vs (boost_old, resolved)', 
                    required=True)
parser.add_argument('-f','--full', 
                    help='Full heatmap: (fwd, n_fwd) vs (resolved, 4 * boost)', 
                    required=True)
args = vars(parser.parse_args())

for dataset in dataset_list:
    efficiencyer = efm(dataset)
    efficiencyer.efficiency_plotter()