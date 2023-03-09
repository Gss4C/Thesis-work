from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  

class full_selector(Module):
    def __init__(self):

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("goodJets_idx", "F" , lenVar="ngoodJets")
        self.out.branch("goodFjets_idx", "F", lenVar="ngoodFjets")
        self.out.branch("goodEle_idx", "F"  , lenVar="ngoodEle")
        self.out.branch("goodMu_idx", "F"   , lenVar="ngoodMu")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self,event):
        #creating collections for every event
        HLT         = Object(event, "HLT")
        MET         = Object(event, "MET")
        jets        = Collection(event, "Jet")
        fatjets     = Collection(event, "FatJet")
        electron   = Collection(event, "Electron")
        muons       = Collection(event, "Muon")

        #**********************#
        #Collections
        #**********************#
        goodJets_idx    = list(filter(lambda idx: jets[idx].pt     > 30  and  abs(jets[idx].eta)               < 2.4 and jets[idx].jetID >= 3, range(0, len(jets))))
        goodFjets_idx   = list(filter(lambda idx: fatjets[idx].pt  > 200 and  abs(fatjets[idx].eta)            < 2.4                         , range(0, len(fatjets))))
        goodEle_idx     = list(filter(lambda idx: electron[idx].pt > 30  and  electron[idx].cutBased_Fall17_V1 >= 2                          , range(0, len(electron))))
        goodMu_idx      = list(filter(lambda idx: muons[idx].pt    > 30  and  muons[idx].looseId                                             , range(0, len(muons))))
        #creating branches
        self.out.fillBranch("goodJet_idx",  goodJets_idx)
        self.out.fillBranch("goodFjet_idx", goodFjets_idx)
        self.out.fillBranch("goodEle_idx",  goodEle_idx)
        self.out.fillBranch("goodMu_idx",   goodMu_idx)

        #**********************
        #objects
        #**********************
        isGoodHLT = HLT.PFMETNoMu120_PFMHTNoMu120_IDTight and HLT.PFMET120_PFMHT120_IDTight
        isGoodMET = MET.pt > 200
        