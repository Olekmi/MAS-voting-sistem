# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 21:35:16 2019

@author: Smail
"""
import numpy as np


def translate_index_matrix(matrix):
    indexes = []
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            if (i == matrix.shape[1] - 1):
                indexes.append(matrix.shape[0] - j)
    indexes_numpy = np.asarray(indexes,dtype=np.int32)
    indexes_numpy = np.reshape(indexes_numpy,(matrix.shape[0],1))
    return indexes_numpy


def translate_index_dictionary(preference_matrix,outcome_dictionary):
    indexes= np.ones((preference_matrix.shape[0],preference_matrix.shape[1]), dtype=np.int32)
    for i in range(preference_matrix.shape[1]):
        for j in range(preference_matrix.shape[0]):
            indexes[j][i] = len(outcome_dictionary) - list(outcome_dictionary.keys()).index(preference_matrix[j][i])
    return indexes