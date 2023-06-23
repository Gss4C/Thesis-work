import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.threshold.thresholding_class import *

import warnings
warnings.filterwarnings("ignore")

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

filenames = json_reader("crabout_files.json")

for cluster in filenames["meta_info"]["cluster_names"]:
    print("\ninizio del cluster:" + cluster + "\n")
    for index in range(len(filenames[cluster])):
        completamento = index/(len(filenames[cluster]))
        percentuale   = completamento*100
        print("Completamento cluster: " + str(percentuale) + "%")
        
        batch_files_list = read_and_list(filenames["meta_info"]["parent_path"] + filenames[cluster][index])
        #testing_dataset  = filenames[cluster][index].replace(".txt","")
        dataset_name  = filenames[cluster][index].replace(".txt","")
        root_filename    = filenames[cluster][index].replace(".txt",".root") 

        N_bins = 250
        h_lowF  = ROOT.TH1F("Lowpt_False" + dataset_name ,"Lowpt_False" + dataset_name , N_bins, 0 ,1)
        h_lowT  = ROOT.TH1F("Lowpt_True" + dataset_name  ,"Lowpt_True" + dataset_name  , N_bins, 0 ,1)
        h_highF = ROOT.TH1F("Highpt_False" + dataset_name,"Highpt_False" + dataset_name, N_bins, 0 ,1)
        h_highT = ROOT.TH1F("Highpt_True" + dataset_name ,"Highpt_True" + dataset_name , N_bins, 0 ,1)

        histomaker = thrashold_histomaker()
        histomaker.crea_4histo(batch_files_list, h_lowF, h_lowT, h_highF, h_highT, dataset_name)

        file = ROOT.TFile("/eos/user/j/jbonetti/Th_outputs/" + root_filename, "RECREATE")
        
        h_highF.Write()
        h_highT.Write()
        h_lowF.Write()
        h_lowT.Write()
        
        file.Close()
        print('DONE')

#batch_files_list = read_and_list(filenames["meta_info"]["parent_path"] + filenames["TT_2018"][1])
#testing_dataset = filenames["TT_2018"][1].replace(".txt","")
#file = ROOT.TFile("/eos/user/j/jbonetti/Th_outputs/out_test_01.root", "RECREATE")
#histomaker = thrashold_histomaker()
#h_lowF, h_lowT, h_highF, h_highT = histomaker.crea_4histo()
#h_highF.Write()
#h_highT.Write()
#h_lowF.Write()
#h_lowT.Write()
#file.Close()