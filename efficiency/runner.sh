#!/usr/bin/bash 
cd /afs/cern.ch/user/j/jbonetti/CMSSW_12_4_7/src/PhysicsTools/NanoAODTools/python/postprocessing/Thesis/efficiency/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 histograms.py -t 1 -c $1