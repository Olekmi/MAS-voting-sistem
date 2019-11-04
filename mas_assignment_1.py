import numpy as np

number_of_preferences = 3
number_of_voters = 10

def gen_preference_matrix(number_of_preferences,number_of_voters):
    preference_matrix = np.arange(number_of_preferences)
    preference_matrix = np.repeat(preference_matrix,number_of_voters,axis=1)
    print(preference_matrix)
    return preference_matrix
outcome = {}
outcome['B'] = 10
print(outcome['B'])
gen_preference_matrix(number_of_preferences,number_of_voters)