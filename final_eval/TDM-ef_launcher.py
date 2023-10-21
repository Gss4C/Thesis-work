#   ISTRUZIONI   #
#Ordine: 3
#Input:  Json con threshold da th_maker.py
#Output: Plots.png delle efficienze, json dei conteggi, tutto per ogni dataset
#Prev:   th_maker.py
#Next:   sig_recluster.py

#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.ef_sig_class import *
import ROOT
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description = "Efficiency of the selection counter")
parser.add_argument("-c", "--cluster",
                    type     = str,
                    help     = "Choose the cluster: TT_2018, QCD_2018, ZJetsToNuNu_2018, Tprime or one of the tdm dataset",
                    required = True)
parser.add_argument("-t", "--threshold",
                    type     = int,
                    help     = "Select if use the Threshold of TprimeToTZ_1000_2018 by 10, 5 or 1",
                    required = True)
opt = parser.parse_args()

crabout = json_reader("crabout_files.json")

if opt.threshold == 1:
    th_dict = json_reader(crabout['meta_info']['eos_th'] + 'thresholds_1.json')
elif opt.threshold == 5:
    th_dict = json_reader(crabout['meta_info']['eos_th'] + 'thresholds_5.json')
elif opt.threshold == 10:
    th_dict = json_reader(crabout['meta_info']['eos_th'] + 'thresholds_10.json')

tdm_names = ['tdm-1000','tdm-500','tdm-50']
if opt.cluster == 'tdm-1000':
    weight = 27000
elif opt.cluster == 'tdm-500':
    weight = 28000
elif opt.cluster == 'tdm-50':
    weight = 12188


#th trovate per il top scelte con la misID al 5%
l_th = 0.23199999332427979
h_th = 0.164000004529953

output_diz = {}
for index in range(len(crabout[opt.cluster])):
    #print('Completamento cluster ' + str(float(index/len(crabout[opt.cluster]) * 100)) + "%")

    ########################
    #    Single Dataset    #
    ########################
    if opt.cluster in tdm_names:
        if opt.cluster == 'tdm-1000':
            filenames = ["../../../../../../../src/PhysicsTools/NanoAODTools/crab/tDM_mPhi1000_mChi1_Skim.root"]
            dataset = "tDM_mPhi1000_mChi1_Skim"
        elif opt.cluster == 'tdm-500':
            filenames = ["../../../../../../../src/PhysicsTools/NanoAODTools/crab/tDM_mPhi500_mChi1_Skim.root"]
            dataset = "tDM_mPhi500_mChi1_Skim"
        elif opt.cluster == 'tdm-50':
            filenames = ["../../../../../../../src/PhysicsTools/NanoAODTools/crab/tDM_mPhi50_mChi1_Skim.root"]
            dataset = "tDM_mPhi50_mChi1_Skim"
    else:
        filenames = read_and_list(crabout["meta_info"]["parent_path"] + crabout[opt.cluster][index])
        dataset = crabout[opt.cluster][index].replace('.txt', '')


    output_diz[dataset] = {}

    print('\nStarting dataset: ' + dataset)
    #definizione contatori
    sel_700 = 0
    sel_700_fwd = 0
    sel_1000 = 0
    sel_1000_fwd = 0
    sel_1800 = 0
    sel_1800_fwd = 0
    #weight = 0

    for i, infile in enumerate(filenames):
        
        temp_file = ROOT.TFile.Open(infile)
        temp_tree = temp_file.Events
        #weight += (temp_file.plots.Get('h_genweight')).GetBinContent(1)
        print('Events in batch: ' + str(temp_tree.GetEntries()))
        
        for event in range(temp_tree.GetEntries()):
            if event%1000 == 0:
                percentuale = float(event/temp_tree.GetEntries() * 100)
                percentuale_troncata = round(percentuale, 2)
                print("Completamento batch: " + str(percentuale_troncata) + '%')
            
            temp_tree.GetEntry(event)
            deepsc  = Object(temp_tree, "deepsc")
            jets    = Collection(temp_tree, "Jet")
            tophigh = Collection(temp_tree, "TopHighPt")
            toplow  = Collection(temp_tree, "TopLowPt")

            cond_high, cond_low = top_conditions(collection_high = tophigh, collection_low = toplow, low_th = l_th, high_th = h_th)
            valid_700, valid_1000, valid_1800 = conditions(scores_object = deepsc, threshold_dict = th_dict) 
            with_forwardjet_event = is_event_fwd(jets)

            if (cond_high or cond_low):
                if valid_700:
                    if with_forwardjet_event:
                        sel_700_fwd += 1
                    else:
                        sel_700 += 1
                
                if valid_1000:
                    if with_forwardjet_event:
                        sel_1000_fwd += 1
                    else:
                        sel_1000 += 1
                
                if valid_1800:
                    if with_forwardjet_event:
                        sel_1800_fwd += 1
                    else:
                        sel_1800 += 1

        temp_file.Close()

    eff_sel_700 = float(sel_700)/weight
    eff_sel_700_fwd = float(sel_700_fwd)/weight
    eff_sel_1000 = float(sel_1000)/weight
    eff_sel_1000_fwd = float(sel_1000_fwd)/weight
    eff_sel_1800 = float(sel_1800)/weight
    eff_sel_1800_fwd = float(sel_1800_fwd)/weight


    output_diz[dataset]['th_700']      = sel_700
    output_diz[dataset]['th_700_fwd']  = sel_700_fwd
    output_diz[dataset]['th_1000']     = sel_1000
    output_diz[dataset]['th_1000_fwd'] = sel_1000_fwd
    output_diz[dataset]['th_1800']     = sel_1800
    output_diz[dataset]['th_1800_fwd'] = sel_1800_fwd
    output_diz[dataset]['weight']      = weight
    
    plotter(eff_sel_700_fwd, 
            eff_sel_700, 
            eff_sel_1000_fwd, 
            eff_sel_1000,
            eff_sel_1800_fwd,
            eff_sel_1800,
            opt.threshold, 
            dataset, 
            crabout['meta_info']['eos_ef'])
    
if opt.cluster in tdm_names:
    if opt.cluster == 'tdm-1000':
        dataname = opt.cluster.replace("-1000", "_1000")
    elif opt.cluster == 'tdm-500':
        dataname = opt.cluster.replace("-500", "_500")
    elif opt.cluster == 'tdm-50':
        dataname = opt.cluster.replace("-50", "_50")
saveas_json(output_diz, crabout['meta_info']['eos_ef']+'ttodm/util_jsons/' + str(opt.threshold)+"_" +dataname + '.json')