import os
import sys
import uproot
import random
import vector
import argparse
import keras
import tensorflow.keras
import mplhep as hep
hep.style.use(hep.style.CMS)
import numpy as np
import pandas as pd
import pickle as pkl
import awkward as ak
import tensorflow as tf
import matplotlib.pyplot as plt
from math import sqrt
from tqdm import tqdm
from keras import backend as K
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, confusion_matrix, auc, roc_curve
from tensorflow.keras.layers import Dense, Dropout, LSTM, concatenate, GRU,Masking, Activation, TimeDistributed, Conv1D, BatchNormalization, MaxPooling1D, Reshape, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier #Non usata
from tensorflow.keras.callbacks import EarlyStopping #Non usata
from tensorflow.keras.utils import plot_model, to_categorical #Non usata
from tensorflow.keras.backend import sigmoid #Non usata
from tensorflow.keras import regularizers #Non usata
from keras.utils.generic_utils import get_custom_objects #Non usata
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.Thesis.NeuralNetwork.training.dnn_utils import *

parser = argparse.ArgumentParser(description = "Training DNN to a signal and background")
parser.add_argument("-s", "--signal",
                    type     = str,
                    help     = "Signal you want to train to: TP_700, TP_1000, TP_1800",
                    required = True)
options = parser.parse_args()

os.environ['PYTHONHASHSEED']=str(seed_value)
random.seed(seed_value)
np.random.seed(seed_value)
tf.random.set_seed(seed_value)
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
K.set_session(sess)

dnn_name         = 'DNN_' + 'noregions_' + 'bil_V2'+ options.signal
#model_folder     = './DNNmodel/' + dnn_name + '/'
model_folder_eos = eos_path_dnn + dnn_name + "/" 
#if not os.path.exists(model_folder):
 #   os.mkdir(model_folder)
if not os.path.exists(model_folder_eos):
    os.mkdir(model_folder_eos)

###########################################
#    SCALING FACTOR E DATA ACQUISITION    #
###########################################
## ATTENZIONE MANCANO zjtnn1,2,3 ##
###################################
bg_datasets = ["ZJTNN_3","ZJTNN_4","ZJTNN_5","ZJTNN_6","ZJTNN_7","TT_1","TT_2","TT_3","TT_4","QCD_1","QCD_2","QCD_3","QCD_4","QCD_5","QCD_6"]
if options.signal == 'TP_1800':
    datasets = ["TP_1800","ZJTNN_3","ZJTNN_4","ZJTNN_5","ZJTNN_6","ZJTNN_7","TT_1","TT_2","TT_3","TT_4","QCD_1","QCD_2","QCD_3","QCD_4","QCD_5","QCD_6"]
if options.signal == 'TP_1000':
    datasets = ["TP_1000","ZJTNN_3","ZJTNN_4","ZJTNN_5","ZJTNN_6","ZJTNN_7","TT_1","TT_2","TT_3","TT_4","QCD_1","QCD_2","QCD_3","QCD_4","QCD_5","QCD_6"]
if options.signal == 'TP_700':
    datasets = ["TP_700","ZJTNN_3","ZJTNN_4","ZJTNN_5","ZJTNN_6","ZJTNN_7","TT_1","TT_2","TT_3","TT_4","QCD_1","QCD_2","QCD_3","QCD_4","QCD_5","QCD_6"]

dict_samples = {}
for i in datasets:
    with open(path_pkl + i + '.pkl', 'rb') as f:
        data = pkl.load(f)
        #print(data)
        dict_samples[i] = data['full'][i]

###############################
#    Normalizzazione fondi    #
###############################
for dataset in bg_datasets:
    sigma_dataset = sample_dict[dizionario_per_samples[dataset]].sigma
    k_dataset = sigma_dataset * luminosity/(dict_samples[dataset][5]) # sigma*L/N_MC
    dataset_N_events = int(k_dataset * len(dict_samples[dataset][0]))
    
    dict_samples[dataset][0] = dict_samples[dataset][0][:dataset_N_events]
    dict_samples[dataset][1] = dict_samples[dataset][1][:dataset_N_events] 
    dict_samples[dataset][2] = dict_samples[dataset][2][:dataset_N_events] 
    dict_samples[dataset][3] = dict_samples[dataset][3][:dataset_N_events]
    dict_samples[dataset][4] = dict_samples[dataset][4][:dataset_N_events] 

#TRAINING BALANCING
for dataset in bg_datasets:
    idx_list = [i for i, x in enumerate(dict_samples[dataset][1])]
    idx_todrop = random.sample(idx_list, int(len(idx_list)*(2/3)))
    dict_samples[dataset][0] = np.delete(dict_samples[dataset][0], idx_todrop, 0)
    dict_samples[dataset][1] = np.delete(dict_samples[dataset][1], idx_todrop, 0)
    dict_samples[dataset][2] = np.delete(dict_samples[dataset][2], idx_todrop, 0)
    dict_samples[dataset][3] = np.delete(dict_samples[dataset][3], idx_todrop, 0)
    dict_samples[dataset][4] = np.delete(dict_samples[dataset][4], idx_todrop, 0)


#correzione per errore dove tolgo la truth
##########################################
for d in datasets:
    for i in range(len(dict_samples[d][0])):
        dict_samples[d][0][i][8] = 0  #highpt
    for i in range(len(dict_samples[d][1])):
        dict_samples[d][1][i][7] = 0 #lowpt

##########################################
##########################################


X_high_top = np.concatenate([dict_samples[d][0] for d in datasets])
X_low_top  = np.concatenate([dict_samples[d][1] for d in datasets])
X_fwd_jet  = np.concatenate([dict_samples[d][2] for d in datasets])
X_met      = np.concatenate([dict_samples[d][3] for d in datasets])
y_signal   = np.concatenate([dict_samples[d][4] for d in datasets])
X_high_train, X_high_test, X_low_train, X_low_test, X_jet_train, X_jet_test, X_met_train, X_met_test, y_train, y_test = train_test_split(X_high_top, X_low_top, X_fwd_jet, X_met, y_signal, stratify=y_signal, shuffle = True, test_size=0.2)

#####################################
#    NEURAL NETWORK ARCHITECTURE    #
#####################################
hpt_inputs = tf.keras.Input(shape = (X_high_train.shape[1],),
                             name  = "Top_High_pt" ) #x
lpt_inputs = tf.keras.Input(shape = (X_low_train.shape[1],),
                             name  = "Top_Low_pt" )  #y
met_inputs = tf.keras.Input(shape = (X_met_train.shape[1],),
                             name  = "MET" )         #z
jet_inputs = tf.keras.Input(shape = (X_jet_train.shape[1],),
                             name  = "Jet" )         #w

x = BatchNormalization()(hpt_inputs)
x = Dense(1, 
          activation = 'tanh', 
          kernel_initializer = 'random_normal')(x)

y = BatchNormalization()(lpt_inputs)
y = Dense(1, 
          activation = 'tanh', 
          kernel_initializer = 'random_normal')(y)

z = BatchNormalization()(met_inputs)
z = Dense(1, 
          activation = 'tanh', 
          kernel_initializer = 'random_normal')(z)
w = BatchNormalization()(jet_inputs)
w = Dense(1,
          activation = 'tanh',
          kernel_initializer = 'random_normal')(w)

x = concatenate([x,y])
x = Dense(2, 
          activation = 'tanh',
          kernel_initializer = 'random_normal')(x)
x = concatenate([x,z])
x = Dense(2, 
          activation = 'tanh',
          kernel_initializer = 'random_normal')(x)

x = concatenate([x,w])
x = Dense(2,
          activation = 'tanh',
          kernel_initializer = 'random_normal')(x)

x = Dropout(dropout)(x)

outputs = Dense(1, activation = 'sigmoid')(x)
model   = tf.keras.Model(inputs = [hpt_inputs, 
                                 lpt_inputs, 
                                 jet_inputs, 
                                 met_inputs],
                       outputs = outputs)
trainer = tf.keras.optimizers.Adam(learning_rate=0.01)
loss    = tf.keras.losses.BinaryCrossentropy()
model.compile(optimizer=trainer, loss=loss, metrics=[tf.keras.metrics.AUC()])
'''
tf.keras.utils.plot_model(model,
                          to_file= model_folder + "model_architecture.png",
                          show_shapes=True,
                          show_dtype=False,
                          show_layer_names=True,
                          rankdir="TB",
                          expand_nested=True,
                          dpi=96,
                          layer_range=None)
'''
tf.keras.utils.plot_model(model,
                          to_file= model_folder_eos + "model_architecture.png",
                          show_shapes=True,
                          show_dtype=False,
                          show_layer_names=True,
                          rankdir="TB",
                          expand_nested=True,
                          dpi=96,
                          layer_range=None)
early_stop = keras.callbacks.EarlyStopping(monitor = 'val_loss',
                                           mode='min',# quantity that has to be monitored (to be minimized in this case)
                                           patience = 30, # Number of epochs with no improvement after which training will be stopped.
                                           min_delta = 1e-5,
                                           restore_best_weights = True) # update the model with the best-seen weights

#Reduce learning rate when a metric has stopped improving
reduce_LR = keras.callbacks.ReduceLROnPlateau(monitor = 'loss',
                                              mode='min',# quantity that has to be monitored
                                              min_delta=1e-5,
                                              factor = 0.1, # factor by which LR has to be reduced...
                                              patience = 10, #...after waiting this number of epochs with no improvements 
                                              #on monitored quantity
                                              min_lr= 1e-15 ) 
callback_list = [early_stop]

########################################
#    TRAINING AND EVALUTATION MODEL    #
########################################
history = model.fit({'Top_High_pt': X_high_train, 'Top_Low_pt': X_low_train, 'Jet': X_jet_train, 'MET': X_met_train}, 
                    y_train, 
                    callbacks = callback_list, 
                    validation_split = 0.15,
                    epochs = epochs, 
                    batch_size = batch_size,
                    verbose=1)

# summarize history for accuracy
fig, ax = plt.subplots(ncols=2, figsize=(25,10))
for var in history.history.keys():
    if ('loss' in var) and (not 'val' in var): ax[1].plot(history.history[var], label ='train')
    if 'val_loss' in var: ax[1].plot(history.history[var], label ='val')
    if ('auc' in var) and (not 'val' in var): ax[0].plot(history.history[var], label ='train')
    if 'val_auc' in var : ax[0].plot(history.history[var], label ='val')

ax[0].set_title('model accuracy')
ax[0].set_ylabel('auc')
ax[0].set_xlabel('epoch')
ax[0].legend()
# summarize history for loss
ax[1].set_title('model loss')
ax[1].set_ylabel('loss')
ax[1].set_xlabel('epoch')
ax[1].legend()
ax[1].set_yscale('Log')

#plt.savefig(model_folder + 'auc_loss.png')
plt.savefig(model_folder_eos + 'auc_loss.png')

# histogram descriminator
y_pred = model.predict({'Top_High_pt': X_high_test, 'Top_Low_pt': X_low_test, 'Jet': X_jet_test,'MET': X_met_test})
y_pred_train = model.predict({'Top_High_pt': X_high_train, 'Top_Low_pt': X_low_train, 'Jet': X_jet_train,'MET': X_met_train})
y_pred_train_bkg = y_pred_train[y_train==0]
y_pred_train_sgn = y_pred_train[y_train==1]
y_pred_bkg = y_pred[y_test==0]
y_pred_sgn = y_pred[y_test==1]

fig, ax = plt.subplots(figsize=(10,10))
bins_count_bkg = ax.hist(y_pred_train_bkg, alpha=0.5, color='blue', 
                         density=True, label='B (train)', range = [0,1], bins = bins)
bins_count_sgn = ax.hist(y_pred_train_sgn, alpha=0.5,color='red', 
                         density=True, label='S (train)', range = [0,1], bins = bins)
hist, bins = np.histogram(y_pred_bkg, range = [0,1], bins=bins, density=True)
scale = len(y_pred_bkg) / sum(hist)
err = np.sqrt(hist * scale) / scale
center = (bins[:-1] + bins[1:]) / 2
ax.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')
hist, bins = np.histogram(y_pred_sgn, range = [0,1], bins=bins, density=True)
scale = len(y_pred_sgn) / sum(hist)
err = np.sqrt(hist * scale) / scale
center = (bins[:-1] + bins[1:]) / 2
ax.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')
ax.set_xlabel('score')
ax.set_ylabel('arbitrary units')
ax.legend()
plt.yscale('Log')

#plt.savefig(model_folder+'traintestDiscrimination.png')
plt.savefig(model_folder_eos+'traintestDiscrimination.png')

from sklearn.metrics import roc_curve, roc_auc_score
y_score = y_pred.ravel()
y_true = y_test.ravel()
fpr, tpr, trs =roc_curve(y_true = y_true, y_score = y_score, pos_label=1)
fig, ax = plt.subplots()
ax.plot(fpr, tpr) 
ax.set_title('ROC')
ax.set_xlabel('False Positive Rate') 
ax.set_ylabel('True Positive Rate')

#plt.savefig(model_folder+'ROC.png')
plt.savefig(model_folder_eos+'ROC.png')

#model.save(model_folder + dnn_name + '.h5')
model.save(model_folder_eos + dnn_name + '.h5')