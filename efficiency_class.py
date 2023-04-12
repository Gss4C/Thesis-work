from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 

class classic_efficiency_make:
    def __init__(self, mini_sample): #devo ricordare di cambiare i nomi dai datasets
        self.mini_sample = mini_sample
    def skim_name(self):
        name_string = mini_sample.name
        skim = name_string.replace(".root","_Skim.root")
        return skim
    
    def hist_name(self):
        histo = "hist_out_" + mini_sample.name 
        return histo
    
    def e_counting(self):
        percorso  = "/home/jbonetti/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/"
        nome_file = self.skim_name()
        nome_hist = self.hist_name()

        histo_file = ROOT.TFile(percorso + nome_hist,"Open")
        skimmed_file = ROOT.TFile(percorso + nome_file,"Open")
        tree = skimmed_file.Events
        histos = histo_file.plots.Get("h_genweight")
        weight = histos.GetBinContent(1)

        boost_w_fj  = 0
        boost_wo_fj = 0
        res_w_fj    = 0
        res_wo_fj   = 0
        for event in range(tree.GetEntries()):
            tree.GetEntry(event)
            jets   = Collection(tree, "Jet")
            BST    = False
            RSL    = False
            is_fwd = False

            if(tree.Boosted):
                BST = True
            if(tree.Resolved and not tree.Boosted):
                RSL = True

            for jet in jets:
                if jet.isForward and jet.isGood:
                    is_fwd = True
            ## Counting ##
            if BST:
                if is_fwd:
                    boost_w_fj  += 1
                else:
                    boost_wo_fj += 1
            if RSL:
                if is_fwd:
                    res_w_fj  += 1
                else:
                    res_wo_fj += 1

        eff_b_w_fj = float(boost_w_fj)/weight
        eff_b_wo_fj = float(boost_wo_fj)/weight
        eff_r_w_fj = float(res_w_fj)/weight
        eff_r_wo_fj = float(res_wo_fj)/weight
        return eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj
    
    def plotto(self, eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj):
        epsilon = {}
        epsilon["boosted"]=[eff_b_w_fj*100, eff_b_wo_fj*100]
        epsilon["resolved"]=[eff_r_w_fj*100, eff_r_wo_fj*100]
        df = pd.DataFrame(data=epsilon , index=["fwd" , "not_fwd"])
        plt.rcParams["figure.figsize"]=[8, 5] 
        plt.rcParams["figure.autolayout"]=True 
        plt.title("Efficiencies (%)") 
        plot = sns.heatmap(df, cmap="summer", annot=True)
        plt.savefig(self.skim_name() +"png") #correggere qua

    def efficiency_plotter(self):
        eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj = self.e_counting()
        self.plotto(eff_b_w_fj, eff_b_wo_fj, eff_r_w_fj, eff_r_wo_fj)
