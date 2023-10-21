import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

###################
#    FUNCTIONS    #
###################
def get_key_string(diz, key):
    for k, v in diz.items():
        if v is key:
            return k
            
def json_reader(nome_file):
    with open(nome_file, "r") as file:
        contenuto = file.read()
        dizionario = json.loads(contenuto)
        return dizionario
def read_and_list(path_to_txtfile): 
    '''
    Input to a txt file containing a column and output a strings list \n
    Python3 necessary
    '''
    lista_file = []
    with open(path_to_txtfile, "r") as file:
        for riga in file:
            riga = riga.strip()
            lista_file.append(riga)
        return lista_file

def saveas_json(dict, filename):
    with open(filename, 'w') as file:
        json.dump(dict, file)

def top_conditions(collection_high, collection_low, low_th, high_th):
    cond_high = False
    cond_low = False
    for top in collection_high: #score2
        if (top.score2 > high_th):
            cond_high = True
    for top in collection_low: #scoreDNN
        if (top.scoreDNN > low_th):
            cond_low = True
    return cond_high, cond_low

def conditions(scores_object, threshold_dict):
    valid_700 = False
    valid_1000 = False
    valid_1800 = False
    if scores_object.tp700 >= threshold_dict['th_700']:
        valid_700 = True
    if scores_object.tp1000 >= threshold_dict['th_1000']:
        valid_1000 = True
    if scores_object.tp1800 >= threshold_dict['th_1800']:
        valid_1800 = True
    return valid_700, valid_1000, valid_1800

def is_event_fwd(collection_jets):
    fwd = False
    for jet in collection_jets:
        if jet.isForward:
            fwd = True
    return fwd
'''
def conditions_fwdj(collection_high, collection_low, collection_jets, low_th, high_th):
    h_fwd = False
    l_fwd = False
    for top in collection_high: #score2
        if (top.score2 > high_th):
            for jet in collection_jets:
                if (abs(jet.eta) > 2.5 and abs(jet.eta) < 4):
                    h_fwd = True
    for top in collection_low: #scoreDNN
        if (top.scoreDNN > low_th):
            for jet in collection_jets:
                if (abs(jet.eta) > 2.5 and abs(jet.eta) < 4):
                    l_fwd = True
    return h_fwd, l_fwd
'''

def plotter(e7f, e7, e10f, e10, e18f, e18, th, dataset = 'No dataset', path = './'):
    efficienze = {}
    efficienze["score_tp700"]  = [e7f  * 100, e7 * 100]
    efficienze["score_tp1000"] = [e10f * 100, e10 * 100]
    efficienze["score_tp1800"] = [e18f * 100, e18 * 100]

    #efficienze["TopHighPt"] = [hf*100, h*100]
    #efficienze["TopLowPt"]  = [lf*100, l*100]
    df = pd.DataFrame(data=efficienze, index=['fwd', 'not_fwd'])

    plt.rcParams["figure.figsize"]    = [8, 5] 
    plt.rcParams["figure.autolayout"] = True 
    plt.title("Efficiencies (%) " + dataset) 

    plot = sns.heatmap(df, cmap='YlGnBu',annot=True)
    plt.savefig(path+ 'plots/eff_' + str(th) +"_" + dataset + '.png')
    plt.close()
    print('Plot successfully saved')