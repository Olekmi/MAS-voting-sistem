import numpy as np

number_of_preferences = 3
number_of_voters = 4

min_number_preference = 0
max_number_preference = 10

def gen_random_preference_matrix(number_of_preferences,number_of_voters):
    preference_matrix = np.random.randint(low=min_number_preference,high=max_number_preference,size=(number_of_preferences,number_of_voters) )
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
    print(outcome)


preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
print(preference_matrix)
calculate_outcome(preference_matrix)

