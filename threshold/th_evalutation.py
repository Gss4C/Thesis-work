from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.meta_funcs.nonroot import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.meta_funcs.histos import *

# ../../../../../../../src/PhysicsTools/NanoAODTools/crab/macros/files/

lista = read_and_list("../../../../../../../src/PhysicsTools/NanoAODTools/crab/macros/files/TT_hadr_2018.txt")
print(lista)