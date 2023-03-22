from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection , Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  

class full_selector(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Jet_isGood",      "O", lenVar="nJet") #O sta per booleano
        self.out.branch("FatJet_isGood",   "O", lenVar="nFatJet")
        self.out.branch("Electron_isGood", "O", lenVar="nElectron")
        self.out.branch("Muon_isGood",     "O", lenVar="nMuon")
        self.out.branch("FatJet_toptagged","O", lenVar="nFatJet")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def tagmaker(self, collect, indici, branch = "no_branch"):
        goodList = []
        for index in range(len(collect)):
            #if index == indici[index]:
            if index in indici:
                isGood = True
            else:
                isGood = False
            goodList.append(isGood)
        self.out.fillBranch(branch , goodList)
            
    def analyze(self,event):
        #creating collections for every event
        HLT      = Object(event, "HLT")
        MET      = Object(event, "MET")
        jets     = Collection(event, "Jet")
        fatjets  = Collection(event, "FatJet")
        electron = Collection(event, "Electron")
        muons    = Collection(event, "Muon")
        #**********************#
        #Collections
        #**********************#
        goodJets_idx    = list(filter(lambda idx: 
                                      jets[idx].pt                     > 30  and  
                                      abs(jets[idx].eta)               < 4 and 
                                      jets[idx].jetId                  >= 3 , 
                                      range(0, len(jets)))) 
        
        goodFjets_idx   = list(filter(lambda idx: fatjets[idx].pt      > 200 and  
                                      abs(fatjets[idx].eta)            < 2.4 ,
                                      range(0, len(fatjets))))
        
        goodEle_idx     = list(filter(lambda idx: electron[idx].pt     > 30  and  
                                      electron[idx].cutBased_Fall17_V1 >= 2  , 
                                      range(0, len(electron))))
        
        goodMu_idx      = list(filter(lambda idx: muons[idx].pt        > 30  and  
                                      muons[idx].looseId , 
                                      range(0, len(muons))))
        #creating branches
        self.tagmaker(jets, goodJets_idx, "Jet_isGood")
        self.tagmaker(fatjets, goodFjets_idx, "FatJet_isGood")
        self.tagmaker(electron, goodEle_idx, "Electron_isGood")
        self.tagmaker(muons, goodMu_idx, "Muon_isGood")
        
        #toptag
        toptaggedFjets_idx = list(filter(lambda idx: 
                                         fatjets[idx].pt >        400 and  
                                         fatjets[idx].msoftdrop > 105 and 
                                         fatjets[idx].msoftdrop > 220 and
                                         fatjets[idx].tau3/(fatjets[idx].tau2) < 0.65
                                         ,range(0, len(fatjets))))
        self.tagmaker(fatjets, toptaggedFjets_idx, "FatJet_toptagged")

        #**********************
        #objects & boolean
        #**********************
        isGoodHLT = HLT.PFMETNoMu120_PFMHTNoMu120_IDTight or HLT.PFMET120_PFMHT120_IDTight
        isGoodMET = MET.pt > 200
        isGoodJet = len(list(filter(lambda idx: jets[idx].btagDeepB >= 0.4184 , goodJets_idx)))
        isGoodFjet = len(goodFjets_idx)
        
        goodEvent = isGoodHLT and isGoodMET and (isGoodJet or isGoodFjet)
        return goodEvent