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
        ## servono solo 4 variabili
        self.resolved_fwd = 0 
        self.resolved_nfw = 0 
        self.boost_fwd    = 0 
        self.boost_nfw    = 0

        self.percorso  = "/afs/cern.ch/user/j/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab"
    def counter_32(self):
        histo_file   = ROOT.TFile(self.percorso + self.nome_hist,"Open")
        skimmed_file = ROOT.TFile(self.percorso + self.nome_file,"Open")
        histos = histo_file.plots.Get("h_genweight")
        weight = histos.GetBinContent(1)
        small_tree = skimmed_file.Events

        '''self.boost_fwd    = 0
        self.boost_nfw    = 0
        self.resolved_fwd = 0
        self.resolved_nfw = 0
        non dovrebbe servire'''
        for event in range(small_tree.GetEntries()):
            small_tree.GetEntry(event)
            jets   = Collection(small_tree, "Jet")
            BST    = False
            RSL    = False
            is_fwd = False

            if(small_tree.Boosted_tau32):
                BST = True
            if(small_tree.Resolved and not small_tree.Boosted_tau32):
                RSL = True

            for jet in jets:
                if jet.isForward and jet.isGood:
                    is_fwd = True

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
        return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj
    def counter_32btag(self):
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

            if(small_tree.Boosted_tau32btag):
                BST = True
            if(small_tree.Resolved and not small_tree.Boosted_tau32btag):
                RSL = True

            for jet in jets:
                if jet.isForward and jet.isGood:
                    is_fwd = True

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
        return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj
    def counter_deep(self):
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

            if(small_tree.Boosted_deeptag):
                BST = True
            if(small_tree.Resolved and not small_tree.Boosted_deeptag):
                RSL = True

            for jet in jets:
                if jet.isForward and jet.isGood:
                    is_fwd = True

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
        return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj
    def counter_deepbtag(self):
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

            if(small_tree.Boosted_deeptagbtag):
                BST = True
            if(small_tree.Resolved and not small_tree.Boosted_deeptagbtag):
                RSL = True

            for jet in jets:
                if jet.isForward and jet.isGood:
                    is_fwd = True

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
        return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj

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

        plot = sns.heatmap(df, cmap=colors[boost_type], annot=True)
        plt.savefig(self.mini_sample.name.replace(".root","") + "_" +boost_type +".png") 
        plt.close()

    def efficiency_plotter(self):
        skim_name = self.skim_name()
        hist_name = self.hist_name()
        the_maker = efficiency_maker(nome_file= skim_name,
                                     nome_hist= hist_name)
        print("acquisito il dataset, inizio operazione\n[--------]")
        eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = the_maker.counter_32()
        self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_tau32")
        print("[##------]")
        eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = the_maker.counter_32btag()
        self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_tau32_btag")
        print("[####----]")
        eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = the_maker.counter_deep()
        self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boost_deep")
        print("[######--]")
        eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = the_maker.counter_deepbtag()
        self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj, "boostdeep_btag")
        print("[########]")
        