import numpy as np
import operator
import collections
import random

number_of_preferences = 3
number_of_voters = 4

def gen_random_preference_matrix(number_of_preferences,number_of_voters):
    preference_matrix = random.sample(range(number_of_preferences),number_of_preferences)
    for i in range(number_of_voters-1):
        preference_matrix = np.vstack([preference_matrix,random.sample(range(number_of_preferences),number_of_preferences)])
    return preference_matrix.T

def generate_fixed_pref_matrix(number_of_preferences,number_of_voters):
    preference_matrix = np.arange(number_of_preferences)
    preference_matrix = np.repeat([preference_matrix],number_of_voters,axis=0)
    return preference_matrix.T
    
def calculate_outcome(preference_matrix):
    outcome = {}
    for j in range(preference_matrix.shape[0]):
        temp = []
        for i in range(preference_matrix.shape[1]):
            temp.append(preference_matrix[j][i])
        unique, counts = np.unique(temp, return_counts=True)
        dict_uniques = dict(zip(unique, counts))
        
        for key in dict_uniques:
            dict_uniques[key] *=  (preference_matrix.shape[0] - 1 - j)
        for key in dict_uniques:
            if key in outcome:
                outcome[key] += dict_uniques[key]
            else:
                outcome[key] = dict_uniques[key]
    outcome = dict(sorted(outcome.items(), key=lambda outcome: outcome[1], reverse=True))      
    return outcome

def happiness_score(outcome_indexes,index_preference_matrix):
    #we subtract the # of rows of preference matrix from  the current index of 
    #the preference of the player to get the highest index as the 1st one 
    distances = np.ones((outcome_indexes.shape[0],outcome_indexes.shape[1]), dtype=np.int32)
    
    for i in range(outcome_indexes.shape[1]):#col by col      
        for j in range(outcome_indexes.shape[0]):
            distances[j][i] = outcome_indexes[j][i] - index_preference_matrix[j]

#    print("distances\n",distances)
    happiness_score = distances * index_preference_matrix
#    print("happiness\n",happiness_score)
    return happiness_score

            
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
    
    
    
  
    
    
preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
print(preference_matrix)
outcome = calculate_outcome(preference_matrix)
print(outcome)
#happiness_score(calculate_outcome(preference_matrix),preference_matrix)

test= np.array([[1,2,3],
                [4,5,6]])
#print(test.shape)
#print(translate_index_matrix(preference_matrix))
indexes_matrix = translate_index_matrix(preference_matrix)
indexes_dict = translate_index_dictionary(preference_matrix,outcome)
happiness_score(indexes_dict,indexes_matrix) 