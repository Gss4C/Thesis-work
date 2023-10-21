import ROOT
from PhysicsTools.NanoAODTools.postprocessing.Thesis.final_eval.stack_class import *
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
#import argparse
import numpy as np

N_bins = 10
crabout = json_reader("crabout_files.json")

print('Lettura dei root files...')

bg_qcd = crabout['meta_info']['backgrounds_QCD'] 
bg_tt = crabout['meta_info']['backgrounds_TT']
bg_zjtnn = crabout['meta_info']['backgrounds_ZJTNN']
#every_background = [bg_qcd, bg_tt, bg_zjtnn]
every_background_v2 = [bg_zjtnn, bg_tt, bg_qcd]

types_names = ["QCD",  "TT", "ZJetsToNuNu"]
kinds = ['ds700','ds1000','ds1800'] #0,1,2

qcd_h_list = []
tt_h_list = []
zjtnn_h_list = []

for i in kinds:
    if i == 'ds700':
        qcd_h_list.append(ROOT.TH1F("qcd" + i,'qcd'+ i, N_bins, 0 ,0.6))
        tt_h_list.append(ROOT.TH1F("tt" + i,'tt'+ i, N_bins, 0 ,0.6))
        zjtnn_h_list.append(ROOT.TH1F("zjtnn" + i,'zjtnn'+ i, N_bins, 0 ,0.6))
    else:
        qcd_h_list.append(ROOT.TH1F("qcd" + i,'qcd'+ i, N_bins, 0 ,1))
        tt_h_list.append(ROOT.TH1F("tt" + i,'tt'+ i, N_bins, 0 ,1))
        zjtnn_h_list.append(ROOT.TH1F("zjtnn" + i,'zjtnn'+ i, N_bins, 0 ,1))

met_pt_qcd   = ROOT.TH1F("qcd", "qcd_" , 10, 200, 1200)
met_pt_tt    = ROOT.TH1F("tt", "tt_" , 10, 200, 1200)
met_pt_zjtnn = ROOT.TH1F("zjtnn", "zjtnn_" , 10, 200, 1200)

#global_bg_list = [qcd_h_list, tt_h_list, zjtnn_h_list]
global_bg_list_v2 = [zjtnn_h_list, tt_h_list, qcd_h_list]


c0 = ROOT.TCanvas("canvas", "Score Stack Plot", 1000, 769)
c0.SetFillColor(0)
c0.SetBorderMode(0)
c0.SetFrameFillStyle(0)
c0.SetFrameBorderMode(0)
c0.SetLeftMargin(0.12)
c0.SetRightMargin(0.9)
c0.SetTopMargin(1)
c0.SetBottomMargin(-1)
c0.SetTickx(1)
c0.SetTicky(1)

hs_ds700 = ROOT.THStack( "hs_ds700",   "hs_ds700")
hs_ds1000 = ROOT.THStack("hs_ds1000", "hs_ds1000")
hs_ds1800 = ROOT.THStack("hs_ds1800", "hs_ds1800")
hs_met = ROOT.THStack("hs_met", "hs_met")

metcount_bg_th700 = 0
metcount_bg_th1000 = 0
metcount_bg_th1800 = 0

th_5_1800 = 0.33
th_5_1000 = 0.41
th_5_700 = 0.35

score1800_bg_counter = 0
score1000_bg_counter = 0
score700_bg_counter = 0

print('Lettura e organizzazione dei fondi...')
for bg_h_list, background_type, bg_type, j in  zip(global_bg_list_v2, every_background_v2, types_names, range(len(global_bg_list_v2))):
    for i, background in enumerate(background_type):
        print("Compleamento tipologia background: " +str(i+1) +"/"+ str(len(background_type)))
        root_filename = crabout['meta_info']['eos_stkr'] + background + ".root"
        temp_rfile = ROOT.TFile(root_filename)

        h_700  = temp_rfile.Get('deepsc_tp700_'  + background)
        h_1000 = temp_rfile.Get('deepsc_tp1000_' + background)
        h_1800 = temp_rfile.Get('deepsc_tp1800_' + background)
        h_met  = temp_rfile.Get('MET_'           + background)
        
        bg_h_list[0].Add(h_700)
        bg_h_list[1].Add(h_1000)
        bg_h_list[2].Add(h_1800)
        score1800_bg_counter += h_1800.Integral(h_1800.FindBin(th_5_1800), 1000)
        score1000_bg_counter += h_1000.Integral(h_1000.FindBin(th_5_1000), 1000)
        score700_bg_counter += h_700.Integral(h_700.FindBin(th_5_700), 1000)
        if j == 0:
            met_pt_qcd.Add(h_met)
            metcount_bg_th700  += h_met.Integral(2,20)
            metcount_bg_th1000 += h_met.Integral(3,20)
            metcount_bg_th1800 += h_met.Integral(5,20)
        if j == 1:
            met_pt_tt.Add(h_met)
            metcount_bg_th700  += h_met.Integral(2,20)
            metcount_bg_th1000 += h_met.Integral(3,20)
            metcount_bg_th1800 += h_met.Integral(5,20)
        if j == 2:
            met_pt_zjtnn.Add(h_met)
            metcount_bg_th700  += h_met.Integral(2,20)
            metcount_bg_th1000 += h_met.Integral(3,20)
            metcount_bg_th1800 += h_met.Integral(5,20)

        bg_h_list[0].SetLineColorAlpha(sample_dict[type_sample[str(j)]].color, 100)
        bg_h_list[1].SetLineColorAlpha(sample_dict[type_sample[str(j)]].color, 100)
        bg_h_list[2].SetLineColorAlpha(sample_dict[type_sample[str(j)]].color, 100)
        
        if j == 0:
            met_pt_qcd.SetLineColorAlpha(sample_dict[type_sample[str(j)]].color, 100)
        if j == 1:
            met_pt_tt.SetLineColorAlpha(sample_dict[type_sample[str(j)]].color, 100)
        if j == 2:
            met_pt_zjtnn.SetLineColorAlpha(sample_dict[type_sample[str(j)]].color, 100)


        bg_h_list[0].SetFillColor(sample_dict[type_sample[str(j)]].color)
        bg_h_list[1].SetFillColor(sample_dict[type_sample[str(j)]].color)
        bg_h_list[2].SetFillColor(sample_dict[type_sample[str(j)]].color)
        if j == 0:
            met_pt_qcd.SetFillColor(sample_dict[type_sample[str(j)]].color)
        if j == 1:
            met_pt_tt.SetFillColor(sample_dict[type_sample[str(j)]].color)
        if j == 2:
            met_pt_zjtnn.SetFillColor(sample_dict[type_sample[str(j)]].color)

        hs_ds700.Add(bg_h_list[0])
        hs_ds1000.Add(bg_h_list[1])
        hs_ds1800.Add(bg_h_list[2])
        if j == 0:
            hs_met.Add(met_pt_qcd)
        if j == 1:
            hs_met.Add(met_pt_tt)
        if j == 2:
            hs_met.Add(met_pt_zjtnn)
        temp_rfile.Close()
print("Lettura completata.\nInizio dello stacking:\nLettura dei segnali:")

root_filename_tp7 = crabout['meta_info']['eos_stkr']  + "TprimeToTZ_700_2018.root"
rfile_tp7 = ROOT.TFile(root_filename_tp7)
h_signal_700_tp7 = rfile_tp7.Get('deepsc_tp700_TprimeToTZ_700_2018')
h_signal_700_tp7.SetLineColor(ROOT.kMagenta+1)
S_score_700 = h_signal_700_tp7.Integral(h_signal_700_tp7.FindBin(th_5_700), 1000)
h_signal_700_tp7.Rebin(100)
h_signal_1000_tp7 = rfile_tp7.Get('deepsc_tp1000_TprimeToTZ_700_2018')
h_signal_1000_tp7.SetLineColor(ROOT.kMagenta+1)
h_signal_1000_tp7.Rebin(100)
h_signal_1800_tp7 = rfile_tp7.Get('deepsc_tp1800_TprimeToTZ_700_2018')
h_signal_1800_tp7.SetLineColor(ROOT.kMagenta+1)
h_signal_1800_tp7.Rebin(100)
h_signal_MET_tp7 = rfile_tp7.Get('MET_TprimeToTZ_700_2018')
h_signal_MET_tp7.SetLineColor(ROOT.kMagenta+1)
S_700 = h_signal_MET_tp7.Integral(2,20)
h_signal_MET_tp7.Rebin(2)


root_filename_tp10 = crabout['meta_info']['eos_stkr']  + "TprimeToTZ_1000_2018.root"
rfile_tp10 = ROOT.TFile(root_filename_tp10)
h_signal_700_tp10 = rfile_tp10.Get('deepsc_tp700_TprimeToTZ_1000_2018')
h_signal_700_tp10.SetLineColor(ROOT.kOrange+7)
h_signal_700_tp10.Rebin(100)
h_signal_1000_tp10 = rfile_tp10.Get('deepsc_tp1000_TprimeToTZ_1000_2018')
h_signal_1000_tp10.SetLineColor(ROOT.kOrange+7)
h_signal_1000_tp10.Rebin(100)
S_score_1000 = h_signal_1000_tp10.Integral(h_signal_1000_tp10.FindBin(th_5_1000), 1000)
h_signal_1800_tp10 = rfile_tp10.Get('deepsc_tp1800_TprimeToTZ_1000_2018')
h_signal_1800_tp10.SetLineColor(ROOT.kOrange+7)
h_signal_1800_tp10.Rebin(100)
h_signal_MET_tp10 = rfile_tp10.Get('MET_TprimeToTZ_1000_2018')
h_signal_MET_tp10.SetLineColor(ROOT.kOrange+7)
S_1000 = h_signal_MET_tp10.Integral(3,20)
h_signal_MET_tp10.Rebin(2)

root_filename_tp18 = crabout['meta_info']['eos_stkr']  + "TprimeToTZ_1800_2018.root"
rfile_tp18 = ROOT.TFile(root_filename_tp18)
h_signal_700_tp18 = rfile_tp18.Get('deepsc_tp700_TprimeToTZ_1800_2018')
h_signal_700_tp18.SetLineColor(ROOT.kGreen+2)
h_signal_700_tp18.Rebin(100)
h_signal_1000_tp18 = rfile_tp18.Get('deepsc_tp1000_TprimeToTZ_1800_2018')
h_signal_1000_tp18.SetLineColor(ROOT.kGreen+2)
h_signal_1000_tp18.Rebin(100)
h_signal_1800_tp18 = rfile_tp18.Get('deepsc_tp1800_TprimeToTZ_1800_2018')
h_signal_1800_tp18.SetLineColor(ROOT.kGreen+2)
h_signal_1800_tp18.Rebin(100)
S_score_1800 = h_signal_1800_tp18.Integral(h_signal_1800_tp18.FindBin(th_5_1800), 1000)
h_signal_MET_tp18 = rfile_tp18.Get('MET_TprimeToTZ_1800_2018')
h_signal_MET_tp18.SetLineColor(ROOT.kGreen+2)
S_1800 = h_signal_MET_tp18.Integral(5,20)
h_signal_MET_tp18.Rebin(2)


leg = ROOT.TLegend(0.45,0.85,0.8,0.7)          
leg.SetBorderSize(0)
leg.AddEntry(qcd_h_list[0], "QCD","f")
leg.AddEntry(tt_h_list[0], "$t\\bar t$ ","f")
leg.AddEntry(zjtnn_h_list[0], "$Z+Jets \\rightarrow \\nu \\nu$","f")

leg.AddEntry(h_signal_700_tp7, "Tprime 700","l")
leg.AddEntry(h_signal_700_tp10, "Tprime 1000","l")
leg.AddEntry(h_signal_700_tp18, "Tprime 1800","l")

leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)
leg.SetNColumns(2)


hs_ds700.SetTitle("")
maximum = hs_ds700.GetMaximum()
hs_ds700.SetMaximum(maximum*10)
hs_ds700.SetMinimum(0.001)
hs_ds700.Draw('hist')
hs_ds700.GetXaxis().SetTitle("700 GeV Hypothesis DNN score")
hs_ds700.GetYaxis().SetTitle("Events")
hs_ds700.GetXaxis().SetTitleFont(42)
hs_ds700.GetYaxis().SetTitleFont(42)
hs_ds700.GetXaxis().SetTitleSize(0.045)
hs_ds700.GetYaxis().SetTitleSize(0.045)
c0.SetLogy()
leg.Draw()
h_signal_700_tp7.Draw('SAME PE')
h_signal_700_tp10.Draw('SAME PE')
h_signal_700_tp18.Draw('SAME PE')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "V1_700_stackplot.png")
c0.Clear()


hs_ds1000.SetTitle("")
maximum = hs_ds1000.GetMaximum()
hs_ds1000.SetMaximum(maximum*10)
hs_ds1000.SetMinimum(0.001)
hs_ds1000.Draw('hist')
hs_ds1000.GetXaxis().SetTitle("1000 GeV Hypothesis DNN score")
hs_ds1000.GetYaxis().SetTitle("Events")
hs_ds1000.GetXaxis().SetTitleFont(42)
hs_ds1000.GetYaxis().SetTitleFont(42)
hs_ds1000.GetXaxis().SetTitleSize(0.045)
hs_ds1000.GetYaxis().SetTitleSize(0.045)
c0.SetLogy()
leg.Draw()
h_signal_1000_tp7.Draw('SAME PE')
h_signal_1000_tp10.Draw('SAME PE')
h_signal_1000_tp18.Draw('SAME PE')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "V1_1000stackplot.png")
c0.Clear()



hs_ds1800.SetTitle("")
maximum = hs_ds1800.GetMaximum()
hs_ds1800.SetMaximum(maximum*10)
hs_ds1800.SetMinimum(0.001)
hs_ds1800.Draw('hist')
hs_ds1800.GetXaxis().SetTitle("1800 GeV Hypothesis DNN score")
hs_ds1800.GetYaxis().SetTitle("Events")
hs_ds1800.GetXaxis().SetTitleFont(42)
hs_ds1800.GetYaxis().SetTitleFont(42)
hs_ds1800.GetXaxis().SetTitleSize(0.045)
hs_ds1800.GetYaxis().SetTitleSize(0.045)
c0.SetLogy()
hs_ds1800.Draw('hist')
leg.Draw()
h_signal_1800_tp7.Draw('SAME PE')
h_signal_1800_tp10.Draw('SAME PE')
h_signal_1800_tp18.Draw('SAME PE')
c0.SaveAs(crabout['meta_info']['eos_stk'] + "V1_1800stackplot.png")
c0.Clear()

hs_met.SetTitle("")
maximum = hs_met.GetMaximum()
hs_met.SetMaximum(maximum*10)
hs_met.SetMinimum(0.001)
hs_met.Draw('hist')
hs_met.GetXaxis().SetTitle("MET p_{T} (GeV)")
hs_met.GetYaxis().SetTitle("Events")
hs_met.GetXaxis().SetTitleFont(42)
hs_met.GetYaxis().SetTitleFont(42)
hs_met.GetXaxis().SetTitleSize(0.045)
hs_met.GetYaxis().SetTitleSize(0.045)
hs_met.GetXaxis().SetRangeUser(200,1000)
c0.SetLogy()
hs_met.Draw('hist')
h_signal_MET_tp7.Draw('SAME PE')
h_signal_MET_tp10.Draw('SAME PE')
h_signal_MET_tp18.Draw('SAME PE')
leg.Draw()
c0.SaveAs(crabout['meta_info']['eos_stk'] + "V1_MET_stackplot.png")
c0.Clear()

print("\n\nInizio il calcolo delle tre significance...")
Z_700 = S_700/np.sqrt(metcount_bg_th700)
Z_1000 = S_1000/np.sqrt(metcount_bg_th1000)
Z_1800 = S_1800/np.sqrt(metcount_bg_th1800)
print("Z per soglia 700: " + str(Z_700))
print("Z per soglia 1000: " + str(Z_1000))
print("Z per soglia 1800: " + str(Z_1800))
Z_score_1800 = S_score_1800/np.sqrt(score1800_bg_counter)
Z_score_1000 = S_score_1000/np.sqrt(score1000_bg_counter)
Z_score_700 = S_score_700/np.sqrt(score700_bg_counter)
print("\n\nZ per soglia score 700: " + str(Z_score_700))
print("Z per soglia score 1000: " + str(Z_score_1000))
print("Z per soglia score 1800: " + str(Z_score_1800))