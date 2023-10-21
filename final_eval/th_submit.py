import os
import optparse
import sys
import time
#from samples.samples import *
#from get_file_fromdas import *

usage = 'python submit_condor.py -d dataset_name -f destination_folder'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('-f', '--folder', dest='folder', type=str, default = '', help='Please enter a destination folder')
#parser.add_option('-u', '--user', dest='us', type='string', default = 'ade', help="")
(opt, args) = parser.parse_args()
#Insert here your uid... you can see it typing echo $uid

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
if username == 'adeiorio':
    uid = 103214
elif username == 'acagnott':
    uid = 140541
elif username == 'jbonetti':
    uid = 159585

def sub_writer(cluster):
    f = open("th_condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write("+JobFlavour             = \"longlunch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek = 1 week
    f.write("executable              = runner.sh\n")
    f.write("arguments               = "+ cluster +"\n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = th_condor/output/"+cluster+".out\n")
    f.write("error                   = th_condor/error/" +cluster+".err\n")
    f.write("log                     = th_condor/log/"   +cluster+".log\n")

    f.write("queue\n")

if not os.path.exists("th_condor/output"):
    os.makedirs("th_condor/output")
if not os.path.exists("th_condor/error"):
    os.makedirs("th_condor/error")
if not os.path.exists("th_condor/log"):
    os.makedirs("th_condor/log")
if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")
'''
datasets = ['tDM_mPhi1000_mChi1']#, 'QCD_HT1000','QCD-HT1500to2000_2018', 'QCD-HT2000toInf_2018', 
            #'TT_Mtt-700to1000_2018', 'TT_Mtt-1000toInf_2018', 'TT_SemiLep_2018', 'TT_Hadr_2018']
datasets= {
    #'tDM_mPhi1000_mChi1': '/eos/home-a/acagnott/DarkMatter/prepro/tDM_mPhi1000_mChi1.root',
    #'tDM_mPhi500_mChi1': '/eos/home-a/acagnott/DarkMatter/prepro/tDM_mPhi500_mChi1.root',
    #'tDM_mPhi50_mChi1': '/eos/home-a/acagnott/DarkMatter/prepro/tDM_mPhi50_mChi1.root',
    'QCD_HT200to300_2018': 'root://cms-xrd-global.cern.ch///store/mc/RunIIAutumn18NanoAODv7/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/130000/5096FFDA-A47E-1846-AE02-033E0F144FF6.root',
    #'QCD_HT300to500_2018': 'root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/120000/41889A83-F0A0-2143-AFB2-8041D63D3141.root',
    #'QCD_HT500to700_2018': 'root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/100000/D2F139EF-CB80-404D-955F-B8D8E682D682.root',
    'QCD_HT700to1000_2018': 'root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/260000/EE305C43-E265-BB4A-B6FA-60B447464524.root',
}
'''
#datasets = QCD_2018.components+TT_2018.components+ZJetsToNuNu_2018.components+[TprimeToTZ_700_2018, TprimeToTZ_1000_2018, TprimeToTZ_1800_2018]
#datasets = [ZJetsToNuNu_HT800to1200_2018]

cluster_list = [
    "ZJTNN_1",
    "ZJTNN_2",
    "ZJTNN_3",
    "ZJTNN_4",
    "ZJTNN_5",
    "ZJTNN_6",
    "ZJTNN_7",
    "TT_1",
    "TT_2",
    "TT_3",
    "TT_4",
    "QCD_1",
    "QCD_2",
    "QCD_3",
    "QCD_4",
    "QCD_5",
    "QCD_6",
    "TP_1800",
    "TP_1000",
    "TP_700"
    ]
'''
cluster_list = [
    "ZJTNN_1",
    "ZJTNN_2",
    ]
'''
for cluster in cluster_list:
    sub_writer(cluster)
    os.popen('condor_submit th_condor.sub')
    print("SUBMITTED")
    time.sleep(5)