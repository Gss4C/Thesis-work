from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

cuts = []
cut1 = {}
cut1["key"]         = "Jet"
cut1["type"]        = 1
cut1["cutFunc"]     = lambda x: True
cut1["goodness"]    = lambda x: True
cuts.append(cut1)

class EvSkim(Module):
    def __init__(self, cuts):
        self.cuts = cuts
        
    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # self.out = wrappedOutputTree
        # self.out.branch("goodJets_pt", "F", lenVar="ngoodJets")
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        # goodEvent = False
        goodness = []
        """process event, return True (go to next module) or False (fail, go to next event)"""
        for cut in self.cuts:
            if cut["type"]:
                Elements = Collection(event, cut["key"])
            else:
                Elements = Object(event, cut["key"])
            
            GoodElements    = list(filter(cut["cutFunc"], Elements))
            isGoodElement   = len(GoodElements) >= 1
            # isGoodElement   = cut["goodness"](GoodElements)
            goodness.append(isGoodElement)
        goodEvent = all(goodness)
        return goodEvent
        
        # Met         = Object(event, "MET")
        # Jets        = Collection(event, "Jet")
        # FatJets     = Collection(event, "FatJet")
        # Muons       = Collection(event, "Muon")
        # Electrons   = Collection(event, "Electron")
        
        # GoodMet         = list(filter(self.MetSel,  Met)) 
        # GoodJets        = list(filter(self.JetSel,  Jets))        
        # GoodFatJets     = list(filter(self.FJetSel, FatJets)) 
        # GoodMuons       = list(filter(self.ElSel,   Muons)) 
        # GoodElectrons   = list(filter(self.MuSel,   Electrons))
        
        
        
        
         
        # self.out.fillBranch("goodJets_pt", [goodJet.pt for goodJet in goodJets])
        # return goodEvent