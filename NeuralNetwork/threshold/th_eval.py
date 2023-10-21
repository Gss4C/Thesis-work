import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.threshold.thresholding_class import *
import warnings
import argparse
warnings.filterwarnings("ignore")

###################
#    Arguments    #
###################
parser = argparse.ArgumentParser(description = "Threshold computation")
parser.add_argument("-e", "--efficiency",
                    type     = int,
                    help     = "Input the threshold background percentage: how much background will survive above this threshold",
                    required = True)
parser.add_argument("-b", "--bondedpt",
                    type     = bool,
                    help     = "If true I will make histograms with an extra pt bond: Pt>300 for highpt and Pt<300 for lowpt",
                    required = True)
options = parser.parse_args()

crabout = json_reader("crabout_files.json")
print('I will compute threshold with the '+ str(options.efficiency) + '%' +' background efficiency')
bg_efficiency = options.efficiency/100

for cluster in crabout["meta_info"]["cluster_names"]:
    print("\ninizio del cluster: " + cluster + "\n")
    for index in range(len(crabout[cluster])):
        completamento = index/(len(crabout[cluster])) 
        percentuale   = completamento*100
        percentuale_troncata = round(percentuale, 2)
        print("Completamento cluster: " + str(percentuale_troncata) + "%")
        
        batch_files_list = read_and_list(crabout["meta_info"]["parent_path"] + crabout[cluster][index])
        dataset_name  = crabout[cluster][index].replace(".txt","")
        root_filename = crabout[cluster][index].replace(".txt",".root") 
        print("Elaborazione del dataset: "+ dataset_name)

        N_bins = 250
        h_lowF  = ROOT.TH1F("Lowpt_False" + dataset_name ,"Lowpt_False" + dataset_name , N_bins, 0 ,1)
        h_lowT  = ROOT.TH1F("Lowpt_True" + dataset_name  ,"Lowpt_True" + dataset_name  , N_bins, 0 ,1)
        h_highF = ROOT.TH1F("Highpt_False" + dataset_name,"Highpt_False" + dataset_name, N_bins, 0 ,1)
        h_highT = ROOT.TH1F("Highpt_True" + dataset_name ,"Highpt_True" + dataset_name , N_bins, 0 ,1)

        histomaker = thrashold_histomaker()
        histomaker.crea_4histo(batch_files_list = batch_files_list, 
                               h_lowF  = h_lowF, 
                               h_lowT  = h_lowT, 
                               h_highF = h_highF, 
                               h_highT = h_highT, 
                               dataset_name  = dataset_name,
                               bg_efficiency = bg_efficiency,
                               pt_bond       = options.bondedpt)
        if options.bondedpt:
            file = ROOT.TFile(crabout["meta_info"]["eos_path"]+'threshold_outputs/'+ str(options.efficiency)+ "/" + root_filename, "RECREATE")
        else:
            file = ROOT.TFile(crabout["meta_info"]["eos_path"] + root_filename, "RECREATE")
        
        h_highF.Write()
        h_highT.Write()
        h_lowF.Write()
        h_lowT.Write()
        
        file.Close()

        print('DONE')