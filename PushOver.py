# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 22:41:29 2019

@author: Smail
"""

import random
import numpy as np
#import mas_assignment_1 as mas


number_of_preferences = 5
number_of_voters = 8

def gen_random_preference_matrix(number_of_preferences,number_of_voters):
    preference_matrix = random.sample(range(number_of_preferences),number_of_preferences)
    for i in range(number_of_voters-1):
        preference_matrix = np.vstack([preference_matrix,random.sample(range(number_of_preferences),number_of_preferences)])
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
    #in case of bullet voting
    try:
        del outcome[-1]
    except KeyError:
        False

    return outcome

#pref_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
pref_matrix = np.array([[0,1,2],[1,2,1],[2,0,0]])
print(pref_matrix)
strategic_voter = 2
preferences_strategic_voter = pref_matrix[:,strategic_voter]

outcome = calculate_outcome(pref_matrix)
print(outcome)
#print(min(outcome, key=outcome.get))

def get_easy_to_beat_preference(outcome):#preference with minimum_score
    temp = min(outcome.values()) 
    minimum_preference = [key for key in outcome if outcome[key] == temp] 
    if(len(minimum_preference)>1):
        return minimum_preference[random.randint(len(minimum_preference))][0]
    else:
        return minimum_preference[0]


easy_to_beat_pref = get_easy_to_beat_preference(outcome)
index_easy_pref = np.where(preferences_strategic_voter == easy_to_beat_pref)
index_easy_pref = index_easy_pref[0][0]
print("easy_to_beat_pref",easy_to_beat_pref)
print(index_easy_pref)
max_rounds = index_easy_pref - 1
print(max_rounds)
for i in range(max_rounds):
    preferences_strategic_voter[[index_easy_pref,index_easy_pref - 1]] = preferences_strategic_voter[[index_easy_pref - 1,index_easy_pref]]
    index_easy_pref -= 1
    changed_pref = np.copy(pref_matrix)
    changed_pref[:,strategic_voter] = preferences_strategic_voter
    print(changed_pref)
#true_pref_voter = pref_matrix[0][strategic_voter]
#print(true_pref_voter)


