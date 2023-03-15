from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection , Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True 

class boosted_resolved(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Boosted",  "I")
        self.out.branch("Resolved", "I")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    #***************************************************#
    # My functions
    #***************************************************#

    def deltaphis(self, collect, object): #MET è un oggetto enon una collection
        deltas = []
        for i in range(len(collect)):
            deltaphi = collect[i].phi - object.phi
            deltas.append(deltaphi)
        return deltas

    def global_veto(self, MET, deltaphis, electrons, muons):
        # cond veto globali che valgono per entrambe le analis, senza lui non vado avanti e scarto l'evento
        cond_MET = MET.pt > 200
        cond_phi = min(deltaphis)>0.6
        if len(electrons)==0 and len(muons)==0:
            cond_lep = True
        else:
            cond_lep = False
        cond_global = cond_lep and cond_phi and cond_MET
        return cond_global
    
    def HT(self, jets):
        #calcola HT e controlla che abbia almeno 3 jets nell'evento
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
        fatjets     = Collection(event, "FatJet")
        electrons    = Collection(event, "Electron")
        muons       = Collection(event, "Muon")
        
        delta_list = self.deltaphis(jets, MET)
        event_global_condition = self.global_veto(MET, delta_list, electrons, muons)
        
        if event_global_condition:
            eventsavior = True
            boost  = False
            resolv = False
            #***********************#
            #   Resolved test   #
            #***********************#
            ht, three= self.HT(jets)
            if ht>200 and three:
                #solo se ho le condiz precedenti inizio a calcolare le combinaz a 3 jet a volta di tlorentzvector
                event_combo_pt = []
                tlv1 = ROOT.TLorentzVector()
                tlv2 = ROOT.TLorentzVector()
                tlv3 = ROOT.TLorentzVector()
                for jet in jets: 
                    for jit in jets:
                        for jot in jets:
                            if not (jet == jit) and not (jot == jet):
                                if(jet.isGood and jot.isGood and jit.isGood):
                                    tlv1.SetPtEtaPhiM(jet.pt , jet.eta , jet.phi , jet.mass)
                                    tlv2.SetPtEtaPhiM(jit.pt , jit.eta , jit.phi , jit.mass)
                                    tlv3.SetPtEtaPhiM(jot.pt , jot.eta , jot.phi , jot.mass)
                                    tlv = tlv1+tlv2+tlv3
                                    if tlv.Pt() > 250: #devo aggiungere btag
                                        event_combo_pt.append(tlv.Pt())
                if len(event_combo_pt):
                    resolv = True
            #***********************#
            #   Boosted test   #
            #***********************#
            if len(jets) and len(fatjets):
                fj_sdm = []
                for jet in fatjets:
                    fj_sdm.append(jet.msoftdrop)
                if max(fj_sdm) >= 40:
                    boost = True
            #ora devo riempire i branches
            self.out.fillBranch("Boosted", boost)
            self.out.fillBranch("Resolved", resolv)
        else:
            eventsavior = False
        return eventsavior #ciao