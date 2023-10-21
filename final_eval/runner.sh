#!/usr/bin/bash 
cd /afs/cern.ch/user/j/jbonetti/CMSSW_12_4_7/src/PhysicsTools/NanoAODTools/python/postprocessing/Thesis/final_eval/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 stk_histo.py -d $1