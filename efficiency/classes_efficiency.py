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
        
def conditions(collection_high, collection_low, low_th, high_th):
    h_fwd = False
    l_fwd = False
    for top in collection_high: #score2
        if (abs(top.eta) > 2.5 and abs(top.eta) < 4 and top.score2 > high_th):
            h_fwd = True
    for top in collection_low: #scoreDNN
        if (abs(top.eta) > 2.5 and abs(top.eta) < 4 and top.scoreDNN > low_th):
            l_fwd = True
    return h_fwd, l_fwd

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


def plotter(hf, h, lf, l, th, dataset = 'No dataset', path = './'):
    efficienze = {}
    efficienze["TopHighPt"] = [hf*100, h*100]
    efficienze["TopLowPt"]  = [lf*100, l*100]
    df = pd.DataFrame(data=efficienze, index=['fwd', 'not_fwd'])

    plt.rcParams["figure.figsize"]    = [8, 5] 
    plt.rcParams["figure.autolayout"] = True 
    plt.title("Efficiencies (%) " + dataset) 

    plot = sns.heatmap(df, cmap='YlGnBu',annot=True)
    plt.savefig(path +'eff_' + str(th) +"_" +dataset + '.png')
    plt.close()
    print('Plot successfully saved')