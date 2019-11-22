import numpy as np
import operator
import collections
import random
import os.path as op
import pandas as pd
import argparse
import voting_schemes as vs
import util
import re
# import sys
# sys.stdout = open('stdout.txt', 'w') #to save in an external file


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

def bullet_voting(preference_matrix, voter, voting_scheme):
    si = []
    number_of_options = 0
    bullet_pref_matrix = np.copy(preference_matrix)
    bullet_pref_matrix[1:, voter] = -1
    new_outcome = calculate_outcome(voting_scheme, bullet_pref_matrix )
    old_outcome = calculate_outcome(voting_scheme, preference_matrix)
    new_overall_happiness = calculate_happiness(preference_matrix, new_outcome)
    old_overall_happiness = calculate_happiness(preference_matrix, old_outcome)
    z_hap_dif = new_overall_happiness[voter] - old_overall_happiness[voter]# change that to voter ???
#    si_list = [bullet_pref_matrix[:,voter], new_outcome, new_overall_happiness, z_hap_dif]
    z_information = "Bullet voting chosen because the individual happiness was increased by {difference_value:.3f}".format(difference_value = z_hap_dif)
    if z_hap_dif>0:
        number_of_options = 1
        si = (list(bullet_pref_matrix[:,voter]), new_outcome, np.sum(new_overall_happiness), z_information)
    return si, number_of_options

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
        print("voting scheme not recognized, exiting")
        quit()
    return outcome


def tactical_voter(voting_scheme, preference_matrix, voter):

    outcome = calculate_outcome(voting_scheme, preference_matrix)

    happiness_vector = calculate_happiness(preference_matrix, outcome)
    #si = strategic options
    si_bull, number_of_options_bull = bullet_voting(preference_matrix, voter, voting_scheme)
    
    
    si_comp, number_of_options_comp = Compromising(happiness_vector, preference_matrix, voter, voting_scheme)

    if len(si_bull)>0:
        si_comp.append(si_bull)

    number_of_options =number_of_options_comp
    si = si_comp

    risk = risk_calculate(number_of_options, preference_matrix.shape[1])

    overall_happiness = np.sum(happiness_vector)
    strategic_options = si[:]

    return outcome, overall_happiness, strategic_options, risk

def Compromising(happiness_scores, preference_matrix, voter, voting_scheme):
    #number_of_options = 0
    vector_happiness = []
    new_happiness_score = []
    preference_matrix_A_acc = []
    si =[]
    index_max = 0
    for j in range(preference_matrix.shape[0]):
        if j>0: #we do not change the top preference, only an alternative
            for g in range(preference_matrix.shape[0]-j-1):#we will iterate through options. 2nd will check everything, but 1st. 3rd, all, but 1st and 2nd, etc.

                g = preference_matrix.shape[0] - g-1#inversing index
                # preference_matrix_A = preference_matrix
                preference_matrix_A = np.array(preference_matrix)#CHANGED-put NP array
                alternative_A = preference_matrix_A[j][voter]
                preference_matrix_A[j][voter] = preference_matrix_A[g][voter]
                preference_matrix_A[g][voter] = alternative_A
                outcome_A = calculate_outcome(voting_scheme, preference_matrix_A)#Changed

                new_happiness_score = calculate_happiness(preference_matrix, outcome_A)
                
                z_hap_dif = new_happiness_score[voter]-happiness_scores[voter]

                if z_hap_dif>0:
                    z_information = "Compromising chosen because the individual happiness was increased by {difference_value:.3f}".format(difference_value = z_hap_dif)
#                    si_list = [preference_matrix_A[:,voter], outcome_A, new_happiness_score, z_information]
                    si_list = (list(preference_matrix_A[:,voter]), outcome_A, np.sum(new_happiness_score), z_information)
                    si.append(si_list)
                vector_happiness.append(new_happiness_score[voter])
                preference_matrix_A_acc.append(preference_matrix_A)
    #not needed
    max_h = max(vector_happiness)
    index_max = vector_happiness.index(max_h)
    
    return si, len(si)

#choose strategic voter depending if we want "selfish" or "altruistic" agent
def choose_strategic_voter(preference_matrix,voting_scheme,behavior):
    if(behavior != "selfish" and behavior != "altruistic"):
        return 0
    number_voters = preference_matrix.shape[1]
    options_tuples = []
    list_differences_overall_happiness = []
    list_difference_individual_happiness = []
    for voter_index in range(number_voters):
        if voting_scheme == "plurality":
            honnest_outcome_plurality = vs.plurality_calculate_outcome(preference_matrix)
            honnest_overall_happiness_plurality = calculate_happiness(preference_matrix, honnest_outcome_plurality)
            overall_honnest_happiness = sum(honnest_overall_happiness_plurality)
            individual_honnest_happiness = honnest_overall_happiness_plurality[voter_index]
        if voting_scheme == "vote2":
            honnest_outcome_vote_for_two = vs.voting_for_two_calculate_outcome(preference_matrix)
            honnest_overall_happiness_vote_for_two = calculate_happiness(preference_matrix, honnest_outcome_vote_for_two)
            overall_honnest_happiness = sum(honnest_overall_happiness_vote_for_two)
            individual_honnest_happiness = honnest_overall_happiness_vote_for_two[voter_index]
        if voting_scheme == "anti_plurality":
            honnest_outcome_anti_plurality = vs.antiplurality_calculate_outcome(preference_matrix)
            honnest_overall_happiness_anti_plurality = calculate_happiness(preference_matrix, honnest_outcome_anti_plurality)
            overall_honnest_happiness = sum(honnest_overall_happiness_anti_plurality)
            individual_honnest_happiness = honnest_overall_happiness_anti_plurality[voter_index]
        if voting_scheme == "borda":
            honnest_outcome_borda = vs.borda_calculate_outcome(preference_matrix)
            honnest_overall_happiness_borda = calculate_happiness(preference_matrix, honnest_outcome_borda)
            overall_honnest_happiness = sum(honnest_overall_happiness_borda)
            individual_honnest_happiness = honnest_overall_happiness_borda[voter_index]

        outcome, overall_happiness, strategic_options, risk = tactical_voter(voting_scheme,preference_matrix,voter_index)
        for i in range(len(strategic_options)):
            options_tuples.append([voter_index,strategic_options[i]])


        for i in range(len(options_tuples) - len(list_differences_overall_happiness)):
            difference_indiv_option_overall = abs(overall_honnest_happiness - options_tuples[i][1][2])
            list_differences_overall_happiness.append(difference_indiv_option_overall)

            individual_happiness_strat_option = re.findall(r'\d+\.\d+', options_tuples[i][1][3])[0]
            list_difference_individual_happiness.append(abs(individual_honnest_happiness - float(individual_happiness_strat_option)))
    
    if(behavior == "selfish"):
        index_tuple = np.argmax(list_difference_individual_happiness)            
    if(behavior == "altruistic"):
        index_tuple = np.argmax(list_differences_overall_happiness)
        

    strategic_voter_index = options_tuples[index_tuple][0]
    
    return strategic_voter_index
    
                    




##-------------------------MAIN------------------------------------

# default
number_of_preferences = 6
number_of_voters = 8

voter = 0
voting_scheme = "borda"

#arguments
parser = argparse.ArgumentParser(description='choose the voting scheme and the input matrix.')
parser.add_argument('-s', '--scheme', dest='scheme', help='Choose voting scheme: (plurality, vote2, anti_plurality, borda)')
parser.add_argument('-p', '--pref', dest='pref_matrix_file_name', help='preference matrix text file name. Each preference \
                    should be separated by a comma and the file should not contain an empty space.')
args = parser.parse_args()

#for debbuging only
# args.pref_matrix_path = "input_preference_matrix_letters.txt"
# args.scheme = "borda"

if args.pref_matrix_file_name:
    preference_matrix = util.return_pref_matrix_from_file(args.pref_matrix_file_name)
    print("input preference matrix:\n", preference_matrix)

    if args.scheme:
        print("Calculating strategic voting for: ", args.scheme, " scheme\n")
        outcome, overall_happiness, strategic_options, risk = tactical_voter(args.scheme, preference_matrix, voter)

        print("outcome: ", outcome)
        print("overall happiness: ", overall_happiness)
        print("risk: ", risk)
        print("strategic options of the voter: ")
        for prnt in strategic_options:
            print(prnt)
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
bullet_list, number_of_options_bullet= bullet_voting(preference_matrix, voter, voting_scheme)


#bullet_outcome_borda = borda_calculate_outcome(bullet_matrix) #
#print(bullet_outcome_borda)
#happiness_vector_bullet_borda = calculate_happiness(preference_matrix, bullet_outcome_borda)
#print("HAPPINESS BULLET:\n", np.vstack(happiness_vector_bullet_borda), "\n\n")


strategy_Compromising, number_of_options = Compromising(happiness_vector_borda, preference_matrix, voter, voting_scheme)
# risk_honest = risk_calculate(1,number_of_voters)#just let's discuss it over
risk_compromising = risk_calculate(number_of_options,number_of_voters)
print(strategy_Compromising)
print(number_of_options)
# print("risk honest =",risk_honest)
print("risk compromising =",risk_compromising)

tactical_voter(voting_scheme, preference_matrix, voter)
voter = choose_strategic_voter(preference_matrix,voting_scheme,"altruistic")
print(voter)
