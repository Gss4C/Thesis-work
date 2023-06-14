import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.threshold.thresholding_class import *

file = ROOT.TFile("/eos/user/j/jbonetti/Th_outputs/out_test_01.root", "RECREATE")
histomaker = thrashold_histomaker()
h_lowF, h_lowT, h_highF, h_highT = histomaker.crea_4histo()
file.Close()