import ROOT
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import awkward as ak

#    Coffea histo maker for single file    #
def histo_writer():
single_tree = NanoEventsFactory.from_root(files_list[1], schemaclass=NanoAODSchema.v6).events()
scores = ak.flatten(tree.TopLowPt[(tree.TopLowPt.truth==0)].scoreDNN)

histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
for score in scores:
    histo.Fill(score)
gisto.Write()