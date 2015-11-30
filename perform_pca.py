#!/usr/bin/env python

    ##------------------------------------------------------------------------------##
    #   The generated encodings can be pretty big. Both in size and number           #
    #   of elements.                                                                 #   
    #   It can lead to memory usage issue in one case, overfitting in the other.     #
    #   One way to deal with it is to perform PCA to reduce the number of elements   #
    #   for each example.                                                            #   
    ##------------------------------------------------------------------------------##

import argparse
import numpy as np
import cPickle
import re
from sklearn.decomposition import PCA


def open_encodings_pkl(pklFile):

    ##------------------------------------------------------------------------------##
    #               Open and load encodings contained in pkl files.                  #
    ##------------------------------------------------------------------------------##
    
    print "\t----> Loading encodings..."
    encoding  = cPickle.load(open(pklFile, "rb"))
    print "\t\tL----> Done."
    
    return encoding

def build_encoding_matrix(encodingDict):
    
    ##------------------------------------------------------------------------------##
    #               Transform this dict into a matrix. Necessary if                  #
    #               you want to perform PCA.                                         # 
    #               Nb of examples X Nb elements per encodings.                      #
    #               We build and keep a key list to be able to go back               # 
    #               from matrix to dictionnary in the end.                           #
    ##------------------------------------------------------------------------------##
    
    print "\t----> Building the matrix..."
    nbDVS = 0
    width =  len(encodingDict[encodingDict.keys()[0]][0])
    encArray = np.zeros((len(encodingDict),width))
    print "\t\tL----> Number of elements (before PCA): ", width 
    keys_list = []

    for keys in encodingDict:
        keys_list.append(keys)
        for i in range(len(encodingDict[keys][0])):
            encArray[nbDVS,i] = encodingDict[keys][-1][i]
        nbDVS += 1
    
    print "\t\tL----> Done."
    return encArray, keys_list

def rebuild_dict(enc_matrix, key_list):
    
    ##------------------------------------------------------------------------------##
    #               Rebuild a dictionnary from the matrix obtained                   # 
    #               after PCA.                                                       #
    ##------------------------------------------------------------------------------##
    
    print "\t----> Rebuilding dictionnary from matrix..."
    rebuiltDict = {}
    
    for idx in range(enc_matrix.shape[0]):
        rebuiltDict[key_list[idx]] = enc_matrix[idx,:]
    
    print "\t\tL----> Done."
    return rebuiltDict

def save_dict(dict_to_save, dict_name):
    
    ##------------------------------------------------------------------------------##
    #               Save  dictionnary to a pkl file.                                 # 
    #               To be used later as features.                                    #
    ##------------------------------------------------------------------------------##
    
    print "\t----> Saving to pkl file..." 
   
    output_name = dict_name + ".pkl" 
    cPickle.dump(dict_to_save, open(output_name, "wb")) 
    
    print "\t\tL----> Done."

def perform_pca(encoding_matrix, nbComp):
    
    ##------------------------------------------------------------------------------##
    #               Perform PCA on the original matrix.                              # 
    #               Returns another matrix.                                          #
    ##------------------------------------------------------------------------------##
    
    print "\t----> Starting performing pca..."
    pca = PCA(n_components = nbComp)
    enc_pca = pca.fit_transform(encoding_matrix)
    print  "\t\tL----> Done."
    return enc_pca

def standard_PCA(path_to_pkl, nb_elements, output_name):

    ##------------------------------------------------------------------------------##
    #               Function is refered as standard because it basically             # 
    #               is the default case.                                             # 
    #               The data fit in memory, so we open and load the full             # 
    #               dataset as a normal pkl file.                                    #  
    #               Then, we perform a normal PCA on the whole matrix at once.       #
    ##------------------------------------------------------------------------------##
    
    print "----> Perform standard PCA on ", path_to_pkl
    print "----> Nb of components after PCA: ", nb_elements

    encDict             = open_encodings_pkl(path_to_pkl)
    encMatrix, key_list = build_encoding_matrix(encDict)
    resultMatrix        = perform_pca(encMatrix, nb_elements)
    rebuiltDict         = rebuild_dict(resultMatrix, key_list)
    
    save_dict(rebuiltDict,output_name)
    print  "----> All done."

def main():
    
    args = parse_args()
   
    if args.standard:
        standard_PCA(args.path, args.components, args.output_name)
    

def parse_args():
    
    parser = argparse.ArgumentParser("Perform PCA on a set of encodings.")
    
    parser.add_argument("--path",         type = str, help="Path to the encodings. (pkl files).")
    parser.add_argument("--output_name",  type = str, help="Name of the output file.")
    
    parser.add_argument("--standard",     action = "store_true",      help="Perform standard PCA on one matrix from one file and returns one file.")
    parser.add_argument("--incremental",  action = "store_true",      help="Perform incremental PCA on chunks of data. Use it if the data is to big fit in memory.")
    
    parser.add_argument("--components",   type = int, default = 2000, help="Numbers of elements in you encoding after the PCA.")
    
    return parser.parse_args()

if __name__ == "__main__":

    main()
    
    #print result
    #print np.shape(encMatrix)
    #print np.shape(result)
