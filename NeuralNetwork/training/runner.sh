#!/usr/bin/bash 
cd /afs/cern.ch/user/j/jbonetti/CMSSW_12_4_7/src/PhysicsTools/NanoAODTools/python/postprocessing/Thesis/NeuralNetwork/training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 DNN_train.py -s $1