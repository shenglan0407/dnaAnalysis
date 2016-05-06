# maps label to attribute name and types
label_attr_map = {
    "train_set": ["train_set", string],
    "val_set:": [ "val_set", string],
    "outlier_cutoff:": [ "outlier_cutoff", float],
    "pca_components:": [ "pca_components", int]
}

import utilities

class Params(object):
    def __init__(self, input_file_name):
        with open(input_file_name, 'r') as input_file:
            for line in input_file:
                row = line.split(" ")
                if len(row>0):
                    label = row[0]
                    data = row[1:]  # rest of row is data list

                    attr = label_attr_map[label][0]
                    datatypes = label_attr_map[label][1:]
                    try:
                        values=[datatypes(this_point) for this_point in data]
                    except ValueError:
                        utilities.printErrorMsg("Type mismatch in input params: check %s in %s."%(attr input_file_name))
                    
                    self.__dict__[attr] = values if len(values) > 1 else values[0]
                
                else: continue


# test
params = Params('input.dat')
print 'params.train_set:', params.train_set
print 'params.val_set:', params.val_set
print 'params.outlier_cutoff:', params.outlier_cutoff
print 'params.pca_components:', params.pca_components