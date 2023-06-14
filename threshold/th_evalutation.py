import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.Thesis.meta_funcs.nonroot import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.meta_funcs.histos import *
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

txt_crab_files_path = "../../../../../../../src/PhysicsTools/NanoAODTools/crab/macros/files/"
all_files_dict = {}

files_list = read_and_list("../../../../../../../src/PhysicsTools/NanoAODTools/crab/macros/files/TT_hadr_2018.txt")
#le liste di file devo organizzarle in un dict di liste così ho tutto a portata di mano

#apro il file, ne prendo uno a caso
single_tree = NanoEventsFactory.from_root(files_list[1], schemaclass=NanoAODSchema.v6).events()
scores = ak.flatten(tree.TopLowPt[(tree.TopLowPt.truth==0)].scoreDNN)

histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
for score in scores:
    histo.Fill(score)
histo.Write()
