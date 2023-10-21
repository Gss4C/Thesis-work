import os
import sys
import ROOT
from array import array
import numpy as np
import pickle as pkl
from PhysicsTools.NanoAODTools.postprocessing.Thesis.NeuralNetwork.data_class import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *

crabout = json_reader("crabout_files.json")
with open(crabout["meta_info"]["eos_nn"] + "pkl_files/" + "TP_1800.pkl", 'rb') as f:
    data = pkl.load(f)
    print(np.shape(data["TP_1800"][0]))
    print(np.shape(data["TP_1800"][1]))
    print(np.shape(data["TP_1800"][2]))
    print(np.shape(data["TP_1800"][3]))
    print('\nPrint delle varie cose\nPrint della label:')
    print(data["TP_1800"][3])