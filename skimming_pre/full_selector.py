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
        self.out.branch("Jet_gidx", "F" , lenVar="ngoodJets")
        self.out.branch("FatJet_gidx", "F", lenVar="ngoodFjets")
        self.out.branch("Electron_gidx", "F"  , lenVar="ngoodEle")
        self.out.branch("Muon_gidx", "F"   , lenVar="ngoodMu")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
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
        self.out.fillBranch("Jet_gidx",  goodJets_idx)
        self.out.fillBranch("FatJets_gidx", goodFjets_idx)
        self.out.fillBranch("goodEle_gidx",  goodEle_idx)
        self.out.fillBranch("Muon_gidx",   goodMu_idx)

        #**********************
        #objects & boolean
        #**********************
        isGoodHLT = HLT.PFMETNoMu120_PFMHTNoMu120_IDTight or HLT.PFMET120_PFMHT120_IDTight
        isGoodMET = MET.pt > 200
        isGoodJet = len(list(filter(lambda idx: jets[idx].btagDeepB >= 0.4184 , goodJets_idx)))
        isGoodFjet = len(goodFjets_idx)
        
        goodEvent = isGoodHLT and isGoodMET and (isGoodJet or isGoodFjet)
        return goodEvent
