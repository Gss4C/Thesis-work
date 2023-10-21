####################
#    Parameters    #
####################
seed_value = 123
dropout    = 0.1
epochs     = 200
batch_size = 100

luminosity = 137000 #pb
bins = 30

#models_local_path = "/afs/cern.ch/user/j/jbonetti/CMSSW_12_4_7/src/PhysicsTools/NanoAODTools/crab/h5_models/"
#models_local_path = "../scripts/"
eos_path_dnn     = "/eos/user/j/jbonetti/NN/DNNmodel/"
path_pkl         = "/eos/user/j/jbonetti/NN/pkl_files/"
#model_name_700  = "DNN_noregions_TP_700"
#model_name_1000 = "DNN_noregions_TP_1000"
#model_name_1800 = "DNN_noregions_TP_1800"
#modelli bilanciati
model_name_700  = "DNN_noregions_bil_TP_700"
model_name_1000 = "DNN_noregions_bil_TP_1000"
model_name_1800 = "DNN_noregions_bil_TP_1800"

dizionario_per_samples = {   
    "QCD_1": "QCDHT_2000toInf_2018",
    "QCD_2": "QCDHT_1500to2000_2018",
    "QCD_3": "QCDHT_1000to1500_2018",
    "QCD_4": "QCDHT_700to1000_2018",
    "QCD_5": "QCDHT_500to700_2018",
    "QCD_6": "QCDHT_300to500_2018",
    "ZJTNN_1": "ZJetsToNuNu_HT200to400_2018",
    "ZJTNN_2": "ZJetsToNuNu_HT400to600_2018",
    "ZJTNN_3": "ZJetsToNuNu_HT600to800_2018",
    "ZJTNN_4": "ZJetsToNuNu_HT800to1200_2018",
    "ZJTNN_5": "ZJetsToNuNu_HT1200to2500_2018",
    "ZJTNN_6": "ZJetsToNuNu_HT2500toInf_2018",
    "ZJTNN_7": "ZJetsToNuNu_HT100to200_2018",
    "TT_1": "TT_Mtt1000toInf_2018",
    "TT_2": "TT_Mtt700to1000_2018",
    "TT_3": "TT_hadr_2018",
    "TT_4": "TT_semilep_2018",
    "TP_1000": "TprimeToTZ_1000_2018",
    "TP_700": "TprimeToTZ_700_2018",
    "TP_1800": "TprimeToTZ_1800_2018"
}