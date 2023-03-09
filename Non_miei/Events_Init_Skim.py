from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

class Events_Init_Skim(Module):
    '''
    You can use this module in PostProcessor() to select events passing some cuts. 
    Usage: p = PostProcessor('.', ['/path/to/file.root'], '', modules=[Events_Init_Skim()], outputbranchsel=os.path.abspath('../scripts/keep_and_drop.txt'), histFileName="histOut.root", histDirName="plots", provenance=True, maxEntries=100, fwkJobReport=True)
    '''
    def __init__(self):
        pass
        
        
    def beginJob(self):
        pass


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("GoodElectrons_Idx", "I", lenVar="nGoodElectrons")
        self.out.branch("GoodMuons_Idx",     "I", lenVar="nGoodMuons")
        self.out.branch("GoodJets_Idx",      "I", lenVar="nGoodJets")
        self.out.branch("GoodFatJets_Idx",   "I", lenVar="nGoodFatJets")
        pass


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def DeepCSV_discr(self, year):
        if year == 2016:
            return 0.6321
        if year == 2017:
            return 0.4941
        if year == 2018:
            return 0.4184
                
    
    def analyze(self, event):
        HLT         = Object(event, "HLT")
        MET         = Object(event, "MET")
        Electrons   = Collection(event, "Electron")    
        Muons       = Collection(event, "Muon")
        Jets        = Collection(event, "Jet")
        FatJets     = Collection(event, "FatJet")
        
        
        GoodElectronsIdx     = list(filter(lambda idx: Electrons[idx].pt > 30     and Electrons[idx].cutBased >= 2     and abs(Electrons[idx].eta) < 2.5,      range(0, len(Electrons))))                               
        GoodMuonsIdx         = list(filter(lambda idx: Muons[idx].pt > 30         and Muons[idx].looseId               and abs(Muons[idx].eta) < 2.5,          range(0, len(Muons))))                       
        GoodJetsIdx          = list(filter(lambda idx: Jets[idx].pt > 30          and Jets[idx].jetId >= 3             and abs(Jets[idx].eta) < 2.4,           range(0, len(Jets))))                       
        GoodFatJetsIdx       = list(filter(lambda idx: FatJets[idx].pt > 200                                           and abs(FatJets[idx].eta) < 2.4,        range(0, len(FatJets))))
        
                                  
        self.out.fillBranch("GoodElectrons_Idx",    GoodElectronsIdx)
        self.out.fillBranch("GoodMuons_Idx",        GoodMuonsIdx)
        self.out.fillBranch("GoodJets_Idx",         GoodJetsIdx)
        self.out.fillBranch("GoodFatJets_Idx",      GoodFatJetsIdx)
        
        
        PassTrigger     = HLT.PFMETNoMu120_PFMHTNoMu120_IDTight or HLT.PFMET120_PFMHT120_IDTight
        PassMET         = MET.pt                                                                                                 >=  200
        PassJets        = len(list(filter(lambda idx: Jets[idx].btagDeepFlavB >= self.DeepCSV_discr(2018), GoodJetsIdx)))        >=  1      
        PassFatJets     = len(GoodFatJetsIdx)                                                                                    >=  1         
        
         
        PassEvent       = PassTrigger and PassMET and (PassJets or PassFatJets)
        return PassEvent