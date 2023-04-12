from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection , Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True 

class boosted_resolved(Module):
    def __init__(self):
        #self.lepton_ok = 0
        #self.phis_ok = 0
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Boosted_tau32" ,  "I")
        self.out.branch("Boosted_tau32btag" ,  "I")
        self.out.branch("Boosted_deeptag" ,  "I")
        self.out.branch("Boosted_deeptagbtag" ,  "I")
        self.out.branch("Resolved", "I")

        self.out.branch("nTopRes",        "I")
        self.out.branch("TopRes_terIdx1", "I", lenVar="nTopRes")
        self.out.branch("TopRes_terIdx2", "I", lenVar="nTopRes")
        self.out.branch("TopRes_terIdx3", "I", lenVar="nTopRes")
        self.out.branch("TopRes_pt",      "D", lenVar="nTopRes")

        self.out.branch("Jet_isForward", "O", lenVar="nJet")        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    #***************************************************#
    # My functions
    #***************************************************#
    def deltaphis(self, collect, object):
        deltas = []
        for i in range(len(collect)):
            if collect[i].isGood:
                deltaphi = abs(collect[i].phi - object.phi)
                deltas.append(deltaphi)
        return (deltas if len(deltas) else [-1.0]) #sta roba serve per evitare l'empy sequence
    def deltaR(self, object1, object2): #distanza piano eta-phi
        Deta = object1.eta - object2.eta
        Dphi = object1.phi - object2.phi
        distance = math.sqrt(Deta*Deta + Dphi*Dphi)
        return distance
    def collect_list_gfilter(self, collection):
        collect_list = []
        for i in range(len(collection)):
            if collection[i].isGood:
                collect_list.append(collection[i])
        return collect_list
    def global_veto(self, MET, deltaphis, electrons, muons):
        # cond veto globali che valgono per entrambe le analis, senza lui non vado avanti e scarto l'evento
        cond_MET = MET.pt        >200
        cond_phi = min(deltaphis)>0.6
        goodEle  = self.collect_list_gfilter(electrons)
        goodMu   = self.collect_list_gfilter(muons)
        if len(goodEle)==0 and len(goodMu)==0:
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
    
    #***************************************************#
    # taggers
    #***************************************************#
    def forward_jet_tagger(self, jet_collection, branch = "Jet_isForward"):
        # mi tagga i jet definibili forward
        forward_list = []
        for jet in jet_collection:
            single_jet_forward = False
            if abs(jet.eta)>2.4 and jet.pt > 30:
                single_jet_forward = True
            forward_list.append(single_jet_forward)
        self.out.fillBranch(branch, forward_list)

    def indexer(self, branch1 , branch2 , branch3 , lista):
        #funzione che riempie i branch (originariamente i jet ak4 toptag) con gli indici della terna originale
        ones   = []
        twos   = []
        threes = []
        for dict in lista:
            ones.append(  dict["1"])
            twos.append(  dict["2"])
            threes.append(dict["3"])
        self.out.fillBranch(branch1, ones)
        self.out.fillBranch(branch2, twos)
        self.out.fillBranch(branch3, threes)


    def analyze(self,event): 
        HLT         = Object(event, "HLT")
        MET         = Object(event, "MET")
        jets        = Collection(event, "Jet")
        fatjets     = Collection(event, "FatJet")
        electrons   = Collection(event, "Electron")
        muons       = Collection(event, "Muon")
        
        delta_list = self.deltaphis(jets, MET)
        event_global_condition = self.global_veto(MET, delta_list, electrons, muons)
        
        if event_global_condition:
            eventsavior = True

            boost  = False
            resolv = False
            self.forward_jet_tagger(jets, "Jet_isForward")
            #########################
            #     Resolved test     #
            #########################
            ht, three= self.HT(jets)
            if ht>200 and three:
                event_combo_pt = []
                index_lists    = []
                n_topres       = 0

                for i in range(len(jets)):
                    for j in range(i):
                        for k in range(j):
                            if(jets[i].isGood and jets[j].isGood and jets[i].isGood):
                                
                                tlv1 = jets[i].p4()
                                tlv2 = jets[j].p4()
                                tlv3 = jets[k].p4()

                                tlv = tlv1+tlv2+tlv3

                                if tlv.Pt() > 250:
                                    event_combo_pt.append(tlv.Pt())

                                    terna = {"1":1, "2":1, "3":1}
                                    terna["1"] = i
                                    terna["2"] = j
                                    terna["3"] = k
                                    index_lists.append(terna)

                                    n_topres += 1
                self.out.fillBranch("nTopRes"  , n_topres)
                self.out.fillBranch("TopRes_pt", event_combo_pt)
                self.indexer("TopRes_terIdx1","TopRes_terIdx2","TopRes_terIdx3",index_lists)
                if len(event_combo_pt):
                    resolv = True
            #########################
            #     Boosted test      #
            #########################
            if len(jets) and len(fatjets):
                for fjet in fatjets:
                    if fjet.msoftdrop>105 and fjet.msoftdrop<220:

                    '''
                    tau32 = fjet.tau3/fjet.tau2 if fjet.tau2 != 0 else 50
                    if fjet.msoftdrop>105 and fjet.msoftdrop<220 and tau32 < 0.65:
                        good_jets_list = self.collect_list_gfilter(jets)
                        for jet in good_jets_list:
                            if jet.btagDeepB > 0.1241:
                                distance = self.deltaR(jet,fjet)
                                if distance<0.8:
                                    boost = True
                    '''
            #ora devo riempire i branches
            self.out.fillBranch("Boosted" , int(boost))
            self.out.fillBranch("Resolved", int(resolv))
        else:
            eventsavior = False
        return eventsavior 