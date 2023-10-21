#big_tree = ROOT.TChain("Events")
#for file in files_del_dataset:
#TChain.Add(file)
#vedi anche qui https://github.com/CMSNAFW/nanoAOD-tools/blob/master/python/postprocessing/tree_skimmer.py#L27C17-L27C17
#o anche https://root-forum.cern.ch/t/add-files-to-a-chain/26045/7
import ROOT
file_list = [ #i due file hanno le seguenti out di GetEntries() rispettivamente - 5354 e 4726
    'root://cms-xrd-global.cern.ch//store/user/jbonetti/DM_Run3_v0/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TT_semilep_2018/230607_144331/0000/tree_hadd_17.root',
    'root://cms-xrd-global.cern.ch//store/user/jbonetti/DM_Run3_v0/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TT_semilep_2018/230607_144331/0000/tree_hadd_42.root'
]

chain = ROOT.TChain('Events')
#print(chain)
for infile in file_list: 
    print("Adding %s to the chain" %(infile))
    chain.Add(infile)
print("Number of events in chain " + str(chain.GetEntries()))  #effettivamente mi dà gli eventi totali
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries())) #mi piglia l'ultimo tree

for event in range(chain.GetEntries()):
    chain.GetEntry(event)
    if event%100 == 0:
        print(event)
print('fratm tropp bell ho stampato tutti gli eventi e infatti ultimo event is numero: '+ str(event))