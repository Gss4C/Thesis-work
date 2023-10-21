import ROOT
import argparse
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.Thesis.efficiency.classes_efficiency import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import awkward as ak

###################
#    FWJD Alert    #
###################

parser = argparse.ArgumentParser(description = "Threshold computation")
parser.add_argument("-t", "--threshold",
                    type     = int,
                    help     = "Select if use the Threshold of TprimeToTZ_1000_2018 by 10, 5 or 1",
                    required = True)
parser.add_argument("-c", "--cluster",
                    type     = str,
                    help     = "Select clusters",
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

def met_condition(collect_H, h_th, collect_L, l_th):
    out_bool = False
    for top in collect_H:
        if top.score2 > h_th:
            out_bool = True
    for top in collect_L:
        if top.scoreDNN > l_th:
            out_bool = True
    return out_bool

luminosity = 137000
#for cluster in crabout[opt.cluster]: #entro nel cluster
print("\ninizio del cluster: " + opt.cluster + "\n")
for index in range(len(crabout[opt.cluster])): 
    #####################
    #    Nel Dataset    #
    #####################
    completamento = index/(len(crabout[opt.cluster])) 
    percentuale   = completamento*100
    percentuale_troncata = round(percentuale, 2)
    print("Completamento cluster: " + str(percentuale_troncata) + "%")

    batch_files_list = read_and_list(crabout["meta_info"]["parent_path"] + crabout[opt.cluster][index])
    dataset_name  = crabout[opt.cluster][index].replace(".txt","")
    new_root_filename = crabout[opt.cluster][index].replace(".txt",".root")

    gen_weight = 0
    N_bins = 250
    h_score_dnn  = ROOT.TH1F("TopLowPt_scoreDNN", "TopLowPt_scoreDNN",N_bins, 0 ,1)
    h_score2     = ROOT.TH1F("TopHighPt_score2", "TopHighPt_score2", N_bins, 0 ,1)
    h_met_pt     = ROOT.TH1F("MET_pt", "MET_pt", N_bins, 200 ,1200)

    #ciclo filling di histo per singolo dataset
    for i, infile in enumerate(batch_files_list): #entro nel batch
        temp_file = ROOT.TFile.Open(infile)
        temp_tree = temp_file.Events
        gen_weight += (temp_file.plots.Get('h_genweight')).GetBinContent(1)

        for event in range(temp_tree.GetEntries()): #entro negli eventi
            if event%1000 == 0:
                percentuale = float(event/temp_tree.GetEntries() * 100)
                percentuale_troncata = round(percentuale, 2)
                print("Completamento batch: " + str(percentuale_troncata) + '%')
            temp_tree.GetEntry(event)
            tophigh = Collection(temp_tree, "TopHighPt")
            toplow  = Collection(temp_tree, "TopLowPt")
            met     = Object(temp_tree, "MET")

            draw_event = met_condition(collect_H = tophigh,
                                        collect_L = toplow,
                                        h_th      = h_th,
                                        l_th      = l_th)
            if draw_event:
                h_met_pt.Fill(met.pt)
            for top in tophigh:
                if top.score2 > h_th:
                    h_score2.Fill(top.score2)
            for top in toplow:
                if top.scoreDNN > l_th:
                    h_score_dnn.Fill(top.scoreDNN)
        temp_file.Close()
        #scalare istogrammi
    sigma = sample_dict[dataset_name].sigma

    h_score_dnn.Scale(sigma * luminosity / (gen_weight))
    h_score2.Scale(sigma * luminosity / (gen_weight))
    h_met_pt.Scale(sigma * luminosity / (gen_weight))

    file = ROOT.TFile(crabout['meta_info']['eos_histo_fwdj'] + str(opt.threshold) +"/Th_" +str(opt.threshold) + "_" + new_root_filename, "RECREATE")
    h_score_dnn.Write()
    h_score2.Write()
    h_met_pt.Write()
    file.Close()
    print("DONE")