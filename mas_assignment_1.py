import numpy as np
import operator
import collections
import random
import os.path as op
import pandas as pd
import argparse
import voting_schemes as vs
# import sys
# sys.stdout = open('stdout.txt', 'w') #to save in an external file

number_of_preferences = 5
number_of_voters = 8
voter = 2
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

def gen_random_preference_matrix(number_of_preferences,number_of_voters):
    preference_matrix = random.sample(range(number_of_preferences),number_of_preferences)
    for i in range(number_of_voters-1):
        preference_matrix = np.vstack([preference_matrix,random.sample(range(number_of_preferences),number_of_preferences)])
    return preference_matrix.T

def generate_fixed_pref_matrix(number_of_preferences,number_of_voters):
    preference_matrix = np.arange(number_of_preferences)
    preference_matrix = np.repeat([preference_matrix],number_of_voters,axis=0)
    return preference_matrix.T

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

def risk_calculate(number_of_options,number_of_voters):
    risk = (abs(number_of_options))/number_of_voters
    return risk

def calculate_outcome(voting_scheme, preference_matrix):
    if voting_scheme == "plurality":
        outcome = vs.plurality_calculate_outcome(preference_matrix)
    elif voting_scheme == "vote2":
        outcome = vs.voting_for_two_calculate_outcome(preference_matrix)
    elif voting_scheme == "anti_plurality":
        outcome = vs.antiplurality_calculate_outcome(preference_matrix)
    elif voting_scheme == "borda":
        outcome = vs.borda_calculate_outcome(preference_matrix)
    else:
        print("voting scheme not recognized, calculating for plurality voting")
        outcome = vs.borda_calculate_outcome(preference_matrix)

    return outcome


def tactical_voter(voting_scheme, preference_matrix, voter):

    outcome = calculate_outcome(voting_scheme, preference_matrix)

    happiness_vector = calculate_happiness(preference_matrix, outcome)

    #TODO: calculate properly
    bullet_matrix = bullet_voting(preference_matrix, voter)
    bullet_outcome = calculate_outcome(voting_scheme, bullet_matrix)

    strategy_Compromising, number_of_options = Compromising(happiness_vector, preference_matrix, voter)

    risk = risk_calculate(number_of_options, preference_matrix.shape[1])

    #TODO:
    overall_happiness = "2"
    strategic_options = "3"

    return outcome, overall_happiness, strategic_options, risk

def Compromising(happiness_scores, preference_matrix, voter):
    number_of_options = 0
    vector_happiness = []
    new_happiness_score = []
    preference_matrix_A_acc = []
    if happiness_scores[voter-1] != 1:#because the index starts frm 0
        print("We will try to improve your happiness.")
        for j in range(preference_matrix.shape[0]):
            if j>0: #we do not change the top preference, only an alternative
                for g in range(preference_matrix.shape[0]-j-1):#we will iterate through options. 2nd will check everything, but 1st. 3rd, all, but 1st and 2nd, etc.
                    number_of_options += 1
                    g = preference_matrix.shape[0] - g-1#inversing index
                    preference_matrix_A = preference_matrix
                    alternative_A = preference_matrix_A[j][voter-1]
                    preference_matrix_A[j][voter-1] = preference_matrix_A[g][voter-1]
                    preference_matrix_A[g][voter-1] = alternative_A
                    outcome_A = vs.antiplurality_calculate_outcome(preference_matrix_A)

                    new_happiness_score = calculate_happiness(preference_matrix_A, outcome_A)
                    vector_happiness.append(new_happiness_score[voter-1])
                    preference_matrix_A_acc.append(preference_matrix_A)
        max_h = max(vector_happiness)
        index_max = vector_happiness.index(max_h)
        if max_h <= happiness_scores[voter-1]:
            print("We cannot improve your happiness.")
            return happiness_scores[voter-1], number_of_options
    else:
        print("We do not need to improve your happiness.")
        return happiness_scores[voter-1], number_of_options
    print("vector_happiness after compromising voting",vector_happiness[index_max])
    return preference_matrix_A_acc[index_max], number_of_options


##-------------------------MAIN------------------------------------

#arguments
parser = argparse.ArgumentParser(description='choose the voting scheme and the input matrix.')
parser.add_argument('-s', '--scheme', dest='scheme', help='choose voting scheme: (plurality, vote2, anti_plurality, borda)')
parser.add_argument('-p', '--pref', dest='pref_matrix_path', help='preference matrix text file path')
args = parser.parse_args()

if args.pref_matrix_path:
    preference_matrix = return_pref_matrix_from_file(args.pref_matrix_path)
    print("input preference matrix:\n", preference_matrix)

    if args.scheme:
        print("Calculating strategic voting for: ", args.scheme, " scheme\n")
        print(tactical_voter(args.scheme, preference_matrix, voter))
        quit()
else:
    preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
    # preference_matrix = generate_fixed_pref_matrix(number_of_preferences,number_of_voters)
    print(preference_matrix)
    # preference_matrix_string = matrix_to_string(preference_matrix)
    # print(preference_matrix_string)

#HAPPINESS WITH HONEST VOTING
outcome_borda = vs.borda_calculate_outcome(preference_matrix)
outcome_plurality = vs.plurality_calculate_outcome(preference_matrix)
outcome_voting_for_two = vs.voting_for_two_calculate_outcome(preference_matrix)
outcome_antiplurality = vs.antiplurality_calculate_outcome(preference_matrix)
print(outcome_borda)
happiness_vector_borda = calculate_happiness(preference_matrix, outcome_borda)
happiness_vector_plurality = calculate_happiness(preference_matrix, outcome_plurality)
happiness_voting_for_two = calculate_happiness(preference_matrix, outcome_voting_for_two)
happiness_antiplurality = calculate_happiness(preference_matrix, outcome_antiplurality)
print("HAPPINESS:\n", np.vstack(happiness_vector_borda), "\n\n")

#HAPPINESS WITH BULLET VOTING
bullet_matrix = bullet_voting(preference_matrix, 0)
bullet_outcome_borda = vs.borda_calculate_outcome(bullet_matrix)
print(bullet_outcome_borda)
happiness_vector_bullet_borda = calculate_happiness(preference_matrix, bullet_outcome_borda)
print("HAPPINESS BULLET:\n", np.vstack(happiness_vector_bullet_borda), "\n\n")


strategy_Compromising, number_of_options = Compromising(happiness_vector_borda, preference_matrix, voter)
# risk_honest = risk_calculate(1,number_of_voters)#just let's discuss it over
risk_compromising = risk_calculate(number_of_options,number_of_voters)
print(strategy_Compromising)
print(number_of_options)
# print("risk honest =",risk_honest)
print("risk compromising =",risk_compromising)
