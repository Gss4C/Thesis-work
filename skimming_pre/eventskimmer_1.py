from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
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

class jets_selector(Module):
    def __init__(self, cuts_dictionary_array):
        self.cuts = cuts_dictionary_array
        pass

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
        goodness = []
        for cut in self.cuts:
            if cut["type"]:
                event_data = Collection(event , cut["key"])
            else:
                event_data = Object(event , cut["key"])
            good_event = list(filter(cut["function"],event_data))
            isGood = len(good_event) >= 1
            #isGood = cut["isGood"](good_event)
            goodness.append(isGood)
        isgoodevent = all(goodness)
        return isgoodevent

