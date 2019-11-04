import numpy as np

number_of_preferences = 3
number_of_voters = 10

def gen_preference_matrix(number_of_preferences,number_of_voters):
    preference_matrix = np.arange(number_of_preferences)
    preference_matrix = np.repeat([preference_matrix],number_of_voters,axis=0)
    print(preference_matrix.T)
    return preference_matrix.T
outcome = {}
outcome['B'] = 10
print(outcome['B'])

def calculate_outcome(preference_matrix):
    
    for j in range(len(preference_matrix)):
        for i in preference_matrix[j]:
            

gen_preference_matrix(number_of_preferences,number_of_voters)