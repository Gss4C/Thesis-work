from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection , Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True 

#########################
#    TAGGING MODULES    #
#########################
class preskim_goodtag:
    '''
    Class for tagging good events and toptagged fatjets
    '''
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Jet_isGood",      "O", lenVar="nJet") 
        self.out.branch("FatJet_isGood",   "O", lenVar="nFatJet")
        self.out.branch("Electron_isGood", "O", lenVar="nElectron")
        self.out.branch("Muon_isGood",     "O", lenVar="nMuon")
        self.out.branch("FatJet_toptagged","O", lenVar="nFatJet")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def index_tagmaker(self, collect, indici, branch = "no_branch"):
        goodList = []
        for index in range(len(collect)):
            if index in indici:
                isGood = True
            else:
                isGood = False
            goodList.append(isGood)
        self.out.fillBranch(branch , goodList)   

    def analyze(self,event):
        jets     = Collection(event, "Jet")
        fatjets  = Collection(event, "FatJet")
        electron = Collection(event, "Electron")
        muons    = Collection(event, "Muon")

        ########################
        #    List filtering    #
        ########################
        goodJets_idx    = list(filter(lambda idx: 
                                      jets[idx].pt       > 30  and  
                                      abs(jets[idx].eta) < 4 and 
                                      jets[idx].jetId    >= 3 , 
                                      range(0, len(jets)))) 
        goodFjets_idx   = list(filter(lambda idx: fatjets[idx].pt > 200 and  
                                      abs(fatjets[idx].eta)       < 2.4 ,
                                      range(0, len(fatjets))))
        goodEle_idx     = list(filter(lambda idx: electron[idx].pt > 30  and  
                                      electron[idx].cutBased >= 2, 
                                      range(0, len(electron))))
        goodMu_idx      = list(filter(lambda idx: muons[idx].pt > 30  and  
                                      muons[idx].looseId , 
                                      range(0, len(muons))))
        toptaggedFjets_idx = list(filter(lambda idx: 
                                         fatjets[idx].pt        > 400 and  
                                         fatjets[idx].msoftdrop > 105 and 
                                         fatjets[idx].msoftdrop > 220, 
                                         range(0, len(fatjets))))
        self.index_tagmaker(jets,     goodJets_idx,  "Jet_isGood")
        self.index_tagmaker(fatjets,  goodFjets_idx, "FatJet_isGood")
        self.index_tagmaker(electron, goodEle_idx,   "Electron_isGood")
        self.index_tagmaker(muons,    goodMu_idx,    "Muon_isGood")
        self.index_tagmaker(fatjets, toptaggedFjets_idx, "FatJet_toptagged")
        return True


##########################
#    SKIMMING MODULES    #
##########################
class first_skimmer:
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def good_btagged_jet(self, jets_collection):
        is_good_jet = False
        for i in range(len(jets_collection)):
            if jets_collection[i].isGood and jets_collection[i].btagDeepB >= 0.4184:
                is_good_jet = True
        return is_good_jet

    def analyze(self,event):
        HLT      = Object(event, "HLT")
        MET      = Object(event, "MET")
        jets     = Collection(event, "Jet")
        fatjets  = Collection(event, "FatJet")

        isGoodHLT  = HLT.PFMETNoMu120_PFMHTNoMu120_IDTight or HLT.PFMET120_PFMHT120_IDTight
        isGoodMET  = MET.pt > 200
        isGoodJet = any(jet.isGood and jet.btagDeepB >= 0.4184 for jet in jets)
        #questo sopra fa quando scritto sotto con la funzione
        #isGoodJet  = self.good_btagged_jet(jets) 
        #isGoodJet  = len(list(filter(lambda idx: jets[idx].btagDeepB >= 0.4184 , goodJets_idx)))
        isGoodFjet = any(fjet.isGood for fjet in fatjets)
        #la funzione sopra è il modo python di scrivere quello sotto
        #isGoodFjet = False
        #for fjet in fatjets:
        #    if fjet.isGood:
        #        isGoodFjet = True
        #isGoodFjet = len(goodFjets_idx)
        goodEvent = isGoodHLT and isGoodMET and (isGoodJet or isGoodFjet)
        return goodEvent

class veto_skimmer:
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def collect_list_gfilter(self, collection):
        collect_list = []
        for i in range(len(collection)):
            if collection[i].isGood:
                collect_list.append(collection[i])
        return collect_list
    def deltaphis(self, collect, object):
        deltas = []
        for i in range(len(collect)):
            if collect[i].isGood:
                deltaphi = abs(collect[i].phi - object.phi)
                deltas.append(deltaphi)
        return (deltas if len(deltas) else [-1.0]) #to avoid 'empty sequence' error
    
    def global_veto(self, MET, deltaphis, electrons, muons):
        '''
        Condizioni globali di veto che definiscono l'ultima selezione di eventi. Questa funzione va studiato se convenga o meno integrarla in
        '''
        cond_MET = MET.pt         >200
        cond_phi = min(deltaphis) >0.6
        goodEle  = self.collect_list_gfilter(electrons)
        goodMu   = self.collect_list_gfilter(muons)
        if len(goodEle)==0 and len(goodMu)==0:
            cond_lep = True
        else:
            cond_lep = False
        cond_global = cond_lep and cond_phi and cond_MET
        return cond_global
    
    def analyze(self, event):
        MET         = Object(event, "MET")
        jets        = Collection(event, "Jet")
        electrons   = Collection(event, "Electron")
        muons       = Collection(event, "Muon")
        
        delta_list = self.deltaphis(jets, MET)
        passing_veto = self.global_veto(MET, delta_list, electrons, muons)
        return passing_veto