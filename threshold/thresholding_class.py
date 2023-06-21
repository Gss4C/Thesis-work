import ROOT
import json
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import awkward as ak

#################
#    Classes    #
#################

class threshold_evalutator:
    '''
    Classe che dati gli istogrammi (con qualsiasi variabile lungo x) dove ci sono 
    gli eventi True (o di tipo A) e gli eventi False (o di tibo B), permette di 
    gestire tutte le operazioni riguardanti la thrashold per la selezione del segnale
    '''
    def __init__(self, histo_true, histo_false, N_bins = 250):
        self.histo_true  = histo_true
        self.histo_false = histo_false
        self.N_bins = N_bins


    def threshold_F_seeker(self, bg_efficiency = 0.1):
        full_integral = self.histo_false.Integral()
        epsilon = 0
        bin_idx = 0
        while(epsilon < bg_efficiency and epsilon > 0):
            bin_idx += 1
            right_integral = self.histo_false.Integral(self.N_bins - bin_idx, self.N_bins)
            epsilon = right_integral/full_integral if full_integral != 0 else 0
        th_bin = self.N_bins - bin_idx
        return th_bin, epsilon

    def threshold_binTodec(self, th_bin):
        unit = 1/(self.N_bins)
        th_double = th_bin * unit
        return th_double



    
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
        
        
    def crea_4histo(self, batch_files_list, h_lowF, h_lowT, h_highF, h_highT, dataset_name,evalutate_threshold = True, N_bins = 250):
        ############################
        #    Filename Menagment    #
        ############################
        #filenames = self.json_reader(self.json_name)
        #root_files = self.read_and_list(filenames["meta_info"]["parent_path"] + filenames["TT_2018"][1]) #qui va aggiunta la possibilità di selezionarsi la monnezza
        tree  = NanoEventsFactory.from_root(batch_files_list[1], schemaclass=NanoAODSchema.v6).events()
        #testing_dataset = filenames["TT_2018"][1].replace(".txt","") #nome file txt

        ########################
        #    Histo Creation    #
        ########################
        if ak.any(tree.TopLowPt.scoreDNN):
            scores_lowF  = ak.flatten(tree.TopLowPt[(tree.TopLowPt.truth==0)].scoreDNN)
            scores_lowT  = ak.flatten(tree.TopLowPt[(tree.TopLowPt.truth==1)].scoreDNN)

        else:
            scores_lowF  = []
            scores_lowT  = []
        if ak.any(tree.TopHighPt.score2):
            scores_highF = ak.flatten(tree.TopHighPt[(tree.TopHighPt.truth==0)].score2)
            scores_highT = ak.flatten(tree.TopHighPt[(tree.TopHighPt.truth==1)].score2)
        else:
            scores_highF  = []
            scores_highT  = []
        #print('DEBUG: Salto la creazione degli istogrammi, returno cose vuote a caso')
        #print('print del comando ROOT.gDirectory.pwd()')
        #print(ROOT.gDirectory.pwd())
        '''
        h_lowF  = ROOT.TH1F("Lowpt_False" + dataset_name ,"Lowpt_False" + dataset_name , N_bins, 0 ,1)
        h_lowT  = ROOT.TH1F("Lowpt_True" + dataset_name  ,"Lowpt_True" + dataset_name  , N_bins, 0 ,1)
        h_highF = ROOT.TH1F("Highpt_False" + dataset_name,"Highpt_False" + dataset_name, N_bins, 0 ,1)
        h_highT = ROOT.TH1F("Highpt_True" + dataset_name ,"Highpt_True" + dataset_name , N_bins, 0 ,1)
        '''
        for score_lf, score_lt, score_hf, score_ht in zip(scores_lowF, scores_lowT, scores_highF, scores_highT):
            if ak.any(scores_lowF):  h_lowF.Fill(score_lf)
            if ak.any(scores_lowT):  h_lowT.Fill(score_lt)
            if ak.any(scores_highF): h_highF.Fill(score_hf)
            if ak.any(scores_highT): h_highT.Fill(score_ht)
        
        
        ########################
        #    Calcolo Soglie    #    
        ########################
        if evalutate_threshold:
            LowEval = threshold_evalutator(N_bins      = N_bins,
                                           histo_true  = h_lowT,
                                           histo_false = h_lowF)
            HighEval = threshold_evalutator(N_bins      = N_bins, 
                                            histo_true  = h_highT, 
                                            histo_false = h_highF)
            print("istanziati gli oggetti")

            LowTh_Bin,  LowEpsilon  = LowEval.threshold_F_seeker()
            print("trovate le threshold")
            LowTh = LowEval.threshold_binTodec(LowTh_Bin)
            h_lowF.SetBinContent(0,LowTh)
            h_lowT.SetBinContent(0,LowTh)
            

            HighTh_Bin, HighEpsilon = HighEval.threshold_F_seeker()
            HighTh = HighEval.threshold_binTodec(HighTh_Bin)
            h_highF.SetBinContent(0,HighTh)
            h_highT.SetBinContent(0,HighTh)