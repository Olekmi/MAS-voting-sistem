import numpy as np

def sorting_dictionary(dict_uniques,outcome):
    for key in dict_uniques:
        if key in outcome:
            outcome[key] += dict_uniques[key]
        else:
            outcome[key] = dict_uniques[key]
    outcome = dict(sorted(outcome.items(), key=lambda outcome: outcome[1], reverse=True))
    return outcome

def handle_bullet_voting(outcome):
    try:
        if (list(outcome.items())[0][0].dtype == np.dtype('<U1')): # checking if it is of type numpy string
            del outcome['-1']
        else:
            del outcome[-1]
    except KeyError:
        False
    return outcome

def borda_calculate_outcome(preference_matrix):
    outcome = {}
    for j in range(preference_matrix.shape[0]):
        temp = []
        for i in range(preference_matrix.shape[1]):
            temp.append(preference_matrix[j][i])
        unique, counts = np.unique(temp, return_counts=True)
        dict_uniques = dict(zip(unique, counts))
        # print("dict",dict_uniques)

        for key in dict_uniques:
            dict_uniques[key] *=  (preference_matrix.shape[0] - 1 - j)
        outcome = sorting_dictionary(dict_uniques,outcome)
    #in case of bullet voting
    outcome = handle_bullet_voting(outcome)
    return outcome

def plurality_calculate_outcome(preference_matrix):
    outcome = {}
    k = 0
    for j in range(preference_matrix.shape[0]):
        if j > 0:
            k = 1
        temp = []
        for i in range(preference_matrix.shape[1]):
            temp.append(preference_matrix[j][i])
        unique, counts = np.unique(temp, return_counts=True)
        dict_uniques = dict(zip(unique, counts))
        for key in dict_uniques:
            dict_uniques[key] *=  (preference_matrix.shape[0] + 1 - preference_matrix.shape[0] - k)#we give weights only to top preference
        outcome = sorting_dictionary(dict_uniques,outcome)
    #in case of bullet voting
    outcome = handle_bullet_voting(outcome)
    return outcome

def voting_for_two_calculate_outcome(preference_matrix):
    outcome = {}
    k = 0
    for j in range(preference_matrix.shape[0]):
        if j > 1:
            k = 1
        temp = []
        for i in range(preference_matrix.shape[1]):
            temp.append(preference_matrix[j][i])
        unique, counts = np.unique(temp, return_counts=True)
        dict_uniques = dict(zip(unique, counts))
        for key in dict_uniques:
            dict_uniques[key] *=  (preference_matrix.shape[0] + 1 - preference_matrix.shape[0] - k)#we give weights only to 2 top preferences
        outcome = sorting_dictionary(dict_uniques,outcome)
    #in case of bullet voting
    outcome = handle_bullet_voting(outcome)
    return outcome

def antiplurality_calculate_outcome(preference_matrix):
    outcome = {}
    k = 0
    for j in range(preference_matrix.shape[0]):
        if j > preference_matrix.shape[0]-2:
            k = 1
        temp = []
        for i in range(preference_matrix.shape[1]):
            temp.append(preference_matrix[j][i])
        unique, counts = np.unique(temp, return_counts=True)
        dict_uniques = dict(zip(unique, counts))
        for key in dict_uniques:
            dict_uniques[key] *=  (preference_matrix.shape[0] + 1 - preference_matrix.shape[0] - k)#we give weights only to 2 top preferences
        outcome = sorting_dictionary(dict_uniques,outcome)
    #in case of bullet voting
    outcome = handle_bullet_voting(outcome)
    return outcome