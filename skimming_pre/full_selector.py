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
        self.out.branch("Jet_gidx",      "O", lenVar="nJet") #O sta per booleano
        self.out.branch("FatJet_gidx",   "O", lenVar="nFatJet")
        self.out.branch("Electron_gidx", "O", lenVar="nElectron")
        self.out.branch("Muon_gidx",     "O", lenVar="nMuon")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def goodmaker(self, collect, indici, branch = "no_branch"):
        goodList = []
        for index in range(0, len(collect)):
            if index == indici[index]:
                isGood = True
            else:
                isGood = False
            goodList.append(isGood)
        self.out.fillBranch(branch , goodList)
            
    def analyze(self,event):
        #creating collections for every event
        HLT         = Object(event, "HLT")
        MET         = Object(event, "MET")
        jets        = Collection(event, "Jet")
        fatjets     = Collection(event, "FatJet")
        electron    = Collection(event, "Electron")
        muons       = Collection(event, "Muon")

        #**********************#
        #Collections
        #**********************#
        goodJets_idx    = list(filter(lambda idx: jets[idx].pt     > 30  and  abs(jets[idx].eta)               < 2.4 and jets[idx].jetId >= 3 , range(0, len(jets)))) #l'ho scelto a caso 0.5 del btag
        goodFjets_idx   = list(filter(lambda idx: fatjets[idx].pt  > 200 and  abs(fatjets[idx].eta)            < 2.4 , range(0, len(fatjets))))
        goodEle_idx     = list(filter(lambda idx: electron[idx].pt > 30  and  electron[idx].cutBased_Fall17_V1 >= 2  , range(0, len(electron))))
        goodMu_idx      = list(filter(lambda idx: muons[idx].pt    > 30  and  muons[idx].looseId                     , range(0, len(muons))))
        #creating branches
        self.goodmaker(jets, goodJets_idx, "Jet_gidx")
        self.goodmaker(fatjets, goodFjets_idx, "FatJet_gidx")
        self.goodmaker(electron, goodEle_idx, "Electron_gidx")
        self.goodmaker(muons, goodMu_idx, "Muon_gidx")
        
       ''' for index in range(0,len(jets)):
            if index == goodJets_idx[index]:
                validator = True
            else:
                validator = False
            self.out.fillBranch("Jet_gidx",  validator)


        self.out.fillBranch("FatJets_gidx", goodFjets_idx)
        self.out.fillBranch("goodEle_gidx",  goodEle_idx)
        self.out.fillBranch("Muon_gidx",   goodMu_idx)'''

        #**********************
        #objects & boolean
        #**********************
        isGoodHLT = HLT.PFMETNoMu120_PFMHTNoMu120_IDTight or HLT.PFMET120_PFMHT120_IDTight
        isGoodMET = MET.pt > 200
        isGoodJet = len(list(filter(lambda idx: jets[idx].btagDeepB >= 0.4184 , goodJets_idx)))
        isGoodFjet = len(goodFjets_idx)
        
        goodEvent = isGoodHLT and isGoodMET and (isGoodJet or isGoodFjet)
        return goodEvent
