import ROOT
import json
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import awkward as ak
import copy

#################
#    OBJECTS    #
#################
N_bins = 250
luminosity = 137000
dizionario_per_samples = {   
    "QCD_1": "QCDHT_2000toInf_2018",
    "QCD_2": "QCDHT_1500to2000_2018",
    "QCD_3": "QCDHT_1000to1500_2018",
    "QCD_4": "QCDHT_700to1000_2018",
    "QCD_5": "QCDHT_500to700_2018",
    "QCD_6": "QCDHT_300to500_2018",
    "ZJTNN_1": "ZJetsToNuNu_HT200to400_2018",
    "ZJTNN_2": "ZJetsToNuNu_HT400to600_2018",
    "ZJTNN_3": "ZJetsToNuNu_HT600to800_2018",
    "ZJTNN_4": "ZJetsToNuNu_HT800to1200_2018",
    "ZJTNN_5": "ZJetsToNuNu_HT1200to2500_2018",
    "ZJTNN_6": "ZJetsToNuNu_HT2500toInf_2018",
    "ZJTNN_7": "ZJetsToNuNu_HT100to200_2018",
    "TT_1": "TT_Mtt1000toInf_2018",
    "TT_2": "TT_Mtt700to1000_2018",
    "TT_3": "TT_hadr_2018",
    "TT_4": "TT_semilep_2018",
    "TP_1000": "TprimeToTZ_1000_2018",
    "TP_700": "TprimeToTZ_700_2018",
    "TP_1800": "TprimeToTZ_1800_2018"
}

###################
#    FUNCTIONS    #
###################
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

def data_storing(json_file, efficiency, verbose = False):
    data_storage = {} 
    data_names = []
    print("Lettura e storing dei dati...")
    for cluster in json_file["meta_info"]["cluster_names"]:
        print("\n\nCluster " + cluster )
        for index in range(len(json_file[cluster])):
            
            root_file_pathname = json_file["meta_info"]["eos_path"] + 'threshold_outputs/' + str(efficiency) + '/'+ json_file[cluster][index].replace(".txt", ".root")
            
            root_file = ROOT.TFile(root_file_pathname, "Open")
            data_name = json_file[cluster][index].replace(".txt", "")
            data_names.append(data_name)
            if data_name not in data_storage:
                data_storage[data_name] = {}  # Inizializza il dizionario, altrimenti rompe il cazzo

            h_LF = root_file.Get("Lowpt_False"  + data_name)
            h_HF = root_file.Get("Highpt_False" + data_name)

            low_th  = h_LF.GetBinContent(0)
            high_th = h_HF.GetBinContent(0)

            data_storage[data_name]["Low_Threshold"]  = low_th
            data_storage[data_name]["High_Threshold"] = high_th

            if verbose:
                print("\nDataset: " + data_name)
                print("Low Pt Threshold: " + str(data_storage[data_name]["Low_Threshold"]))
                print("High Pt Threshold:" + str(data_storage[data_name]["High_Threshold"]))
    return data_storage, data_names

def saveas_json(dict, filename):
    with open(filename, 'w') as file:
        json.dump(dict, file)

#################
#    Classes    #
#################
class threshold_evalutator:
    '''
    Classe nata per il calcolo della threshold dato un istogramma e una misID probability
    '''
    def __init__(self, histo):
        self.histo = histo

    def threshold_F_seeker(self, bg_efficiency = 0.1, decimal_th = True):
        full_integral = float(self.histo.Integral())
        #print("full integral: " + str(full_integral))
        
        epsilon = 0.001
        th_bin  = 0

        if full_integral < 1e-10: #se histo vuoto deve fermarsi
            print("Warning: Full integral is very close to zero. Cannot evalutate this threshold")
            return th_bin, epsilon
        else:        
            bin_idx = 0
            while epsilon < bg_efficiency and epsilon > 0:
                bin_idx += 1
                right_integral = self.histo.Integral(N_bins - bin_idx, N_bins)
                
                if right_integral > 1e-10 and full_integral > 1e-10:
                    if full_integral != 0:
                        epsilon = right_integral/full_integral
                    else:
                        epsilon = 0

            th_bin = N_bins - bin_idx
            if epsilon == 0:
                print('^^^    impossible to find threshold    ^^^')
            else:
                print("^^^    Trovata la TH al bin: " + str(th_bin) + "   ^^^")
            
            if decimal_th:
                th_double = self.threshold_binTodec(th_bin)
                return th_double, epsilon
            else:
                return th_bin, epsilon

    def threshold_binTodec(self, th_bin):
        unit = 1/(N_bins)
        th_double = th_bin * unit
        return th_double



class thrashold_histomaker:
    '''
    Classe per la creazione ed il salvataggio degli istogrammi necessari alla valutazione della threshold
    '''
    def __init__(self, json_name = "crabout_files.json"):
        self.json_name = json_name
        
    def crea_3_histo(self, 
                    batch_files_list, 
                    h_ds700, #ds = deepscore
                    h_ds1000,
                    h_ds1800,
                    dataset_name,
                    evalutate_threshold = False,
                    bg_efficiency       = 5,
                    N_bins              = 250):
        weight = 0
        for i in range(len(batch_files_list)):
            if i%10 == 0:
                completion_percentage = (i / len(batch_files_list)) * 100
                print(f"Percentuale di completamento dataset: {completion_percentage:.2f}%")
            
            tree = NanoEventsFactory.from_root(batch_files_list[i], schemaclass=NanoAODSchema.v6).events()
            
            rfile = ROOT.TFile.Open(batch_files_list[i])
            weight += (rfile.plots.Get('h_genweight')).GetBinContent(1)
            
            scores_700   = tree.deepsc.tp700
            scores_1000  = tree.deepsc.tp1000
            scores_1800  = tree.deepsc.tp1800

            for score in scores_700:
                h_ds700.Fill(score)
            for score in scores_1000:
                h_ds1000.Fill(score)
            for score in scores_1800:
                h_ds1800.Fill(score)
                
        return weight