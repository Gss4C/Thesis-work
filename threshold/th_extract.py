import ROOT
import argparse
import json
from PhysicsTools.NanoAODTools.postprocessing.Thesis.threshold.thresholding_class import *

###################
#    Arguments    #
###################
parser = argparse.ArgumentParser(description = "Threshold reading and elaboration")
parser.add_argument("-v", "--verbose",
                    type     = bool,
                    help     = "If true print output on screen",
                    required = False)
parser.add_argument("-b", "--bondedpt",
                    type     = bool,
                    help     = "True if you want to take histos from bondedpt folder",
                    required = True)
parser.add_argument("-s", "--save",
                    type     = int,
                    help     = "Save the output in a useful well-formatted JSON file called th_bg_SS.json. Input the thrashold percentage for background",
                    required = True)
options = parser.parse_args()

###################
#    Functions    #
###################
def data_storing(json_file):
    data_storage = {}
    if options.save:
        data_names = []
    print("Lettura e storing dei dati...")
    for cluster in json_file["meta_info"]["cluster_names"]:
        print("\n\nCluster " + cluster )
        for index in range(len(json_file[cluster])):
            if options.bondedpt:
                root_file_pathname = json_file["meta_info"]["eos_path_bond"] + json_file[cluster][index].replace(".txt", ".root")
            else:
                root_file_pathname = json_file["meta_info"]["eos_path"] + json_file[cluster][index].replace(".txt", ".root")
            root_file = ROOT.TFile(root_file_pathname, "Open")
            data_name = json_file[cluster][index].replace(".txt", "")
            if options.save:
                data_names.append(data_name)

            if data_name not in data_storage:
                data_storage[data_name] = {}  # Inizializza il dizionario, altrimenti rompe il cazzo

            h_LF = root_file.Get("Lowpt_False"  + data_name)
            h_HF = root_file.Get("Highpt_False" + data_name)

            low_th  = h_LF.GetBinContent(0)
            high_th = h_HF.GetBinContent(0)

            data_storage[data_name]["Low_Threshold"]  = low_th
            data_storage[data_name]["High_Threshold"] = high_th

            if options.verbose:
                print("\nDataset: " + data_name)
                print("Low Pt Threshold: " + str(data_storage[data_name]["Low_Threshold"]))
                print("High Pt Threshold:" + str(data_storage[data_name]["High_Threshold"]))
    return data_storage, data_names

def saveas_json(dict, filename):
    with open(filename, 'w') as file:
        json.dump(dict, file)

##############
#    MAIN    #
##############
if not options.verbose and options.save:
    print("Save a json file without any output")
print('WARNING: reading the th_eval.py output, make sure it ran before me')

filenames = json_reader("crabout_files.json")
print("Avvio lettura delle threshold, saranno mostrate le soglie calcolate da th_eval.py che permettono di scartare lo 0.9 dei false")

th_datas, data_names = data_storing(filenames)
if options.save:
    if options.bondedpt:
        json_output = "th_bg_bond_" + str(options.save) + ".json"
    else:
        json_output = "th_bg_" + str(options.save) + ".json"
    
    th_datas["meta_info"] = {}
    th_datas["meta_info"]['data_names'] = data_names
    th_datas["meta_info"]['lowhigh'] = ['Low_Threshold', 'High_Threshold']

    saveas_json(dict = th_datas, filename = json_output)
    print("\nSaved file here as " + json_output)
