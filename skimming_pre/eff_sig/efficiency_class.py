from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class efficiency_maker:
    '''
    Contatore delle efficienze. Segue l'elenco delle funzioni (in output danno le efficienze da mettere nel grafico): \n
    counter_32() \n
    counter_32btag()\n
    counter_deep()\n
    counter_deepbtag()\n
    '''
    def __init__(self, nome_file, nome_hist):
        self.nome_file = nome_file
        self.nome_hist = nome_hist
        self.resolved_fwd = 0 
        self.resolved_nfw = 0 
        self.boost_fwd    = 0 
        self.boost_nfw    = 0

        self.percorso  = "/afs/cern.ch/user/j/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab"
    def dammi_il_boolean(self, small_tree, jets, key = 0):
        if key == 0: #tau 32
            if(small_tree.Boosted_tau32):
                    BST = True
                if(small_tree.Resolved and not small_tree.Boosted_tau32):
                    RSL = True
                for jet in jets:
                    if jet.isForward and jet.isGood:
                        is_fwd = True
            return BST, RSL, is_fwd
        
        elif key == 1: #tau 32 btag
            if(small_tree.Boosted_tau32btag):
                    BST = True
                if(small_tree.Resolved and not small_tree.Boosted_tau32btag):
                    RSL = True
                for jet in jets:
                    if jet.isForward and jet.isGood:
                        is_fwd = True
            return BST, RSL, is_fwd
        
        elif key == 2: #deep
            if(small_tree.Boosted_deeptag):
                    BST = True
                if(small_tree.Resolved and not small_tree.Boosted_deeptag):
                    RSL = True
                for jet in jets:
                    if jet.isForward and jet.isGood:
                        is_fwd = True
            return BST, RSL, is_fwd
        
        elif key == 3: #deep btag
            if(small_tree.Boosted_deeptagbtag):
                    BST = True
                if(small_tree.Resolved and not small_tree.Boosted_deeptagbtag):
                    RSL = True

                for jet in jets:
                    if jet.isForward and jet.isGood:
                        is_fwd = True
            return BST, RSL, is_fwd
        
    def counter_32(self, sig):
        self.resolved_fwd = 0 
        self.resolved_nfw = 0 
        self.boost_fwd    = 0 
        self.boost_nfw    = 0

        histo_file   = ROOT.TFile(self.percorso + self.nome_hist,"Open")
        skimmed_file = ROOT.TFile(self.percorso + self.nome_file,"Open")
        histos = histo_file.plots.Get("h_genweight")
        weight = histos.GetBinContent(1)
        small_tree = skimmed_file.Events

        for event in range(small_tree.GetEntries()):
            small_tree.GetEntry(event)
            jets   = Collection(small_tree, "Jet")
            BST    = False
            RSL    = False
            is_fwd = False
            
            BST, RSL, is_fwd = self.dammi_il_boolean(small_tree = small_tree, jets=jets , key=0)

            ##############
            ## Counting ##
            ##############
            if BST:
                if is_fwd:
                    self.boost_fwd  += 1
                else:
                    self.boost_nfw += 1
            if RSL:
                if is_fwd:
                    self.resolved_fwd  += 1
                else:
                    self.resolved_nfw += 1
        eff_b_w_fj  = float(self.boost_fwd)/weight
        eff_b_wo_fj = float(self.boost_nfw)/weight
        eff_r_w_fj  = float(self.resolved_fwd)/weight
        eff_r_wo_fj = float(self.resolved_nfw)/weight
        if sig:
            return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, self.boost_fwd, self.boost_nfw, self.resolved_fwd, self.resolved_nfw, weight
        else:
            return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj
    def counter_32btag(self, sig):
        self.resolved_fwd = 0 
        self.resolved_nfw = 0 
        self.boost_fwd    = 0 
        self.boost_nfw    = 0

        histo_file   = ROOT.TFile(self.percorso + self.nome_hist,"Open")
        skimmed_file = ROOT.TFile(self.percorso + self.nome_file,"Open")
        histos = histo_file.plots.Get("h_genweight")
        weight = histos.GetBinContent(1)
        small_tree = skimmed_file.Events

        for event in range(small_tree.GetEntries()):
            small_tree.GetEntry(event)
            jets   = Collection(small_tree, "Jet")
            BST    = False
            RSL    = False
            is_fwd = False

            BST, RSL, is_fwd = self.dammi_il_boolean(small_tree = small_tree, jets=jets , key=1)
            ##############
            ## Counting ##
            ##############
            if BST:
                if is_fwd:
                    self.boost_fwd  += 1
                else:
                    self.boost_nfw += 1
            if RSL:
                if is_fwd:
                    self.resolved_fwd  += 1
                else:
                    self.resolved_nfw += 1
        eff_b_w_fj  = float(self.boost_fwd)/weight
        eff_b_wo_fj = float(self.boost_nfw)/weight
        eff_r_w_fj  = float(self.resolved_fwd)/weight
        eff_r_wo_fj = float(self.resolved_nfw)/weight
        if sig:
            return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, self.boost_fwd, self.boost_nfw, self.resolved_fwd, self.resolved_nfw, weight
        else:
            return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj
    def counter_deep(self, sig):
        self.resolved_fwd = 0 
        self.resolved_nfw = 0 
        self.boost_fwd    = 0 
        self.boost_nfw    = 0

        histo_file   = ROOT.TFile(self.percorso + self.nome_hist,"Open")
        skimmed_file = ROOT.TFile(self.percorso + self.nome_file,"Open")
        histos = histo_file.plots.Get("h_genweight")
        weight = histos.GetBinContent(1)
        small_tree = skimmed_file.Events

        for event in range(small_tree.GetEntries()):
            small_tree.GetEntry(event)
            jets   = Collection(small_tree, "Jet")
            BST    = False
            RSL    = False
            is_fwd = False

            BST, RSL, is_fwd = self.dammi_il_boolean(small_tree = small_tree, jets=jets , key=2)
            ##############
            ## Counting ##
            ##############
            if BST:
                if is_fwd:
                    self.boost_fwd  += 1
                else:
                    self.boost_nfw += 1
            if RSL:
                if is_fwd:
                    self.resolved_fwd  += 1
                else:
                    self.resolved_nfw += 1
        eff_b_w_fj  = float(self.boost_fwd)/weight
        eff_b_wo_fj = float(self.boost_nfw)/weight
        eff_r_w_fj  = float(self.resolved_fwd)/weight
        eff_r_wo_fj = float(self.resolved_nfw)/weight
        if sig:
            return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, self.boost_fwd, self.boost_nfw, self.resolved_fwd, self.resolved_nfw, weight
        else:
            return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj
    def counter_deepbtag(self, sig):
        self.resolved_fwd = 0 
        self.resolved_nfw = 0 
        self.boost_fwd    = 0 
        self.boost_nfw    = 0

        histo_file   = ROOT.TFile(self.percorso + self.nome_hist,"Open")
        skimmed_file = ROOT.TFile(self.percorso + self.nome_file,"Open")
        histos = histo_file.plots.Get("h_genweight")
        weight = histos.GetBinContent(1)
        small_tree = skimmed_file.Events

        for event in range(small_tree.GetEntries()):
            small_tree.GetEntry(event)
            jets   = Collection(small_tree, "Jet")
            BST    = False
            RSL    = False
            is_fwd = False

            BST, RSL, is_fwd = self.dammi_il_boolean(small_tree = small_tree, jets=jets , key=3)

            ##############
            ## Counting ##
            ##############
            if BST:
                if is_fwd:
                    self.boost_fwd  += 1
                else:
                    self.boost_nfw += 1
            if RSL:
                if is_fwd:
                    self.resolved_fwd  += 1
                else:
                    self.resolved_nfw += 1
        eff_b_w_fj  = float(self.boost_fwd)/weight
        eff_b_wo_fj = float(self.boost_nfw)/weight
        eff_r_w_fj  = float(self.resolved_fwd)/weight
        eff_r_wo_fj = float(self.resolved_nfw)/weight
        if sig:
            return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, self.boost_fwd, self.boost_nfw, self.resolved_fwd, self.resolved_nfw, weight
        else:
            return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj
        
class significancer:
    def __init__(self, mini_sample):
        self.mini_sample = mini_sample
        self.L_run2 = 138
    def normalize_counting(self, n_sel = 10 , n_tot = 10):
        norm_count = n_sel * self.mini_sample.sigma * self.L_run2 / n_tot
        return norm_count

class efficiency_plot:
    def __init__(self, mini_sample): #devo ricordare di cambiare i nomi dai datasets
        self.mini_sample = mini_sample

    def skim_name(self):
        #name_string = self.mini_sample.name
        skim = self.mini_sample.name.replace(".root","_Skim.root")
        return skim
    def hist_name(self):
        histo = "hist_out_" + self.mini_sample.name 
        return histo   
    def plotto(self, eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, boost_type = ""):
        epsilon = {}
        epsilon[boost_type] = [eff_b_w_fj*100, eff_b_wo_fj*100]
        epsilon["resolved"] = [eff_r_w_fj*100, eff_r_wo_fj*100]
        df = pd.DataFrame(data=epsilon , index=["fwd" , "not_fwd"])

        plt.rcParams["figure.figsize"]=[8, 5] 
        plt.rcParams["figure.autolayout"]=True 
        plt.title("Efficiencies (%)" + self.mini_sample.name) 
        
        colors = {
            "boost_tau32": "YlGnBu",
            "boost_tau32_btag": "BuPu",
            "boost_deep": "summer",
            "boostdeep_btag": "PiYG"
        }

        plot = sns.heatmap(df, cmap= 'YlGnBu', annot=True) #colors[boost_type]
        plt.savefig(self.mini_sample.name.replace(".root","") + "_" +boost_type +".png") 
        plt.close()
    def efficiency_plotter(self, significance = 1):
        skim_name = self.skim_name()
        hist_name = self.hist_name()
        the_maker = efficiency_maker(nome_file= skim_name,
                                     nome_hist= hist_name)
        n_boost_fwd    = 0
        n_boost_nfw    = 0 
        n_resolved_fwd = 0 
        n_resolved_nfw = 0
        NCount_db = 0
        NCount_d = 0
        NCount_t32 = 0
        NCount_t32b =0
        
        
        if significance:
            print("acquisito il dataset, inizio operazione\n[--------]")
            make_sig = significancer(self.mini_sample)
        
            eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, n_boost_fwd, n_boost_nfw, n_resolved_fwd, n_resolved_nfw, Ntot = the_maker.counter_32(sig=significance)
            self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_tau32")
            n_list = [n_boost_fwd, n_boost_nfw, n_resolved_fwd, n_resolved_nfw]
            NCount_t32 = []
            for i in n_list:
                normalized_count = make_sig.normalize_counting(i, Ntot)
                NCount_t32.append(normalized_count)
            print("[##------]")

            eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, n_boost_fwd, n_boost_nfw, n_resolved_fwd, n_resolved_nfw, Ntot  = the_maker.counter_32btag(sig=significance)
            self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_tau32_btag")
            n_list = [n_boost_fwd, n_boost_nfw, n_resolved_fwd, n_resolved_nfw]
            NCount_t32b = []
            for i in n_list:
                normalized_count = make_sig.normalize_counting(i, Ntot)
                NCount_t32b.append(normalized_count)
            print("[####----]")

            eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, n_boost_fwd, n_boost_nfw, n_resolved_fwd, n_resolved_nfw, Ntot  = the_maker.counter_deep(sig=significance)
            self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_deep")
            n_list = [n_boost_fwd, n_boost_nfw, n_resolved_fwd, n_resolved_nfw]
            NCount_d = []
            for i in n_list:
                normalized_count = make_sig.normalize_counting(i, Ntot)
                NCount_d.append(normalized_count)
            print("[######--]")

            eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, n_boost_fwd, n_boost_nfw, n_resolved_fwd, n_resolved_nfw, Ntot  = the_maker.counter_deepbtag(sig=significance)
            self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boostdeep_btag")
            n_list = [n_boost_fwd, n_boost_nfw, n_resolved_fwd, n_resolved_nfw]
            NCount_db = []
            for i in n_list:
                normalized_count = make_sig.normalize_counting(i, Ntot)
                NCount_db.append(normalized_count)
            print("[########]")

            return NCount_t32, NCount_t32b, NCount_d, NCount_db
        else:
            print("acquisito il dataset, inizio operazione\n[--------]")
            eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = the_maker.counter_32(sig=significance)
            self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_tau32")
            print("[##------]")

            eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = the_maker.counter_32btag(sig=significance)
            self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_tau32_btag")
            print("[####----]")

            eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = the_maker.counter_deep(sig=significance)
            self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_deep")
            print("[######--]")

            eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = the_maker.counter_deepbtag(sig=significance)
            self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boostdeep_btag")
            print("[########]")

            return NCount_t32, NCount_t32b, NCount_d, NCount_db