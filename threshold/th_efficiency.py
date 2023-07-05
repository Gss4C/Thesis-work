import ROOT
import argparse
import json
from PhysicsTools.NanoAODTools.postprocessing.Thesis.threshold.thresholding_class import *

def saveas_json(dict, filename):
    with open(filename, 'w') as file:
        json.dump(dict, file)

parser = argparse.ArgumentParser(description = "Threshold reading and elaboration")
parser.add_argument("-b", "--bondedpt",
                    type     = bool,
                    help     = "True if you want to take histos from bondedpt folder",
                    required = True)
options = parser.parse_args()

json_file = json_reader("crabout_files.json")
if options.bondedpt:
    th1_json  = json_reader("th_bg_bond_1.json")
    th5_json  = json_reader("th_bg_bond_5.json")
    th10_json = json_reader("th_bg_bond_10.json")
else:
    th1_json  = json_reader("th_bg_1.json")
    th5_json  = json_reader("th_bg_5.json")
    th10_json = json_reader("th_bg_10.json")
j_list   = [th1_json,th5_json,th10_json] 

print("Lettura e storing dei dati...")
for cluster in json_file["meta_info"]["cluster_has_trues"]:
    print("\n\nCluster " + cluster )
    for index in range(len(json_file[cluster])):
        if options.bondedpt:
            root_file_pathname = json_file["meta_info"]["eos_path_bond"] + json_file[cluster][index].replace(".txt", ".root")
        else:
            root_file_pathname = json_file["meta_info"]["eos_path_bond"] + json_file[cluster][index].replace(".txt", ".root")
        root_file = ROOT.TFile(root_file_pathname, "Open")
        data_name = json_file[cluster][index].replace(".txt", "")

        h_HT = root_file.Get("Highpt_True" + data_name)
        h_LT = root_file.Get("Lowpt_True"  + data_name)

        for j_file in j_list:
            high_th = j_file[data_name]["High_Threshold"]
            low_th  = j_file[data_name]["Low_Threshold"]

            high_th_bin = h_HT.FindBin(high_th)
            low_th_bin  = h_LT.FindBin(low_th)

            high_full_integral = h_HT.Integral()
            low_full_integral  = h_LT.Integral()

            high_right_integral = h_HT.Integral(high_th_bin, 250)
            low_right_integral  = h_LT.Integral(low_th_bin,  250)

            high_efficiency = high_right_integral/high_full_integral
            low_efficiency  = low_right_integral/low_full_integral

            j_file[data_name]["High_Efficiency"] = high_efficiency
            j_file[data_name]["Low_Efficiency"] = low_efficiency

print('Salvataggio file...')
if options.bondedpt:
    saveas_json(th1_json,  "th_bg_bond_1.json")
    saveas_json(th5_json,  "th_bg_bond_5.json")
    saveas_json(th10_json, "th_bg_bond_10.json")
else:
    saveas_json(th1_json, "th_bg_1.json")
    saveas_json(th5_json, "th_bg_5.json")
    saveas_json(th10_json, "th_bg_10.json")
print('DONE')