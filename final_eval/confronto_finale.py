import ROOT
import json

def json_reader(nome_file):
    with open(nome_file, "r") as file:
        contenuto = file.read()
        dizionario = json.loads(contenuto)
        return dizionario

def calcola_efficienze_segnale(histogram, signal):
    if signal == 700:
        th_1 = 0.54
        th_5 = 0.35
        th_10 = 0.28
    elif signal == 1000:
        th_1 = 0.73
        th_5 = 0.41
        th_10 = 0.26
    elif signal == 1800:
        th_1 = 0.68
        th_5 = 0.33
        th_10 = 0.14

    integral = histogram.Integral()
    right_1  = histogram.Integral(histogram.FindBin(th_1), 1000)
    right_5  = histogram.Integral(histogram.FindBin(th_5), 1000)
    right_10 = histogram.Integral(histogram.FindBin(th_10), 1000)
    epsilon_1 = right_1/integral
    epsilon_5 = right_5/integral
    epsilon_10 = right_10/integral
    return epsilon_1, epsilon_5, epsilon_10

def threshold_F_seeker(histogram, efficiency = 0.1):
    
    epsilon = 0.0001
    th_bin  = 0
    full_integral = histogram.Integral()
    if full_integral < 1e-10: #se histo vuoto deve fermarsi
        print("Warning: Full integral is very close to zero. Cannot evalutate this threshold")
        return th_bin, epsilon
    else:        
        bin_idx = 0
        while epsilon < efficiency and epsilon > 0:
            bin_idx += 1
            right_integral = histogram.Integral(1000 - bin_idx, 1000)
            
            if right_integral > 1e-10 and full_integral > 1e-10:
                if full_integral != 0:
                    epsilon = right_integral/full_integral
                else:
                    epsilon = 0

        th_bin = 1000 - bin_idx
        if epsilon == 0:
            print('^^^    FAIL    ^^^')
        else:
            print("^^^    SUCCESS   ^^^")
        
        return th_bin, epsilon

#variabili che mi servono

crabout = json_reader("crabout_files.json")

filename_700  = crabout['meta_info']['eos_stkr']+"TprimeToTZ_700_2018.root" 
filename_1000 = crabout['meta_info']['eos_stkr']+"TprimeToTZ_1000_2018.root"
filename_1800 = crabout['meta_info']['eos_stkr']+"TprimeToTZ_1800_2018.root"

rfile_700 = ROOT.TFile(filename_700)
h_tp700_score700 = rfile_700.Get('deepsc_tp700_TprimeToTZ_700_2018')
signal_700_epsilon_1, signal_700_epsilon_5, signal_700_epsilon_10 = calcola_efficienze_segnale(h_tp700_score700, 700)

rfile_1000 = ROOT.TFile(filename_1000)
h_tp1000_score1000 = rfile_1000.Get('deepsc_tp1000_TprimeToTZ_1000_2018')
signal_1000_epsilon_1, signal_1000_epsilon_5, signal_1000_epsilon_10 = calcola_efficienze_segnale(h_tp1000_score1000, 1000)

rfile_1800 = ROOT.TFile(filename_1800)
h_tp1800_score1800 = rfile_1800.Get('deepsc_tp1800_TprimeToTZ_1800_2018')
signal_1800_epsilon_1, signal_1800_epsilon_5, signal_1800_epsilon_10 = calcola_efficienze_segnale(h_tp1800_score1800, 1800)

print("Efficienze di segnale con le thresholds trovate:")
print("Segnale 700 GeV - 1,5,10%: "  + str(signal_700_epsilon_1)  + " --- "+str(signal_700_epsilon_5) +" --- "+str(signal_700_epsilon_10))
print("Segnale 1000 GeV - 1,5,10%: " + str(signal_1000_epsilon_1) + " --- "+str(signal_1000_epsilon_5) +" --- "+str(signal_1000_epsilon_10))
print("Segnale 1800 GeV - 1,5,10%: " + str(signal_1800_epsilon_1) + " --- "+str(signal_1800_epsilon_5) +" --- "+str(signal_1800_epsilon_10))

print("\nCalcolo del taglio equivalente in MET")
h_tp700_MET = rfile_700.Get('MET_TprimeToTZ_700_2018')
h_tp1000_MET = rfile_1000.Get('MET_TprimeToTZ_1000_2018')
h_tp1800_MET = rfile_1800.Get('MET_TprimeToTZ_1800_2018')

met_th_700 = threshold_F_seeker(h_tp700_MET, signal_700_epsilon_5)
met_th_1000 = threshold_F_seeker(h_tp1000_MET, signal_1000_epsilon_5)
met_th_1800 = threshold_F_seeker(h_tp1800_MET, signal_1800_epsilon_5)

print("Bin risultanti dalla ricerca della threshold imponendo l'efficienza di segnale desiderata:")
print("Segnale 700: "  + str(met_th_700))
print("Segnale 1000: " + str(met_th_1000))
print("Segnale 1800: " + str(met_th_1800))