from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.mini_samples import *
from PhysicsTools.NanoAODTools.postprocessing.jon_scr.efficiency_class import efficiency_make as efm
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd #mi servono qua?

for dataset in dataset_list:
    efficiencyer = efm(dataset)
    efficiencyer.efficiency_plotter()