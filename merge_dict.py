#!/usr/bin/env python

import cPickle
import argparse

def merge_dicts(dict_names_list): # *dict_args):

    print "----> Merging the dictionaries..."
    merged_dict = {}

    for dictionary in dict_names_list:
        merged_dict.update(dictionary)
    
    print "\tL----> Done."
    return merged_dict

#def merge_pickles(*pkl_args):
def merge_pickles(outputName, *pkl_args):
    
    idx = 0
    pkl_list = []
    
    print "----> Loading the pkl files..."
    for pickles in pkl_args:
        dict_name = str(pickles) + str(idx)
        dict_name = cPickle.load(open(pickles, "rb"))
        pkl_list.append(dict_name)
        idx += 1
    print "\tL----> Done."

    newDict = merge_dicts(pkl_list)

    print "----> Dumping the merged dict to pkl..."
    cPickle.dump(newDict, open(outputName + ".pkl", "wb"))
    print "\tL----> Done."

def main ():
    
    args = parse_args()
    
    merge_pickles(args.output_name, args.pkl_path1, args.pkl_path2)

def parse_args():
    
    parser = argparse.ArgumentParser("Merge pickle files containing the encodings.")
    
    parser.add_argument("--pkl_path1",   type = str, help="Path to the encoding pickle files.")
    parser.add_argument("--pkl_path2",   type = str, help="Path to the encoding pickle files.")
    parser.add_argument("--output_name", type = str, help="Name of the merged file.")

    return parser.parse_args()

if __name__ == "__main__":

    main()


