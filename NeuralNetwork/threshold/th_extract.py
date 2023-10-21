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
                    required = False,
                    default  = False)
parser.add_argument("-s", "--save",
                    type     = int,
                    help     = "Save the output in a useful well-formatted JSON file called th_bg_SS.json. Input the thrashold percentage for background",
                    required = True)
options = parser.parse_args()

##############
#    MAIN    #
##############
if not options.verbose and options.save:
    print("Save a json file without any output")
print('WARNING: reading the th_eval.py output, make sure it ran before me')

crabout = json_reader("crabout_files.json")
print("Avvio lettura delle threshold...")

th_datas, data_names = data_storing(crabout, efficiency = options.save, verbose = options.verbose)

if options.save:
    json_output = crabout['meta_info']['eos_path']+'threshold_outputs/outputs_json/'+ "thresholds_bg_" + str(options.save) + ".json"
    
    th_datas["meta_info"] = {} #potrebbe servirmi avere una lista coi nomi del dizionario
    th_datas["meta_info"]['data_names'] = data_names
    th_datas["meta_info"]['lowhigh'] = ['Low_Threshold', 'High_Threshold']

    saveas_json(dict = th_datas, filename = json_output)
    print("\nSaved file as " + json_output)
