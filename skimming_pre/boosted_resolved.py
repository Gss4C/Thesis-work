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
        self.out.branch("Boosted",  "0")
        self.out.branch("Resolved", "0")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    #***************************************************#
    # My functions
    #***************************************************#

    def deltaphis(self, collect1, collect2):
        deltas = []
        for i in range(len(collect1)):
            for j in range(len(collect2)):
                deltaphi = collect1[i].phi - collect2[j].phi
                deltas.append(deltaphi)
        return deltas

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
    
    def HT(jets):
        somma = 0
        count = 0
        leastthree = False
        for jet in jets:
            if jet.isGood: 
                somma += jet.pt 
                count += 1
        if count >= 3: leastthree = True
        return somma, leastthree

    def analyze(self,event): #qui raccolgo solo robaccia good
        HLT         = Object(event, "HLT")
        MET         = Object(event, "MET")
        jets        = Collection(event, "Jet")
        #fatjets     = Collection(event, "FatJet")
        electrons    = Collection(event, "Electron")
        muons       = Collection(event, "Muon")
        
        delta_list = self.deltaphis(jets, MET)
        event_global_condition = self.global_veto(MET, delta_list, electrons, muons)
        
        if event_global_condition:
            eventsavior = True
            boost  = False
            resolv = False
            ht, three= self.HT(jets)
            if ht>200 and three:
                #solo se ho le condiz precedenti inizio a calcolare le combinaz a 3 jet a volta di tlorentzvector
                for jet in jets: 
                    
                resolv = True

        else:
            eventsavior = False
        return eventsavior