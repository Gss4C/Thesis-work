#!/usr/bin/bash 
cd /afs/cern.ch/user/j/jbonetti/CMSSW_12_4_7/src/PhysicsTools/NanoAODTools/python/postprocessing/Thesis/NeuralNetwork/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 data_making.py -c $1