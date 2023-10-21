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
    f = open("stk_condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write("+JobFlavour             = \"workday\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek = 1 week
    f.write("executable              = runner.sh\n")
    f.write("arguments               = "+ cluster +"\n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = stk_condor/output/"+'histo'+ cluster+".out\n")
    f.write("error                   = stk_condor/error/" +'histo'+ cluster+".err\n")
    f.write("log                     = stk_condor/log/"   +'histo'+ cluster+".log\n")

    f.write("queue\n")

if not os.path.exists("stk_condor/output"):
    os.makedirs("stk_condor/output")
if not os.path.exists("stk_condor/error"):
    os.makedirs("stk_condor/error")
if not os.path.exists("stk_condor/log"):
    os.makedirs("stk_condor/log")
if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

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
    "ZJTNN_6"
    ]
'''

for cluster in cluster_list:
    sub_writer(cluster)
    os.popen('condor_submit stk_condor.sub')
    print("SUBMITTED")
    time.sleep(5)
