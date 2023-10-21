import json
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import awkward as ak
import copy
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object

luminosity = 137000 #bp^-1
l_th = 0.23199999332427979
h_th = 0.164000004529953
N_bins = 1000

type_sample = { #servono solo per il colore
    "2": "QCDHT_700to1000_2018",
    "1": "TT_hadr_2018",
    "0": "ZJetsToNuNu_HT600to800_2018"
}

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

def scaling_factor(sample_dict, name_string, luminosity, weight):
    sigma = sample_dict[name_string].sigma
    sl = sigma*luminosity
    if weight != 0:
        k = sl/weight
    else:
        k = 1
    return k


def histo_adder(h_700,h_1000,h_1800,h_met, h_ds700,h_ds1000,h_ds1800, h_met_pt):
    h_ds700.Add(h_700)
    h_ds1000.Add(h_1000)
    h_ds1800.Add(h_1800)
    h_met_pt.Add(h_met)
        
class stack_plotter:
    '''
    Classe per la creazione ed il salvataggio degli istogrammi necessari alla valutazione della threshold
    '''
    def __init__(self):
        pass
        
    def fill_4_histos(self, 
                      batch_files_list, 
                      h_ds700, 
                      h_ds1000,
                      h_ds1800,
                      h_met,
                      dataset_name):
        weight = 0
        for i in range(len(batch_files_list)):
            if i%10 == 0:
                completion_percentage = (i / len(batch_files_list)) * 100
                print(f"Percentuale di completamento dataset: {completion_percentage:.2f}%")
            
            #tree = NanoEventsFactory.from_root(batch_files_list[i], schemaclass=NanoAODSchema.v6).events()
            
            rfile = ROOT.TFile.Open(batch_files_list[i])
            tree = rfile.Events
            weight += (rfile.plots.Get('h_genweight')).GetBinContent(1)
            
            #[ak.any(tree.TopLowPt.scoreDNN > l_th) or ak.any(tree.TopHighPt.score2 > h_th)]
            #print(tree.TopLowPt.scoreDNN)
            #print(type(tree.TopLowPt.scoreDNN))
            #if(ak.any(tree.TopLowPt.scoreDNN > l_th) or ak.any(tree.TopHighPt.score2 > h_th)):
            #l'unica cosa che posso fare è andare evento per evento
            '''
            selected_indices = ak.where((tree.TopLowPt.scoreDNN > l_th) | (tree.TopHighPt.score2 > h_th))
            scores_700   = tree.deepsc.tp700[selected_indices]
            scores_1000  = tree.deepsc.tp1000[selected_indices]
            scores_1800  = tree.deepsc.tp1800[selected_indices]
            met = tree.MET.pt[selected_indices]

            for score in scores_700:
                h_ds700.Fill(score)
            for score in scores_1000:
                h_ds1000.Fill(score)
            for score in scores_1800:
                h_ds1800.Fill(score)
            for pt in met:
                h_met.Fill(pt)
            '''
            scores_700 = []
            scores_1000 = []
            scores_1800 = []
            met_values = []
            #for event in range(tree.GetEntries()):
            for event in range(100):
                tree.GetEntry(event)
                if event%1000 == 0 and tree.GetEntries() != 0:
                    percentuale = round(float(event/tree.GetEntries() * 100),2)
                    print("Completamento batch: " + str(percentuale) + '%')
                tophigh = Collection(tree, "TopHighPt")
                toplow  = Collection(tree, "TopLowPt")

                cond_high, cond_low = top_conditions(collection_high = tophigh, collection_low = toplow, low_th = l_th, high_th = h_th)

                if (cond_high or cond_low):
                    met  = Object(tree, "MET")
                    deepsc  = Object(tree, "deepsc")
                    scores_700.append(deepsc.tp700)
                    scores_1000.append(deepsc.tp1000)
                    scores_1800.append(deepsc.tp1800)
                    met_values.append(met.pt)

            for score in scores_700:
                h_ds700.Fill(score)
            for score in scores_1000:
                h_ds1000.Fill(score)
            for score in scores_1800:
                h_ds1800.Fill(score)
            for pt in met_values:
                h_met.Fill(pt)
            
        return weight