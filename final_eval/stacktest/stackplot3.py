import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.stack_class import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
import warnings
import argparse
warnings.filterwarnings("ignore")

#aggiungere argparse per scegliere il segnale, legato ad una stringa che viene appesa a every_bg_list

crabout = json_reader("crabout_files.json")

bg_qcd = crabout['meta_info']['backgrounds_QCD']
bg_tt = crabout['meta_info']['backgrounds_TT']
bg_zjtnn = crabout['meta_info']['backgrounds_ZJTNN']
every_background = [bg_qcd, bg_tt, bg_zjtnn]

#queste liste servono solo per i fondi
h_list_700 = []
h_list_1000 = []
h_list_1800 = []
h_list_met = []

c0 = ROOT.TCanvas("canvas", "Score Stack Plot", 800, 600)
#in ogni segnale vanno prodotti tutti questi stack
hs_ds700 = ROOT.THStack("hs_ds700", "Stack plot Deep Score 700")
hs_ds1000 = ROOT.THStack("hs_ds1000", "Stack plot Deep Score 1000")
hs_ds1800 = ROOT.THStack("hs_ds1800", "Stack plot Deep Score 1800")
hs_met = ROOT.THStack("hs_met", "Stack plot MET_pt")

'''
for component in every_background: #fisso la lista di backgrounds
    for index, single_background in enumerate(component):
        percentuale = round(index/(len(component)) * 100, 2)
        print("Completamento dataset background: " + str(percentuale) + "%")
        
        batch_files_list = read_and_list(crabout["meta_info"]["parent_path"] + component[index] + ".txt")
        dataset_name  = component[index]
        root_filename = component[index] + ".root"
        print("Elaborazione background: "+ dataset_name)

        h_ds700   = ROOT.TH1F("deepsc_tp700_"  + dataset_name, "deepsc_tp700"  + dataset_name , N_bins, 0 ,1)
        h_ds1000  = ROOT.TH1F("deepsc_tp1000_" + dataset_name, "deepsc_tp1000" + dataset_name , N_bins, 0 ,1)
        h_ds1800  = ROOT.TH1F("deepsc_tp1800_" + dataset_name, "deepsc_tp1800" + dataset_name , N_bins, 0 ,1)
        h_met = ROOT.TH1F("MET_" + dataset_name, "MET_" + dataset_name, N_bins, 0, 2000)

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
        
        h_ds700.SetFillColorAlpha(sample_dict[dataset_name].color,  1)
        h_ds1000.SetFillColorAlpha(sample_dict[dataset_name].color, 1)
        h_ds1800.SetFillColorAlpha(sample_dict[dataset_name].color, 1)
        h_met.SetFillColorAlpha(sample_dict[dataset_name].color,    1)

        if single_background != component[-1]: #solo se is ultimo in ordine nella lista dei components deve avere trasparenza massima
            h_ds700.SetFillColorAlpha(sample_dict[dataset_name].color,  0)
            h_ds1000.SetFillColorAlpha(sample_dict[dataset_name].color, 0)
            h_ds1800.SetFillColorAlpha(sample_dict[dataset_name].color, 0)
            h_met.SetFillColorAlpha(sample_dict[dataset_name].color,    0)

        h_list_700.append(h_ds700)
        h_list_1000.append(h_ds1000)
        h_list_1800.append(h_ds1800)
        h_list_met.append(h_met)
        print('DONE')

for score7, score10, score18, met in zip(h_list_700, h_list_1000, h_list_1800, h_list_met):
    hs_ds700.Add(score7)
    hs_ds1000.Add(score10)
    hs_ds1800.Add(score18)
    hs_met.Add(met)

c0.SetLogy()
hs_ds700.Draw('hist')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "700_try_plot_stack.png")
c0.Clear()
c0.SetLogy()
hs_ds1000.Draw('hist')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "1000_try_plot_stack.png")
c0.Clear()
c0.SetLogy()
hs_ds1800.Draw('hist')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "1800_try_plot_stack.png")
c0.Clear()
c0.SetLogy()
hs_met.Draw('hist')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "MET_try_plot_stack.png")
c0.Clear()
'''



every_bg_list =["TprimeToTZ_1000_2018", "ZJetsToNuNu_HT800to1200_2018"]
color_list = [ROOT.kRed, ROOT.kBlue]
for index, color in zip(range(len(every_bg_list)), color_list):
    completamento = index/(len(every_bg_list)) 
    percentuale   = completamento*100
    percentuale_troncata = round(percentuale, 2)
    print("Completamento dataset background: " + str(percentuale_troncata) + "%")
    
    batch_files_list = read_and_list(crabout["meta_info"]["parent_path"] + every_bg_list[index] + ".txt")
    dataset_name  = every_bg_list[index]
    root_filename = every_bg_list[index] + ".root"
    print("Elaborazione del dataset: "+ dataset_name)

    
    h_ds700   = ROOT.TH1F("deepsc_tp700_"  + dataset_name, "deepsc_tp700"  + dataset_name , N_bins, 0 ,1)
    h_ds1000  = ROOT.TH1F("deepsc_tp1000_" + dataset_name, "deepsc_tp1000" + dataset_name , N_bins, 0 ,1)
    h_ds1800  = ROOT.TH1F("deepsc_tp1800_" + dataset_name, "deepsc_tp1800" + dataset_name , N_bins, 0 ,1)
    h_met = ROOT.TH1F("MET_" + dataset_name, "MET_" + dataset_name, N_bins, 0, 2000)

    
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
    '''
    h_ds700.SetFillColor(color)
    h_ds1000.SetFillColor(color)
    h_ds1800.SetFillColor(color)
    h_met.SetFillColor(color)
    '''
    h_list_700.append(h_ds700)
    h_list_1000.append(h_ds1000)
    h_list_1800.append(h_ds1800)
    h_list_met.append(h_met)
    print('DONE')

for score7, score10, score18, met in zip(h_list_700, h_list_1000, h_list_1800,h_list_met):
    hs_ds700.Add(score7)
    hs_ds1000.Add(score10)
    hs_ds1800.Add(score18)
    hs_met.Add(met)

c0.SetLogy()
hs_ds700.Draw('hist')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "HELP_700_try_plot_stack.png")
c0.Clear()

c0.SetLogy()
hs_ds1000.Draw('hist')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "HELP_1000_try_plot_stack.png")
c0.Clear()

c0.SetLogy()
hs_ds1800.Draw('hist')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "HELP_1800_try_plot_stack.png")
c0.Clear()

c0.SetLogy()
hs_met.Draw('hist')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "HELP_MET_try_plot_stack.png")
c0.Clear()
