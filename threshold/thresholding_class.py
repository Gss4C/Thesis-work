import ROOT
import json
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

#################
#    Classes    #
#################

class threshold_evalutator:
    '''
    Classe che dati gli istogrammi (con qualsiasi variabile lungo x) dove ci sono 
    gli eventi True (o di tipo A) e gli eventi False (o di tibo B), permette di 
    gestire tutte le operazioni riguardanti la thrashold per la selezione del segnale
    '''
    def __init__(self, histo_true, histo_false):
        self.histo_true   = histo_true
        self.histo_false  = histo_false
    def threshold_F_seeker(self, n_bins, bg_efficiency = 0.1):
        full_integral = histo_false.Integral()
        epsilon = 0
        bin_idx = 0
        while(epsilon < bg_efficiency):
            bin_idx += 1
            right_integral = histo_false.Integral(n_bins - bin_idx, n_bins)
            epsilon = right_integral/full_integral
        th_bin = n_bins - bin_idx
        return th_bin, epsilon
    
class thrashold_histomaker:
    '''
    Classe per la creazione ed il salvataggio degli istogrammi necessari alla valutazione della threshold
    '''
    def __init__(self, json_name = "crabout_files.json"):
        self.json_name       = json_name

    def json_reader(self, nome_file):
        with open(nome_file, "r") as file:
            contenuto = file.read()
            dizionario = json.loads(contenuto)
            return dizionario
        
    def read_and_list(self, path_to_txtfile): 
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
        
    def crea_4histo(self):
        filenames = self.json_reader(self.json_name)
        root_files = read_and_list(filenames["parent_path"] + filenames["TT_2018"][0]) #qui va aggiunta la possibilità di selezionarsi la monnezza
        
        single_tree  = NanoEventsFactory.from_root(root_files[1], schemaclass=NanoAODSchema.v6).events()
        scores_lowF  = ak.flatten(tree.TopLowPt[(tree.TopLowPt.truth==0)].scoreDNN)
        scores_lowT  = ak.flatten(tree.TopLowPt[(tree.TopLowPt.truth==1)].scoreDNN)
        scores_highF = ak.flatten(tree.TopHighPt[(tree.TopHighPt.truth==0)].score2)
        scores_highT = ak.flatten(tree.TopHighPt[(tree.TopHighPt.truth==1)].score2)

        testing_dataset = filenames["TT_2018"][0]

        h_lowF  = ROOT.TH1F("Lowpt_False" + testing_dataset ,"Lowpt_False" + testing_dataset , 200, 0 ,1)
        h_lowT  = ROOT.TH1F("Lowpt_True" + testing_dataset  ,"Lowpt_True" + testing_dataset  , 200, 0 ,1)
        h_highF = ROOT.TH1F("Highpt_False" + testing_dataset,"Highpt_False" + testing_dataset, 200, 0 ,1)
        h_highT = ROOT.TH1F("Highpt_True" + testing_dataset ,"Highpt_True" + testing_dataset , 200, 0 ,1)
        
        for score_lf, score_lt, scote_hf, score_ht in zip(scores_lowF, scores_lowT, scores_highF, scores_highT):
            '''penso di poter fare uno zip anche con gli histo, devo provare ma ora mi scoccio'''
            h_lowF.Fill(score_lf)
            h_lowT.Fill(score_lt)
            h_highF.Fill(score_hf)
            h_highT.Fill(score_ht)
        return h_lowF, h_lowT, h_highF, h_highT
    