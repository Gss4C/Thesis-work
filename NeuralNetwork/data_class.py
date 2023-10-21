import numpy as np
import json
###################
#     General     #
###################
def json_reader(nome_file):
    with open(nome_file, "r") as file:
        contenuto = file.read()
        dizionario = json.loads(contenuto)
        return dizionario
        
def saveas_json(dict, filename):
    with open(filename, 'w') as file:
        json.dump(dict, file)

def read_and_list(path_to_txtfile): 
    '''
    Input a txt file containing a column of filenames and output a strings list with filenames \n
    Python3 necessary
    '''
    lista_file = []
    with open(path_to_txtfile, "r") as file:
        for riga in file:
            riga = riga.strip()
            lista_file.append(riga)
        return lista_file

#############################
#    Parameters & objects   #
#############################
h_th = 0.164000004529953
l_th = 0.23199999332427979

full_jet  = np.zeros((1,6))
full_htop = np.zeros((1, 11))
full_ltop = np.zeros((1, 10))
full_met  = np.zeros((1, 12))
full_label = np.zeros((1,1))

fw_jet  = np.zeros((1,6))
fw_htop = np.zeros((1, 11))
fw_ltop = np.zeros((1, 10))
fw_met  = np.zeros((1, 12))
fw_label = np.zeros((1,1))

nf_jet  = np.zeros((1,6))
nf_htop = np.zeros((1, 11))
nf_ltop = np.zeros((1, 10))
nf_met  = np.zeros((1, 12))
nf_label = np.zeros((1,1))

###################
#    Functions    #
###################
def best_top(collection, key):
    if key == 'high':
        max_score2 = 0
        best_h = 0
        for top in collection:
            if top.score2 > max_score2:
                best_h = top
                max_score2 = top.score2
        return best_h
    if key == 'low':
        max_scoreDNN = 0
        best_l = 0
        for top in collection:
            if top.scoreDNN > max_scoreDNN:
                best_l = top
                max_score2 = top.scoreDNN
        return best_l


def fill_label(dataset = "NONE"):
    '''
    Fill the label tensor for the event: 1 if signal, 0 if background
    '''
    dataset_list = ["TP_700", "TP_1000", "TP_1800"]
    to_append = np.zeros((1,1))
    if dataset in dataset_list:
        to_append[0] = 1
    else:
        to_append[0] = 0
    return to_append

def fill_objects(collection_element, obj_type = "NONE", zeros = False):
    if obj_type == "TopHighPt":
        to_append = np.zeros((1, 11))
        if not zeros:
            to_append[0, 0]  = collection_element.idxFatJet
            to_append[0, 1]  = collection_element.idxJet0
            to_append[0, 2]  = collection_element.idxJet1
            to_append[0, 3]  = collection_element.idxJet2
            to_append[0, 4]  = collection_element.pt
            to_append[0, 5]  = collection_element.eta
            to_append[0, 6]  = collection_element.phi
            to_append[0, 7]  = collection_element.mass
            to_append[0, 8]  = collection_element.truth
            to_append[0, 9]  = collection_element.score2
            to_append[0, 10] = collection_element.thgood
        return to_append

    if obj_type == "TopLowPt":
        to_append = np.zeros((1, 10))
        if not zeros:
            to_append[0, 0]  = collection_element.idxJet0
            to_append[0, 1]  = collection_element.idxJet1
            to_append[0, 2]  = collection_element.idxJet2
            to_append[0, 3]  = collection_element.pt
            to_append[0, 4]  = collection_element.eta
            to_append[0, 5]  = collection_element.phi
            to_append[0, 6]  = collection_element.mass
            to_append[0, 7]  = collection_element.truth
            to_append[0, 8]  = collection_element.scoreDNN
            to_append[0, 9] = collection_element.thgood
        return to_append

    if obj_type == "MET":
        to_append = np.zeros((1, 12))
        if not zeros:
            to_append[0, 0]  = collection_element.MetUnclustEnUpDeltaX
            to_append[0, 1]  = collection_element.MetUnclustEnUpDeltaY
            to_append[0, 2]  = collection_element.covXX
            to_append[0, 3]  = collection_element.covXY
            to_append[0, 4]  = collection_element.covYY
            to_append[0, 5]  = collection_element.phi
            to_append[0, 6]  = collection_element.pt
            to_append[0, 7]  = collection_element.significance
            to_append[0, 8]  = collection_element.sumEt
            #to_append[0, 9]  = collection_element.sumPtUnclustered 
            #only for local
            to_append[0, 9]  = 0
            to_append[0, 10] = collection_element.fiducialGenPhi
            to_append[0, 11] = collection_element.fiducialGenPt
        return to_append

    if obj_type == "Jet":
        to_append = np.zeros((1, 6))
        if not zeros:
            to_append[0, 0]  = collection_element.isGood
            to_append[0, 1]  = collection_element.isForward
            to_append[0, 2]  = collection_element.mass
            to_append[0, 3]  = collection_element.phi
            to_append[0, 4]  = collection_element.pt
            to_append[0, 5]  = collection_element.eta
        return to_append