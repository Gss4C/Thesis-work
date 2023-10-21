import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.stack_class import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
import argparse

parser = argparse.ArgumentParser(description = "Threshold computation")
parser.add_argument("-d", "--dataset",
                    type     = str,
                    help     = "Choose the dataset to launch",
                    required = True)
opt = parser.parse_args()


crabout = json_reader("crabout_files.json")
single_dataset = crabout[opt.dataset][0]

batch_files_list = read_and_list(crabout["meta_info"]["parent_path"] + single_dataset + ".txt")
dataset_name  = single_dataset
root_filename = single_dataset + ".root"

h_ds700   = ROOT.TH1F("deepsc_tp700_"  + dataset_name, "deepsc_tp700"  + dataset_name , N_bins, 0 ,0.6)
h_ds1000  = ROOT.TH1F("deepsc_tp1000_" + dataset_name, "deepsc_tp1000" + dataset_name , N_bins, 0 ,1)
h_ds1800  = ROOT.TH1F("deepsc_tp1800_" + dataset_name, "deepsc_tp1800" + dataset_name , N_bins, 0 ,1)
h_met = ROOT.TH1F("MET_" + dataset_name, "MET_" + dataset_name, 20, 200, 1200)

stacker = stack_plotter()
weight = stacker.fill_4_histos(batch_files_list = batch_files_list, 
                                h_ds700  = h_ds700,
                                h_ds1000 = h_ds1000,
                                h_ds1800 = h_ds1800,
                                h_met = h_met,
                                dataset_name  = dataset_name)
k = scaling_factor(sample_dict = sample_dict,
                    name_string = dataset_name,
                    luminosity = luminosity,
                    weight = weight)


h_ds700.Scale(k)
h_ds1000.Scale(k)
h_ds1800.Scale(k)
h_met.Scale(k)

new_root_file = ROOT.TFile(crabout["meta_info"]["eos_stk"]+'root_files/' + root_filename, "RECREATE")
h_ds700.Write()
h_ds1000.Write()
h_ds1800.Write()
h_met.Write()
new_root_file.Close()

print('DONE')