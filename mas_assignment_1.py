import numpy as np
import operator
import collections
import random
import util

# import sys
# sys.stdout = open('stdout.txt', 'w') #to save in an external file

number_of_preferences = 5
number_of_voters = 8
voter = 8

def gen_random_preference_matrix(number_of_preferences,number_of_voters):
    preference_matrix = random.sample(range(number_of_preferences),number_of_preferences)
    for i in range(number_of_voters-1):
        preference_matrix = np.vstack([preference_matrix,random.sample(range(number_of_preferences),number_of_preferences)])
    return preference_matrix.T

def generate_fixed_pref_matrix(number_of_preferences,number_of_voters):
    preference_matrix = np.arange(number_of_preferences)
    preference_matrix = np.repeat([preference_matrix],number_of_voters,axis=0)
    return preference_matrix.T

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
        for key in dict_uniques:
            if key in outcome:
                outcome[key] += dict_uniques[key]
            else:
                outcome[key] = dict_uniques[key]
    outcome = dict(sorted(outcome.items(), key=lambda outcome: outcome[1], reverse=True))
    #in case of bullet voting
    try:
        del outcome[-1]
    except KeyError:
        False

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
        for key in dict_uniques:
            if key in outcome:
                outcome[key] += dict_uniques[key]
            else:
                outcome[key] = dict_uniques[key]
    outcome = dict(sorted(outcome.items(), key=lambda outcome: outcome[1], reverse=True))
    #in case of bullet voting
    try:
        del outcome[-1]
    except KeyError:
        False
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
        for key in dict_uniques:
            if key in outcome:
                outcome[key] += dict_uniques[key]
            else:
                outcome[key] = dict_uniques[key]
    outcome = dict(sorted(outcome.items(), key=lambda outcome: outcome[1], reverse=True))
    #in case of bullet voting
    try:
        del outcome[-1]
    except KeyError:
        False
    return outcome

def happiness_player(total_distance_players):
    happiness_player = 1/(1+np.abs(total_distance_players))
    return happiness_player

def calculate_happiness(preference_matrix, outcome):
    outcome = np.array([*outcome]) #list out of the dict keys
    prefs_size =preference_matrix.shape[0]
    distance_vector = []
    for prefs in preference_matrix.T:

        total_distance = 0
        for pos, pref in enumerate(prefs):
            if pref == -1: break # for bullet voting
            k = prefs_size - np.where(outcome == pref)[0][0] #current position (in the voting outcome) 
            w = prefs_size - pos # “desired” position (in the voter’s true preference list)
            total_distance += (k - w) * w #weighted distance

        distance_vector.append(total_distance)

    happiness_vector = happiness_player(distance_vector)
    return happiness_vector

def bullet_voting(preference_matrix, voter):
    bullet_pref_matrix = np.copy(preference_matrix)
    bullet_pref_matrix[1:, voter] = -1
    return bullet_pref_matrix



##-------------------------MAIN------------------------------------

preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
# preference_matrix = generate_fixed_pref_matrix(number_of_preferences,number_of_voters)
print(preference_matrix)

#HAPPINESS WITH HONEST VOTING
outcome = voting_for_two_calculate_outcome(preference_matrix)
print(outcome)
happiness_vector = calculate_happiness(preference_matrix, outcome)
print("HAPPINESS:\n", np.vstack(happiness_vector), "\n\n")

#HAPPINESS WITH BULLET VOTING
bullet_matrix = bullet_voting(preference_matrix, 0)
bullet_outcome = borda_calculate_outcome(bullet_matrix)
print(bullet_outcome)
happiness_vector_bullet = calculate_happiness(preference_matrix, bullet_outcome)
print("HAPPINESS BULLET:\n", np.vstack(happiness_vector_bullet), "\n\n")

def Compromising(happiness_scores, preference_matrix, voter):
    counter = 0
    vector_happiness = []
    new_happiness_score = []
    preference_matrix_A_acc = []
    if happiness_scores[voter-1] != 1:#because the index starts frm 0
        print("We will try to improve your happiness.")
        for j in range(preference_matrix.shape[0]):
            if j>0: #we do not change the top preference, only an alternative
                for g in range(preference_matrix.shape[0]-j-1):#we will iterate through options. 2nd will check everything, but 1st. 3rd, all, but 1st and 2nd, etc.
                    counter += 1
                    g = preference_matrix.shape[0] - g-1#inversing index
                    preference_matrix_A = preference_matrix
                    alternative_A = preference_matrix_A[j][voter-1]
                    preference_matrix_A[j][voter-1] = preference_matrix_A[g][voter-1]
                    preference_matrix_A[g][voter-1] = alternative_A
                    outcome_A = voting_for_two_calculate_outcome(preference_matrix_A)

                    new_happiness_score = calculate_happiness(preference_matrix_A, outcome_A)
                    vector_happiness.append(new_happiness_score[voter-1])
                    preference_matrix_A_acc.append(preference_matrix_A)
        max_h = max(vector_happiness)
        index_max = vector_happiness.index(max_h)
        if max_h <= happiness_scores[voter-1]:
            return print("We cannot improve your happiness.")
    else:
        return print("We do not need to improve your happiness.")
    print("vector_happiness after compromising voting",vector_happiness[index_max])
    return preference_matrix_A_acc[index_max]

strategy_Compromising = Compromising(happiness_vector, preference_matrix, voter)
print(strategy_Compromising)
