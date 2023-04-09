class mini_sample:
    def __init__(self, sigma=1, name = 'FILE.root', path = 'path string'):
        '''Class for a costumized mini samples.py, for using more dataset in an optimized way \n
        sigma = cross section in pb \n
        name  = name of the file.root you want to use, with extension \n
        path  = path to the folder where the file is \n
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

########## Signals ##########
TprimeBToTZ_M_1000 = mini_sample(sigma= 0.01362, 
                                 name = 'TprimeBToTZ_M-1000.root', 
                                 path = group_path)
TprimeBToTZ_M_1100 = mini_sample(sigma= 0.00823,
                                 name = 'TprimeBToTZ_M-1100.root',
                                 path = group_path)
TprimeBToTZ_M_1300 = mini_sample(sigma= 0.00325,
                                 name = 'TprimeBToTZ_M-1300.root',
                                 path = group_path)

########## Backgrounds ##########
TT_Mtt_1000toInf = mini_sample(sigma = 21.3,
                               name  = 'TT_Mtt-1000toInf.root',
                               path  = group_path)
TT_Mtt_700to1000 = mini_sample(sigma = 80.5,
                               name  = 'TT_Mtt-700to1000.root',
                               path  = group_path)

ZJetsToNuNu_2500ToInf  = mini_sample(sigma = 0.007*0.88, 
                                     name  = 'ZJetsToNuNu_HT-2500ToInf.root',
                                     path  = group_path)
ZJetsToNuNu_1200To2500 = mini_sample(sigma = 0.29*0.88, 
                                     name  = 'ZJetsToNuNu_HT-1200To2500.root',
                                     path  = group_path)
ZJetsToNuNu_800To1200  = mini_sample(sigma = 1.18*1.14, 
                                     name  = 'ZJetsToNuNu_HT-800To1200.root',
                                     path  = group_path)
ZJetsToNuNu_600To800   = mini_sample(sigma = 2.56*1.04, 
                                     name  = 'ZJetsToNuNu_HT-600To800.root',
                                     path  = group_path)

########## Liste utili ##########
datasets_list = [TprimeBToTZ_M_1000,
                 TprimeBToTZ_M_1100,
                 TprimeBToTZ_M_1300,
                 TT_Mtt_1000toInf,
                 TT_Mtt_700to1000,
                 ZJetsToNuNu_2500ToInf,
                 ZJetsToNuNu_1200To2500,
                 ZJetsToNuNu_800To1200,
                 ZJetsToNuNu_600To800]