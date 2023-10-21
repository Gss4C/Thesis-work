import os
import ROOT
import math
import numpy as np
import keras.models
from array import array
from itertools import combinations, chain
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.Thesis.NeuralNetwork.training.dnn_utils import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.NeuralNetwork.data_class import *
from PhysicsTools.NanoAODTools.postprocessing.tools import *
ROOT.PyConfig.IgnoreCommandLineOptions = True 

#models_local_path = "%s/src/PhysicsTools/NanoAODTools/scripts/" % os.environ['CMSSW_BASE']
models_local_path = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/dict_tresholds/" % os.environ['CMSSW_BASE']

model_700  = keras.models.load_model(models_local_path +  model_name_700 + ".h5")
model_1000 = keras.models.load_model(models_local_path + model_name_1000 + ".h5")
model_1800 = keras.models.load_model(models_local_path + model_name_1800 + ".h5")

class tmet_dnn_evaluate:
    '''
    Evaluate 3 DNN models trained to recognize Tprime 700, 1000 and 1800 GeV. \n
    Whis module calculate 3 different scores, one each signal:\n
    - deepsc_tp700
    - deepsc_tp1000
    - deepsc_tp1800
    '''
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("deepsc_tp700",  "D")
        self.out.branch("deepsc_tp1000", "D")
        self.out.branch("deepsc_tp1800", "D")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        top_hpt = Collection(event,"TopHighPt")
        top_lpt = Collection(event,"TopLowPt")
        jets    = Collection(event,"Jet")
        met     = Object(event, "MET")

        ############################
        #     creating objects     #
        ############################
        if len(top_hpt) != 0: 
            best_htop = best_top(top_hpt, 'high')
        elif len(top_hpt) == 0:
            best_htop = 0

        if len(top_lpt) != 0: 
            best_ltop = best_top(top_lpt, 'low')
        elif len(top_lpt) == 0:
            best_ltop = 0

        best_jet = 0
        g_jet_list = []
        for jet in jets:
            if jet.isGood and jet.isForward:
                g_jet_list.append(jet)
        if len(g_jet_list):
            best_jet = g_jet_list[0]

        if best_htop == 0:
            dnn_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = True)
        elif (best_htop.score2 >= h_th):
            dnn_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = False)
        elif (best_htop.score2 < h_th):
            dnn_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = True)

        if best_ltop == 0:
            dnn_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = True)
        elif (best_ltop.scoreDNN >= h_th): 
            dnn_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = False)
        elif (best_ltop.scoreDNN < h_th): 
            dnn_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = True)
        
        if best_jet == 0:
            dnn_jet = fill_objects(collection_element = best_jet, obj_type = "Jet", zeros = True)
        else:
            dnn_jet = fill_objects(collection_element = best_jet, obj_type = "Jet", zeros = False)
            
        dnn_met    = fill_objects(collection_element = met, obj_type = "MET", zeros = False)
        
        deepsc_tp700  = model_700.predict({'Top_High_pt': dnn_tophpt, 'Top_Low_pt': dnn_toplpt, 'Jet': dnn_jet, 'MET': dnn_met})
        deepsc_tp1000 = model_1000.predict({'Top_High_pt': dnn_tophpt, 'Top_Low_pt': dnn_toplpt, 'Jet': dnn_jet, 'MET': dnn_met})
        deepsc_tp1800 = model_1800.predict({'Top_High_pt': dnn_tophpt, 'Top_Low_pt': dnn_toplpt, 'Jet': dnn_jet, 'MET': dnn_met})

        self.out.fillBranch("deepsc_tp700",  deepsc_tp700)
        self.out.fillBranch("deepsc_tp1000", deepsc_tp1000)
        self.out.fillBranch("deepsc_tp1800", deepsc_tp1800)

        return True