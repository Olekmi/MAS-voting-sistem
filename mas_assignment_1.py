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
    print(outcome)
    return outcome

def happiness_score(outcome,preference_matrix):
    
    for i in range(preference_matrix.shape[1]):
        distance = []
        for j in range(preference_matrix.shape[0]):
            distance.append(preference_matrix.shape[1]-list(outcome.keys()).index(preference_matrix[j][i]) - preference_matrix.shape[1]-i) #rank of the outcome - 
            rank_outcome = list(outcome.keys()).index(preference_matrix[j][i])
            prefer_rank = preference_matrix.shape[1]
        
        print(distance)
            # weights = 
    
preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
print(preference_matrix)
calculate_outcome(preference_matrix)
happiness_score(calculate_outcome(preference_matrix),preference_matrix)

