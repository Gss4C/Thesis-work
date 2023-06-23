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
        full_integral = float(self.histo_false.Integral())
        print("full integral: " + str(full_integral))
        
        epsilon = 0.001
        th_bin  = 0

        if full_integral < 1e-10: #se l'histo è vuoto deve fermarsi
            print("Warning: Full integral is very close to zero. Cannot evalutate this threshold")
            return th_bin, epsilon
        else:        
            bin_idx = 0
            while epsilon < bg_efficiency and epsilon > 0:
                bin_idx += 1
                right_integral = self.histo_false.Integral(self.N_bins - bin_idx, self.N_bins)
                
                if right_integral > 1e-10 and full_integral > 1e-10:
                    if full_integral != 0:
                        epsilon = right_integral/full_integral
                    else:
                        epsilon = 0

            th_bin = self.N_bins - bin_idx
            if epsilon == 0:
                print('^^^^    impossible to find threshold    ^^^^')
                print("FAIL")
            else:
                print("^^^    Trovata la TH al bin: " + str(th_bin) + "   ^^^")
                print("SUCCESS")
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
        for i in range(len(batch_files_list)):
            if i%10 == 0:
                completion_percentage = (i / len(batch_files_list)) * 100
                print(f"Percentuale di completamento dataset: {completion_percentage:.2f}%")
            
            tree = NanoEventsFactory.from_root(batch_files_list[i], schemaclass=NanoAODSchema.v6).events()
            #print(len(tree))
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

            for score_lf in scores_lowF:
                h_lowF.Fill(score_lf)
            for score_lt in scores_lowT:
                h_lowT.Fill(score_lt)
            for score_hf in scores_highF:
                h_highF.Fill(score_hf)
            for score_ht in scores_highT:
                h_highT.Fill(score_ht)

        ########################
        #    Calcolo Soglie    #    
        ########################
        print('Inizio calcolo soglie per il dataset...')
        if evalutate_threshold:
            LowEval = threshold_evalutator(N_bins      = N_bins,
                                            histo_true  = h_lowT,
                                            histo_false = h_lowF)
            HighEval = threshold_evalutator(N_bins      = N_bins, 
                                            histo_true  = h_highT, 
                                            histo_false = h_highF)

            LowTh_Bin,  LowEpsilon  = LowEval.threshold_F_seeker()
            LowTh = LowEval.threshold_binTodec(LowTh_Bin)
            print("Soglia in decimale di Low: " + str(LowTh))
            h_lowF.SetBinContent(0,LowTh)
            h_lowT.SetBinContent(0,LowTh)

            HighTh_Bin, HighEpsilon = HighEval.threshold_F_seeker()
            HighTh = HighEval.threshold_binTodec(HighTh_Bin)
            print("Soglia in decimale di High: " + str(HighTh))
            h_highF.SetBinContent(0,HighTh)
            h_highT.SetBinContent(0,HighTh)