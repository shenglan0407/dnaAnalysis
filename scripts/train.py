#! /usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), '../src'))

import utilities
import dnaAnalysis as da

import ConfigParser
import getopt

import h5py

def usage():
    print './train.py -i <config_file> -o <output_file> -v -h'
    print '-i configuration file name'
    print '-o output file name'
    print '-v verbose'
    print '-o allow overwriting previous output'
    print '-h print this message'
    
def main(argv):
    verbose = False
    config_file = None
    output_file = "model.hdf5"
    overwrite = False
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))

    try:
        opts, args = getopt.getopt(argv,"hvwi:o:",["config_file=","output_file="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--config_file"):
            config_file = arg
        elif opt=='-v':
            verbose = True
        elif opt=='-w':
            overwrite=True
        elif opt in  ("-o", "--output_file"):
            output_file = arg

    if config_file == None:
        utilities.printErrorMsg("Must provide config file to train.py")
        usage()
        sys.exit(2)
    else:
        config=ConfigParser.ConfigParser()
        config_path = os.path.join(fileDir, '../config/%s'%config_file)
        config.read(config_path)
        
        try:
            train_set = config.get('Data','train_set').split(',')
            outlier_cutoff = config.getfloat('Outliers','outlier_cutoff')
            num_bins =config.getint('Outliers','num_bins')
            psi_skip = config.getint('Outliers','psi_skip')
        except ConfigParser.NoSectionError:
            utilities.printErrorMsg("Config file config/%s either doesn't exist or contains errors. "%config_file)
            sys.exit(2)

        if verbose:
            print("Read configurations from config/%s"%config_file)
            print("Using the following data files for training:")
            
            for this_file in train_set:
                print this_file
            print "\n"
            print("Outlier cutoff will be %.2f sigmas"%outlier_cutoff)
            print("Total number of bins used in creating histograms will be %d"%num_bins)
            print("The first %d psi values will be skipped"%psi_skip)
            print "\n"
            
    output_path = os.path.join(fileDir, '../models/%s'%output_file)
    
    
    while(os.path.isfile(output_path)):
        if overwrite:
            utilities.printWarningMsg("Overwriting existing model models/%s"%output_file)
            break
        else:
            utilities.printWarningMsg("Output file models/s% already exist. Will not overwrite")
            print "Enter new file name: "
            output_file = raw_input()
            output_path = os.path.join(fileDir, '../models/%s'%output_file)
    
    # train model using train_set
    model = []
    for this_file in train_set:
        data_file = h5py.File(this_file,'r')
        
        for i in range(data_file['dif_cors'].shape[1])[psi_skip:]:
            data = data_file['dif_cors'][:,i]
            coefs = da.train(data,outlier_cutoff,num_bins)
            model.append(coefs)
        
        data_file.close()
    
    output = h5py.File(output_path,'w')
    output.create_dataset('dists',data=model)
    output.create_dataset('train_set',data=train_set)
    output.create_dataset('config',data=[config_path])
    
    output.close()
    
        
        
    
if __name__ == "__main__":
   main(sys.argv[1:])