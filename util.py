# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 21:35:16 2019

@author: Smail
"""
import numpy as np
import os.path as op
import pandas as pd

def matrix_to_string(matrix):
    for j in range(matrix.shape[0]):
        matrix_ascii = []
        for i in range(matrix.shape[1]):
            matrix_ascii.append(chr(ord('@')+matrix[j][i]+1))
        if j == 0:
            matrix_string = matrix_ascii
        else:
            matrix_string = np.vstack((matrix_string,matrix_ascii))
    return matrix_string

def return_pref_matrix_from_file(file_name):
    assert op.isfile(file_name),"the file specified does not exists, please use another file"
    splitted_file_name = file_name.split(".")
    assert splitted_file_name[1] == "txt", "the file specified is not a text file, please use a text file instead"
    data = pd.read_csv(file_name, header = None)
    assert data.isnull().values.any() == False, "it seems the file is not comma separated, please use a csv instead"
    return data.to_numpy()
    
def number_to_ascii(keys):
  keys_ascii = []
  for i in range(len(keys)):
    keys_ascii.append(chr(ord('@')+keys[i]+1))
  return keys_ascii
  
def join_strings_for_graph(keys,keys_ascii,values):
  text = []    
  for i in range(len(keys)):
    text.append(str(keys_ascii[i]) + ": " + str(values[i]))
  return text