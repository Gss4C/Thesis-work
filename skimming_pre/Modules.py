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
                                      jets[idx].jetId    >= 3, 
                                      range(0, len(jets)))) 
        goodFjets_idx   = list(filter(lambda idx: fatjets[idx].pt > 200 and  
                                      abs(fatjets[idx].eta)       < 2.4,
                                      range(0, len(fatjets))))
        goodEle_idx     = list(filter(lambda idx: electron[idx].pt > 30  and  
                                      electron[idx].cutBased >= 2, 
                                      range(0, len(electron))))
        goodMu_idx      = list(filter(lambda idx: muons[idx].pt > 30  and  
                                      muons[idx].looseId, 
                                      range(0, len(muons))))
        
        self.index_tagmaker(jets,     goodJets_idx,  "Jet_isGood")
        self.index_tagmaker(fatjets,  goodFjets_idx, "FatJet_isGood")
        self.index_tagmaker(electron, goodEle_idx,   "Electron_isGood")
        self.index_tagmaker(muons,    goodMu_idx,    "Muon_isGood")
        return True

class jets_NBR_tag:
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("FatJet_toptagged","O", lenVar="nFatJet")
        self.out.branch("Jet_isForward", "O", lenVar="nJet")
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
        jets        = Collection(event, "Jet")
        fatjets     = Collection(event, "FatJet")

        forward_list = [abs(jet.eta) > 2.4 and jet.pt > 30 for jet in jets]
        self.out.fillBranch("Jet_isForward", forward_list)

        #questa funzione pure si deve riscrivere piu pythonic
        toptaggedFjets_idx = list(filter(lambda idx: 
                                         fatjets[idx].pt        > 400 and  
                                         fatjets[idx].msoftdrop > 105 and 
                                         fatjets[idx].msoftdrop > 220, 
                                         range(0, len(fatjets))))
        self.index_tagmaker(fatjets, toptaggedFjets_idx, "FatJet_toptagged")
        return True

class Resolved_tagger:
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Resolved", "I")
        self.out.branch("nTopRes",        "I")
        self.out.branch("TopRes_terIdx1", "I", lenVar="nTopRes")
        self.out.branch("TopRes_terIdx2", "I", lenVar="nTopRes")
        self.out.branch("TopRes_terIdx3", "I", lenVar="nTopRes")
        self.out.branch("TopRes_pt",      "D", lenVar="nTopRes")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def HT(self, jets):
        #calcola HT e controlla che abbia almeno 3 jets nell evento
        somma = 0
        count = 0
        leastthree = False
        for jet in jets:
            if jet.isGood: 
                somma += jet.pt 
                count += 1
        if count >= 3: leastthree = True
        return somma, leastthree
    
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
        jets   = Collection(event, "Jet")
        resolv = False
        ht, three= self.HT(jets)
        if ht>200 and three: #voglio pt totale dei jets sopra una certa soglia
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
        self.out.fillBranch("Resolved", int(resolv))
        return True
    
class Boost_tagger:
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Boosted_tau32" ,      "I")
        self.out.branch("Boosted_tau32btag",   "I")
        self.out.branch("Boosted_deeptag",     "I")
        self.out.branch("Boosted_deeptagbtag", "I")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def collect_list_gfilter(self, collection):
        collect_list = []
        for i in range(len(collection)):
            if collection[i].isGood:
                collect_list.append(collection[i])
        return collect_list
    def deltaR(self, object1, object2): #distanza piano eta-phi
        Deta = object1.eta - object2.eta
        Dphi = object1.phi - object2.phi
        distance = math.sqrt(Deta*Deta + Dphi*Dphi)
        return distance
    def analyze(self,event):
        jets        = Collection(event, "Jet")
        fatjets     = Collection(event, "FatJet")
        boost_tau32        = False
        boost_tau32btag    = False
        boost_deeptag      = False
        boost_deeptagbtag  = False
        if len(jets) and len(fatjets):
            for fjet in fatjets:
                if fjet.msoftdrop>105 and fjet.msoftdrop<220:
                    #########################
                    #   caso non deeptag    #
                    #########################
                    tau32 = fjet.tau3/fjet.tau2 if fjet.tau2 != 0 else 50
                    if tau32 < 0.65:
                        boost_tau32 = True
                        good_jets_list = self.collect_list_gfilter(jets)
                        for jet in good_jets_list:
                            if jet.btagDeepB > 0.1241:
                                distance = self.deltaR(jet,fjet)
                                if distance<0.8:
                                    boost_tau32btag = True
                    #########################
                    #     caso deeptag      #
                    #########################
                    if fjet.deepTag_TvsQCD > 0.802: #WP for 1% mistagging rate
                        boost_deeptag = True
                        good_jets_list = self.collect_list_gfilter(jets)
                        for jet in good_jets_list:
                            if jet.btagDeepB > 0.1241:
                                distance = self.deltaR(jet,fjet)
                                if distance<0.8:
                                    boost_deeptagbtag = True
        self.out.fillBranch("Boosted_tau32"       , int(boost_tau32))
        self.out.fillBranch("Boosted_tau32btag"   , int(boost_tau32btag))
        self.out.fillBranch("Boosted_deeptag"     , int(boost_deeptag))
        self.out.fillBranch("Boosted_deeptagbtag" , int(boost_deeptagbtag))
        return True

class TopDNN_threshold_tagger:
    '''
    tagger che nasce dopo una valutazione con una dnn ed i suoi scoring
    le threshold sono state scelte tramite i programmi th_extract.py, qui si crea una flag che mi dice se la threshold è rispettata
    in particolare la threshold è stata scelta basandosi sul dataset tprimetotz 1000
    '''
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("TopHighPt_thgood", "I", lenVar="nTopHighPt")
        self.out.branch("TopLowPt_thgood",  "I", lenVar="nTopLowPt")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        tophigh_dnn = Collection(event, "TopHighPt")
        toplow_dnn  = Collection(event,  "TopLowPt")

        th_high = 0.164000004529953
        th_low  = 0.23199999332427979

        #hightag
        Hthgood_list = []
        for hjet in tophigh_dnn:
            if hjet.score2 > th_high:
                goodness = True
            else:
                goodness = False
            Hthgood_list.append(int(goodness))
        self.out.fillBranch("TopHighPt_thgood", Hthgood_list)
            
        #lowtag
        Lthgood_list = []
        for ljet in toplow_dnn:
            if ljet.scoreDNN > th_low:
                goodness = True
            else:
                goodness = False
            Lthgood_list.append(int(goodness))
        self.out.fillBranch("TopLowPt_thgood", Lthgood_list)
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
        #la funzione sopra e il modo python di scrivere quello sotto
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