class mini_sample:
    def __init__(self, sigma=1, name = 'FILE.root', path = 'path string'):
        '''Class for a costumized mini samples.py, for using more dataset in an optimized way \n
        .sigma = cross section in pb \n
        .name  = name of the file.root you want to use, with extension \n
        .path  = path to the folder where the file is \n
        '''
        self.sigma = sigma
        self.name  = name
        self.path  = path

    def dammi_combo_string(self):
        namepath = self.name + self.path
        return namepath

## Metas
subgroup = 1 #folders 
#creare file config
eos = '/eos/user/j/jbonetti/datasets/'
if subgroup == 1: 
    group_path = '/eos/user/j/jbonetti/datasets/05_04_2023/'

################
#   Signals    #
################
TprimeBToTZ_M_600  = mini_sample(sigma= 0.13728,
                                 name = 'TprimeBToTZ_M_600.root',
                                 path = group_path)
TprimeBToTZ_M_1000 = mini_sample(sigma= 0.01362, 
                                 name = 'TprimeBToTZ_M_1000.root', 
                                 path = group_path)
TprimeBToTZ_M_1100 = mini_sample(sigma= 0.00823,
                                 name = 'TprimeBToTZ_M_1100.root',
                                 path = group_path)
TprimeBToTZ_M_1300 = mini_sample(sigma= 0.00325,
                                 name = 'TprimeBToTZ_M_1300.root',
                                 path = group_path)
TprimeBToTZ_M_1800 = mini_sample(sigma= 0.00044,
                                 name = 'TprimeBToTZ_M_1800',
                                 path =group_path)

####################
#   Backgrounds    #
####################
TT_Mtt_1000toInf = mini_sample(sigma = 21.3,
                               name  = 'TT_Mtt_1000toInf.root',
                               path  = group_path)
TT_Mtt_700to1000 = mini_sample(sigma = 80.5,
                               name  = 'TT_Mtt_700to1000.root',
                               path  = group_path)

ZJetsToNuNu_HT_2500ToInf  = mini_sample(sigma = 0.007*0.88, 
                                     name  = 'ZJetsToNuNu_HT_2500ToInf.root',
                                     path  = group_path)
ZJetsToNuNu_HT_1200To2500 = mini_sample(sigma = 0.29*0.88, 
                                     name  = 'ZJetsToNuNu_HT_1200To2500.root',
                                     path  = group_path)
ZJetsToNuNu_HT_800To1200  = mini_sample(sigma = 1.18*1.14, 
                                     name  = 'ZJetsToNuNu_HT_800To1200.root',
                                     path  = group_path)
ZJetsToNuNu_HT_600To800   = mini_sample(sigma = 2.56*1.04, 
                                     name  = 'ZJetsToNuNu_HT_600To800.root',
                                     path  = group_path)

##############
#   Liste    #
##############
full_range_signals_list = [TprimeBToTZ_M_1000,
                            TprimeBToTZ_M_1100,
                            TprimeBToTZ_M_1300,
                            TT_Mtt_1000toInf,
                            TT_Mtt_700to1000,
                            ZJetsToNuNu_HT_2500ToInf,
                            ZJetsToNuNu_HT_1200To2500,
                            ZJetsToNuNu_HT_800To1200,
                            ZJetsToNuNu_HT_600To800]

signal_only_list = [TprimeBToTZ_M_600,
                    TprimeBToTZ_M_1000,
                    TprimeBToTZ_M_1100,
                    TprimeBToTZ_M_1300,
                    TprimeBToTZ_M_1800]

signal_only_list_full = [TprimeBToTZ_M_600,
                         TprimeBToTZ_M_1000,
                         TprimeBToTZ_M_1100,
                         TprimeBToTZ_M_1300,
                         TprimeBToTZ_M_1800]