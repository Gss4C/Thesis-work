import os
import sys
import ROOT
import argparse
from array import array
import numpy as np
import pickle as pkl
from PhysicsTools.NanoAODTools.postprocessing.Thesis.NeuralNetwork.data_class import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
    
parser = argparse.ArgumentParser(description = "PKL file creation")
parser.add_argument("-c", "--cluster",
                    type     = str,
                    help     = "Cluster you want to pickle",
                    required = True)
options = parser.parse_args()

crabout = json_reader("crabout_files.json")
files_list = read_and_list(crabout["meta_info"]["parent_path"] + crabout[options.cluster][0])
weight = 0

for number, batch_file in enumerate(files_list):
    # Lettura singolo file
    rfile = ROOT.TFile.Open(batch_file)
    tree = InputTree(rfile.Get("Events"))
    print("Acquisizione batchfile " + str(number) + "/" + str(len(files_list)) )

    weight += (rfile.plots.Get('h_genweight')).GetBinContent(1)
    
    # Valutazione evento per evento
    for i in range(tree.GetEntries()):
        if i%1000 == 0:
            print("Event: " + str(i) + '/' + str(tree.GetEntries()) + '     ' + 'Completamento batch: ' + str(i/(tree.GetEntries()) * 100 ))

        event = Event(tree, i)
        top_hpt = Collection(event,"TopHighPt")
        top_lpt = Collection(event,"TopLowPt")
        jets = Collection(event,"Jet")
        met = Object(event, "MET")
        
        ##############################
        #    Acquisizione oggetti    #
        ##############################
        if (len(top_hpt) == 0) and (len(top_lpt) == 0): continue

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

        ############################
        #    TEMP Array Filling    #
        ############################
        #    No region division    #
        ############################
        if best_htop == 0:
            temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = True)
        elif (best_htop.score2 >= h_th):
            temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = False)
        elif (best_htop.score2 < h_th):
            temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = True)

        if best_ltop == 0:
            temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = True)
        elif (best_ltop.scoreDNN >= h_th): 
            temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = False)
        elif (best_ltop.scoreDNN < h_th): 
            temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = True)
        
        if best_jet == 0:
            temp_jet = fill_objects(collection_element = best_jet, obj_type = "Jet", zeros = True)
        else:
            temp_jet = fill_objects(collection_element = best_jet, obj_type = "Jet", zeros = False)
            
        temp_met    = fill_objects(collection_element = met, obj_type = "MET", zeros = False)
        temp_label  = fill_label(dataset = options.cluster)

        full_htop  = np.append(full_htop,  temp_tophpt, axis = 0)
        full_ltop  = np.append(full_ltop,  temp_toplpt, axis = 0)
        full_jet   = np.append(full_jet,   temp_jet,    axis = 0)
        full_met   = np.append(full_met,   temp_met,    axis = 0)
        full_label = np.append(full_label, temp_label,  axis = 0)
        

        #########################
        #    Region Division    #
        #########################
        #    Forward    #
        #################
        if hasattr(best_jet, 'isForward'):
            if best_htop == 0:
                temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = True)
            elif (best_htop.score2 >= h_th):
                temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = False)
            elif (best_htop.score2 < h_th):
                temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = True)

            if best_ltop == 0:
                temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = True)
            elif (best_ltop.scoreDNN >= h_th): 
                temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = False)
            elif (best_ltop.scoreDNN < h_th): 
                temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = True)
            
            temp_jet = fill_objects(collection_element = best_jet, obj_type = "Jet", zeros = False)
            temp_met    = fill_objects(collection_element = met, obj_type = "MET", zeros = False)
            temp_label  = fill_label(dataset = options.cluster)

            fw_htop = np.append(fw_htop, temp_tophpt, axis = 0)
            fw_ltop = np.append(fw_ltop, temp_toplpt, axis = 0)
            fw_jet  = np.append(fw_jet,  temp_jet,    axis = 0)
            fw_met  = np.append(fw_met,  temp_met,    axis = 0)
            fw_label = np.append(fw_label, temp_label,  axis = 0)
            
        
        #####################
        #    Non forward    #
        #####################
        else:
            if best_htop == 0:
                temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = True)
            elif (best_htop.score2 >= h_th):
                temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = False)
            elif (best_htop.score2 < h_th):
                temp_tophpt = fill_objects(collection_element = best_htop, obj_type = "TopHighPt", zeros = True)

            if best_ltop == 0:
                temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = True)
            elif (best_ltop.scoreDNN >= h_th): 
                temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = False)
            elif (best_ltop.scoreDNN < h_th): 
                temp_toplpt = fill_objects(collection_element = best_ltop, obj_type = "TopLowPt", zeros = True)
            
            temp_jet = fill_objects(collection_element = best_jet, obj_type = "Jet", zeros = True)
            temp_met    = fill_objects(collection_element = met, obj_type = "MET", zeros = False)
            temp_label  = fill_label(dataset = options.cluster)

            nf_htop = np.append(nf_htop, temp_tophpt, axis = 0)
            nf_ltop = np.append(nf_ltop, temp_toplpt, axis = 0)
            nf_jet  = np.append(nf_jet,  temp_jet,    axis = 0)
            nf_met  = np.append(nf_met,  temp_met,    axis = 0)
            nf_label = np.append(nf_label, temp_label,  axis = 0)

nf_list  = [nf_htop, nf_ltop, nf_jet, nf_met, nf_label, weight]
fw_list  = [fw_htop, fw_ltop, fw_jet, fw_met, fw_label, weight]
full_list  = [full_htop, full_ltop, full_jet, full_met, full_label, weight]
            

categories = ['full', 'forward', 'noforward']
output = {c: {} for c in categories} 
output['full'][options.cluster]      = full_list
output['forward'][options.cluster]   = fw_list
output['noforward'][options.cluster] = nf_list

#effettivo salvataggio del file pkl 
output_file = open(crabout["meta_info"]["eos_nn"] + "pkl_files/" + options.cluster + ".pkl", "wb")
pkl.dump(output, output_file)
output_file.close()
rfile.Close()
'''
output_file = open('TEST' + options.cluster + ".pkl", "wb")
pkl.dump(output, output_file)
output_file.close()
rfile.Close()
'''
## test per vedere se fa bene
print("Processo completo.\nPrint test...")
with open(crabout["meta_info"]["eos_nn"] + "pkl_files/" + options.cluster + ".pkl", 'rb') as f:
    data = pkl.load(f)
    print('Caso full:')
    print(np.shape(data['full'][options.cluster][0]))
    print(np.shape(data['full'][options.cluster][1]))
    print(np.shape(data['full'][options.cluster][2]))
    print(np.shape(data['full'][options.cluster][3]))
    print(np.shape(data['full'][options.cluster][4]))
    print(np.shape(data['full'][options.cluster][5]))
    print(data['full'][options.cluster][5])

    print('Caso Forward:')
    print(np.shape(data['forward'][options.cluster][0]))
    print(np.shape(data['forward'][options.cluster][1]))
    print(np.shape(data['forward'][options.cluster][2]))
    print(np.shape(data['forward'][options.cluster][3]))
    print(np.shape(data['forward'][options.cluster][4]))
    print(np.shape(data['forward'][options.cluster][5]))

    print('Caso Non Forward:')
    print(np.shape(data['noforward'][options.cluster][0]))
    print(np.shape(data['noforward'][options.cluster][1]))
    print(np.shape(data['noforward'][options.cluster][2]))
    print(np.shape(data['noforward'][options.cluster][3]))
    print(np.shape(data['noforward'][options.cluster][4]))
    print(np.shape(data['noforward'][options.cluster][5]))