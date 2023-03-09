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
        self.out.branch("Boosted",  "0", lenVar="ngoodJets")
        self.out.branch("Resolved", "0", lenVar="ngoodJets")

    def deltaphis(self, collect1, collect2):
        for i in range(len(collect1)):
        

    def global_veto(self, MET, deltaphis, electrons, muons):
        # non voglio ci siano leptoni
        cond_MET = MET.pt > 200
        cond_phi = min(deltaphis)>0.6
        if len(electrons)==0 and len(muons)==0:
            cond_lep = True
        else:
            cond_lep = False
        cond_global = cond_lep and cond_phi and cond_MET
        return cond_global

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self,event): #qui raccolgo solo robaccia good
        HLT         = Object(event, "HLT")
        MET         = Object(event, "MET")
        jets        = Collection(event, "Jet")
        #fatjets     = Collection(event, "FatJet")
        electron    = Collection(event, "Electron")
        muons       = Collection(event, "Muon")
        
        delta_list = deltaphis(jets, MET)