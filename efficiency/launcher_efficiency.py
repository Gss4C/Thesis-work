#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.Thesis.efficiency.classes_efficiency import *
import ROOT
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description = "Threshold computation")
parser.add_argument("-c", "--cluster",
                    type     = str,
                    help     = "Choose the cluster: TT_2018, QCD_2018, ZJetsToNuNu_2018, Tprime",
                    required = True)
parser.add_argument("-t", "--threshold",
                    type     = int,
                    help     = "Select if use the Threshold of TprimeToTZ_1000_2018 by 10, 5 or 1",
                    required = True)
opt = parser.parse_args()

if opt.threshold == 1:
    l_th = 0.5120000243186951
    h_th = 0.5879999995231628
elif opt.threshold == 5:
    l_th = 0.23199999332427979
    h_th = 0.164000004529953
elif opt.threshold == 10:
    l_th = 0.11999999731779099
    h_th = 0.03999999910593033

crabout = json_reader("crabout_files.json")
output_diz = {}

for index in range(len(crabout[opt.cluster])):
    print('Completamento cluster ' + str(float(index/len(crabout[opt.cluster]) * 100)) + "%")

    ########################
    #    Single Dataset    #
    ########################
    dataset = crabout[opt.cluster][index].replace('.txt', '')
    output_diz[dataset] = {}

    print('\n Starting dataset: ' + dataset)
    filenames = read_and_list(crabout["meta_info"]["parent_path"] + crabout[opt.cluster][index])

    sel_toplow_fwd  = 0
    sel_tophigh_fwd = 0
    sel_toplow  = 0
    sel_tophigh = 0
    weight = 0

    for i, infile in enumerate(filenames):
        
        temp_file = ROOT.TFile.Open(infile)
        temp_tree = temp_file.Events
        weight += (temp_file.plots.Get('h_genweight')).GetBinContent(1)
        print('Events in batch: ' + str(temp_tree.GetEntries()))
        
        for event in range(temp_tree.GetEntries()):
            if event%1000 == 0:
                percentuale = float(event/temp_tree.GetEntries() * 100)
                percentuale_troncata = round(percentuale, 2)
                print("Completamento batch: " + str(percentuale_troncata) + '%')
            
            temp_tree.GetEntry(event)
            tophigh = Collection(temp_tree, "TopHighPt")
            toplow  = Collection(temp_tree, "TopLowPt")

            h_fwd, l_fwd = conditions(tophigh, toplow, l_th, h_th) 

            if h_fwd:
                sel_tophigh_fwd += 1
            elif (not h_fwd) and len(tophigh):
                sel_tophigh += 1

            if l_fwd:
                sel_toplow_fwd += 1
            elif (not l_fwd) and len(toplow):
                sel_toplow += 1
        temp_file.Close()

    eff_sel_tophigh_fwd = float(sel_tophigh_fwd)/weight
    eff_sel_tophigh     = float(sel_tophigh)/weight
    eff_sel_toplow_fwd  = float(sel_toplow_fwd)/weight
    eff_sel_toplow      = float(sel_toplow)/weight

    output_diz[dataset]['TopHigh_fwd'] = sel_tophigh_fwd
    output_diz[dataset]['TopHigh']     = sel_tophigh
    output_diz[dataset]['TopLow_fwd']  = sel_toplow_fwd
    output_diz[dataset]['TopLow']      = sel_toplow
    output_diz[dataset]['weight']      = weight

    plotter(eff_sel_tophigh_fwd, eff_sel_tophigh, eff_sel_toplow_fwd, eff_sel_toplow, opt.threshold, dataset, crabout['meta_info']['eos_plot_path'])
saveas_json(output_diz, crabout['meta_info']['eos_count_path'] + str(opt.threshold)+"_" +opt.cluster + '.json')