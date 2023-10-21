import ROOT
import argparse

from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.ef_sig_class import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import awkward as ak
import copy
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description = "Threshold computation")
parser.add_argument("-s", "--signal",
                    type     = int,
                    help     = "signal name between: 700, 1000, 1800",
                    required = True)
opt = parser.parse_args()

def scaling_factor(sample_dict, name_string, luminosity, weight):
    sigma = sample_dict[name_string].sigma
    sl = sigma*luminosity
    if weight != 0:
        k = sl/weight
    else:
        k = 1
    return k

#setting variabili
mass = opt.signal
if opt.signal == 700:
    signal_name = "TprimeToTZ_700_2018"
elif opt.signal == 1000:
    signal_name = "TprimeToTZ_1000_2018" 
elif opt.signal == 1800:
    signal_name = "TprimeToTZ_1800_2018"
else:
    print("ERROR: Invalid signal input")

crabout = json_reader("crabout_files.json")
every_bg_list = ["TprimeToTZ_1000_2018","TT_hadr_2018"] #testing
#every_bg_list  = crabout['meta_info']['backgroun_list']
luminosity = 137000 #bp^-1
l_th = 0.23199999332427979
h_th = 0.164000004529953

c0 = ROOT.TCanvas("canvas", "Score Stack Plot", 800, 600)
#c1 = ROOT.TCanvas("canvas", "Score Stack Plot", 800, 600)
#c2 = ROOT.TCanvas("canvas", "Score Stack Plot", 800, 600)
#c3 = ROOT.TCanvas("canvas", "Score Stack Plot", 800, 600)
hs_ds700 = ROOT.THStack("hs_ds700", "Stack plot Deep Score 700")
hs_ds1000 = ROOT.THStack("hs_ds1000", "Stack plot Deep Score 1000")
hs_ds1800 = ROOT.THStack("hs_ds1800", "Stack plot Deep Score 1800")
hs_met = ROOT.THStack("hs_met", "Stack plot")

h_ds_list_700  = []
h_ds_list_1000 = []
h_ds_list_1800 = []
h_met_list     = []

for bg in every_bg_list:
    filenames = read_and_list(crabout["meta_info"]["parent_path"] + bg + ".txt")
    
    h_ds_list_700.append(ROOT.TH1F("deepsc_tp700"   + bg, "deepsc_tp700" , 250, 0 ,1))
    h_ds_list_1000.append(ROOT.TH1F("deepsc_tp1000" + bg, "deepsc_tp1000", 250, 0 ,1))
    h_ds_list_1800.append(ROOT.TH1F("deepsc_tp1800" + bg, "deepsc_tp1800", 250, 0 ,1))
    h_met_list.append(ROOT.TH1F("MET_pt" + bg, "MET", 250, 0 ,1))

    #h_ds700   = ROOT.TH1F("deepsc_tp700"+bg, "deepsc_tp700"  , 250, 0 ,1)
    #print(h_ds700)
    #h_ds1000  = ROOT.TH1F("deepsc_tp1000"+bg, "deepsc_tp1000" , 250, 0 ,1)
    #h_ds1800  = ROOT.TH1F("deepsc_tp1800"+bg, "deepsc_tp1800" , 250, 0 ,1)
    #h_met = ROOT.TH1F('MET_pt'+bg, 'MET', 250,200,1000)
    weight = 0
    for i, infile in enumerate(filenames):
        temp_file = ROOT.TFile.Open(infile)
        tree = NanoEventsFactory.from_root(infile, schemaclass=NanoAODSchema.v6).events()
        #temp_tree = temp_file.Events
        weight += (temp_file.plots.Get('h_genweight')).GetBinContent(1)
        
        scores_700   = tree.deepsc.tp700
        scores_1000  = tree.deepsc.tp1000
        scores_1800  = tree.deepsc.tp1800
        met = tree.MET.pt

        #scores_700   = tree.deepsc[ak.any(tree.TopLowPt.scoreDNN > l_th) + ak.any(tree.TopHighPt.score2 > h_th)].tp700
        #scores_1000  = tree.deepsc[(ak.any(tree.TopLowPt.scoreDNN > l_th)) + ak.any((tree.TopHighPt.score2 > h_th))].tp1000
        #scores_1800  = tree.deepsc[ak.any((tree.TopLowPt.scoreDNN > l_th)) + ak.any((tree.TopHighPt.score2 > h_th))].tp1800
        #met          = tree.MET[ak.any((tree.TopLowPt.scoreDNN > l_th)) + ak.any((tree.TopHighPt.score2 > h_th))].pt

        for score in scores_700:
            h_ds_list_700[-1].Fill(score)
        for score in scores_1000:
            h_ds_list_1000[-1].Fill(score)
        for score in scores_1800:
            h_ds_list_1800[-1].Fill(score)
        for met_pt in met:
            h_met_list[-1].Fill(met_pt)

    k = scaling_factor(sample_dict = sample_dict,
                       name_string = bg,
                       luminosity = luminosity,
                       weight = weight)
    

    #print(h_ds_list_700[-1])
    h_ds_list_700[-1].Scale(k)
    h_ds_list_1000[-1].Scale(k)
    h_ds_list_1800[-1].Scale(k)
    h_met_list[-1].Scale(k)

    #h_ds1000.Scale(k)
    #h_ds1800.Scale(k)
    #h_met.Scale(k)
    '''
    rfile = ROOT.TFile(crabout["meta_info"]["eos_stk"] + bg +'.root', "RECREATE")
    h_ds700.Write()
    h_ds1000.Write()
    h_ds1800.Write()
    h_met.Write()
    rfile.Close()
    '''
    hs_ds700.Add(h_ds_list_700[-1])
    hs_ds1000.Add(h_ds_list_1000[-1])
    hs_ds1800.Add(h_ds_list_1800[-1])
    hs_met.Add(h_met_list[-1])

hs_ds700.Draw("nostack")
c0.SaveAs(crabout['meta_info']['eos_stk'] + "700_try_plot_stack.png")
c0.Clear()
hs_ds1000.Draw("nostack")
c0.SaveAs(crabout['meta_info']['eos_stk'] + "1000_try_plot_stack.png")
c0.Clear()
hs_ds1800.Draw("nostack")
c0.SaveAs(crabout['meta_info']['eos_stk'] + "1800_try_plot_stack.png")
c0.Clear()
hs_met.Draw("nostack")
c0.SaveAs(crabout['meta_info']['eos_stk'] + "MET_try_plot_stack.png")
c0.Clear()