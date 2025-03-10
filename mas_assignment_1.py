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
    z_hap_dif = new_overall_happiness[voter] - old_overall_happiness[voter]
    z_information = "Bullet voting chosen because the individual happiness was increased by {difference_value:.3f}".format(difference_value = z_hap_dif)
    if z_hap_dif>0:
        number_of_options = 1
        si.append((list(bullet_pref_matrix[:,voter]), new_outcome, np.sum(new_overall_happiness), z_information))
    
    # if len(si) == 0:
    #    z_information = "We cannot improve happiness."
    #    si.append((list(preference_matrix[:,voter]), calculate_outcome(voting_scheme, preference_matrix), np.sum(new_overall_happiness), z_information))
 
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
    si_bullet_voting, number_of_options_bull = bullet_voting(preference_matrix, voter, voting_scheme)
    
    
    si_comp, number_of_options_comp = Compromising(happiness_vector, preference_matrix, voter, voting_scheme)

    if len(si_bullet_voting)>0:
        si_comp.append(si_bullet_voting[0])#because si_bullet_voting is a list of tuple. the list is of size 1

    number_of_options =number_of_options_comp
    si = si_comp

    risk = risk_calculate(number_of_options, preference_matrix.shape[1])
    print("individual happiness vector", happiness_vector)

    overall_happiness = np.sum(happiness_vector)
    strategic_options = si[:]

    return outcome, overall_happiness, strategic_options, risk

def Compromising(happiness_scores, preference_matrix, voter, voting_scheme):
    vector_happiness = []
    new_happiness_score = []
    preference_matrix_A_acc = []
    si =[]
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
                    si_list = (list(preference_matrix_A[:,voter]), outcome_A, np.sum(new_happiness_score), z_information)
                    si.append(si_list)
                vector_happiness.append(new_happiness_score[voter])
                preference_matrix_A_acc.append(preference_matrix_A)

    # if len(si) == 0:
    #    z_information = "We cannot improve happiness."
    #    si.append((list(preference_matrix[:,voter]), calculate_outcome(voting_scheme, preference_matrix), np.sum(new_happiness_score), z_information))
    
    return si, len(si)

#choose strategic voter depending if we want "selfish" or "altruistic" agent
def choose_strategic_voter(preference_matrix,voting_scheme,behavior):
    if(behavior != "selfish" and behavior != "altruistic"):
        return 0 # default voter is the first one if there is an invalid behavior
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
            individual_happiness_improvement = re.findall(r'\d+\.\d+', strategic_options[i][3])
            if(len(individual_happiness_improvement)>0):#checking if valid strategic option
                options_tuples.append([voter_index,strategic_options[i]])


        for i in range(len(options_tuples) - len(list_differences_overall_happiness)):
            difference_indiv_option_overall = abs(overall_honnest_happiness - options_tuples[i][1][2])
            list_differences_overall_happiness.append(difference_indiv_option_overall)
            
            individual_happiness_strat_option = re.findall(r'\d+\.\d+', options_tuples[i][1][3])[0]
            list_difference_individual_happiness.append(abs(individual_honnest_happiness - float(individual_happiness_strat_option)))

    if(behavior == "selfish"):
        if len(list_difference_individual_happiness) == 0:
            strategic_voter_index = np.random.randint(0,number_voters)
            agent_type = "none"
        else:
            index_tuple = np.argmax(list_difference_individual_happiness)
            strategic_voter_index = options_tuples[index_tuple][0]    
            agent_type = "selfish"
    if(behavior == "altruistic"):
        if len(list_differences_overall_happiness) == 0:
            strategic_voter_index = np.random.randint(0,number_voters)
            agent_type = "none"
        else:  
            index_tuple = np.argmax(list_differences_overall_happiness)
            strategic_voter_index = options_tuples[index_tuple][0]
            agent_type = "altruistic"

    return strategic_voter_index,agent_type


def extract_str_from_text(text):
    string = []
    for word in text.split():
        try:
            string.append(float(word))
        except ValueError:
            pass
    return string    

##-------------------------MAIN------------------------------------

# default
number_of_preferences = 6
number_of_voters = 8

voter = 1
voting_scheme = "borda"

#arguments
parser = argparse.ArgumentParser(description='choose the voting scheme and the input matrix.')
parser.add_argument('-s', '--scheme', dest='scheme', help='Choose voting scheme: (plurality, vote2, anti_plurality, borda)')
parser.add_argument('-p', '--pref', dest='pref_matrix_file_name', help='preference matrix text file name. Each preference \
                    should be separated by a comma and the file should not contain an empty space.')
parser.add_argument('-v', '--voter', dest='voter', help='Choose the index of the voter, that strategic voting will be calculated for. ')
parser.add_argument('-b', '--behavior', dest='behavior', help='If a voter is not selected you can choose the behavior of a voter(selfish, altruistic). The voter with the most fitting result for this behavior will be selected.')
args = parser.parse_args()

#for debbuging only
# args.pref_matrix_path = "input_preference_matrix_letters.txt"
# args.scheme = "borda"

if args.pref_matrix_file_name:
    preference_matrix = util.return_pref_matrix_from_file(args.pref_matrix_file_name)
    print("input preference matrix:\n", preference_matrix)

else:
    preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
    # preference_matrix = generate_fixed_pref_matrix(number_of_preferences,number_of_voters)
    print(preference_matrix)
    # preference_matrix_string = matrix_to_string(preference_matrix)
    # print(preference_matrix_string)

if args.voter:
    voter =  int(args.voter)

if args.scheme:

    if args.behavior:
        if args.behavior =="altruistic" or args.behavior == "selfish":
            voter, agent_type = choose_strategic_voter(preference_matrix, args.scheme,args.behavior)
            print("selecting the most ", args.behavior, " voter: ", voter, "\n")
        else:
            print("wrong value for behavior, exiting")
            quit()
            

    print("Calculating strategic voting for: ", args.scheme, " scheme\n")
    outcome, overall_happiness, strategic_options, risk = tactical_voter(args.scheme, preference_matrix, voter)

    print("original outcome: ", outcome)
    print("overall happiness of honest voting: ", overall_happiness)
    print("risk: ", risk)
    print("strategic options of the ", voter ," voter: ")
    if strategic_options == []:
        print("No options for this voter")
    else:
        for prnt in strategic_options:
            print(prnt)
    quit()

# else:
#     print("Please select a scheme to continue.")
#     quit()


#****************************************************************************************
#**********************TESTS AND EXPERIMENTS not executable in main pipeline**************
#****************************************************************************************

#HAPPINESS WITH HONEST VOTING for 
outcome_borda = vs.borda_calculate_outcome(preference_matrix)
outcome_plurality = vs.plurality_calculate_outcome(preference_matrix)
outcome_voting_for_two = vs.voting_for_two_calculate_outcome(preference_matrix)
outcome_antiplurality = vs.antiplurality_calculate_outcome(preference_matrix)
#for an optimised agent

happiness_vector_borda = calculate_happiness(preference_matrix, outcome_borda)
happiness_vector_plurality = calculate_happiness(preference_matrix, outcome_plurality)
happiness_voting_for_two = calculate_happiness(preference_matrix, outcome_voting_for_two)
happiness_antiplurality = calculate_happiness(preference_matrix, outcome_antiplurality)
#in overall
happiness_overall_vector_borda = np.sum(calculate_happiness(preference_matrix, outcome_borda))
happiness_overall_vector_plurality = np.sum(calculate_happiness(preference_matrix, outcome_plurality))
happiness_overall_voting_for_two = np.sum(calculate_happiness(preference_matrix, outcome_voting_for_two))
happiness_overall_antiplurality = np.sum(calculate_happiness(preference_matrix, outcome_antiplurality))
print("HAPPINESS:\n", np.vstack(happiness_vector_borda), "\n\n")

#HAPPINESS WITH COMPROMISING VOTING for selfish
voter_compromising_plurality,agent_type = choose_strategic_voter(preference_matrix,"plurality","selfish")
voter_compromising_voting_for_two,agent_type = choose_strategic_voter(preference_matrix,"vote2","selfish")
voter_compromising_anti_plurality,agent_type = choose_strategic_voter(preference_matrix,"anti_plurality","selfish")
voter_compromising_borda,agent_type = choose_strategic_voter(preference_matrix,"borda","selfish")

compromising_plurality, len_si = Compromising(happiness_vector_plurality, preference_matrix, voter_compromising_plurality, "plurality")
compromising_voting_for_two, len_si = Compromising(happiness_voting_for_two, preference_matrix, voter_compromising_voting_for_two, "vote2")
compromising_anti_plurality, len_si = Compromising(happiness_antiplurality, preference_matrix, voter_compromising_anti_plurality, "anti_plurality")
compromising_borda, len_si = Compromising(happiness_vector_borda, preference_matrix, voter_compromising_borda, "borda")

happiness_vector_borda_agent = (np.round(extract_str_from_text(compromising_borda[0][3])+happiness_vector_borda[voter_compromising_borda],2))
happiness_vector_plurality_agent = (np.round(extract_str_from_text(compromising_plurality[0][3])+happiness_vector_plurality[voter_compromising_plurality],2))
happiness_voting_for_two_agent = (np.round(extract_str_from_text(compromising_voting_for_two[0][3])+happiness_voting_for_two[voter_compromising_voting_for_two],2))
happiness_antiplurality_agent = (np.round(extract_str_from_text(compromising_anti_plurality[0][3])+happiness_antiplurality[voter_compromising_anti_plurality],2))

#HAPPINESS WITH COMPROMISING VOTING for altruistic
voter_compromising_alt_plurality,agent_type = choose_strategic_voter(preference_matrix,"plurality","altruistic")
voter_compromising_alt_voting_for_two,agent_type = choose_strategic_voter(preference_matrix,"vote2","altruistic")
voter_compromising_alt_anti_plurality,agent_type = choose_strategic_voter(preference_matrix,"anti_plurality","altruistic")
voter_compromising_alt_borda,agent_type = choose_strategic_voter(preference_matrix,"borda","altruistic")

compromising_alt_plurality, len_si = Compromising(happiness_vector_plurality, preference_matrix, voter_compromising_alt_plurality, "plurality")
compromising_alt_voting_for_two, len_si = Compromising(happiness_voting_for_two, preference_matrix, voter_compromising_alt_voting_for_two, "vote2")
compromising_alt_anti_plurality, len_si = Compromising(happiness_antiplurality, preference_matrix, voter_compromising_alt_anti_plurality, "anti_plurality")
compromising_alt_borda, len_si = Compromising(happiness_vector_borda, preference_matrix, voter_compromising_alt_borda, "borda")



#HAPPINESS WITH Bullet VOTING for selfish
voter_bullet_plurality,agent_type = choose_strategic_voter(preference_matrix,"plurality","selfish")
voter_bullet_voting_for_two,agent_type = choose_strategic_voter(preference_matrix,"vote2","selfish")
voter_bullet_anti_plurality,agent_type = choose_strategic_voter(preference_matrix,"anti_plurality","selfish")
voter_bullet_borda,agent_type = choose_strategic_voter(preference_matrix,"borda","selfish")
bullet_plurality, len_si = bullet_voting(preference_matrix, voter_bullet_plurality, "plurality")
bullet_voting_for_two, len_si = bullet_voting(preference_matrix, voter_bullet_voting_for_two, "vote2")
bullet_anti_plurality, len_si = bullet_voting(preference_matrix, voter_bullet_anti_plurality, "anti_plurality")
bullet_borda, len_si = bullet_voting(preference_matrix, voter_bullet_borda, "borda")

happiness_vector_borda_bagent = (np.round(extract_str_from_text(bullet_borda[0][3])+happiness_vector_borda[voter_bullet_borda],2))
happiness_vector_plurality_bagent = (np.round(extract_str_from_text(bullet_plurality[0][3])+happiness_vector_plurality[voter_bullet_plurality],2))
happiness_voting_for_two_bagent = (np.round(extract_str_from_text(bullet_voting_for_two[0][3])+happiness_voting_for_two[voter_bullet_voting_for_two],2))
happiness_antiplurality_bagent = (np.round(extract_str_from_text(bullet_anti_plurality[0][3])+happiness_antiplurality[voter_bullet_anti_plurality],2))


#HAPPINESS WITH Bullet VOTING for altruistic
voter_bullet_alt_plurality,agent_type = choose_strategic_voter(preference_matrix,"plurality","altruistic")
voter_bullet_alt_voting_for_two,agent_type = choose_strategic_voter(preference_matrix,"vote2","altruistic")
voter_bullet_alt_anti_plurality,agent_type = choose_strategic_voter(preference_matrix,"anti_plurality","altruistic")
voter_bullet_alt_borda,agent_type = choose_strategic_voter(preference_matrix,"borda","altruistic")
bullet_alt_plurality, len_si = bullet_voting(preference_matrix, voter_bullet_alt_plurality, "plurality")
bullet_alt_voting_for_two, len_si = bullet_voting(preference_matrix, voter_bullet_alt_voting_for_two, "vote2")
bullet_alt_anti_plurality, len_si = bullet_voting(preference_matrix, voter_bullet_alt_anti_plurality, "anti_plurality")
bullet_alt_borda, len_si = bullet_voting(preference_matrix, voter_bullet_alt_borda, "borda")
#HAPPINESS WITH BULLET VOTING
bullet_list, number_of_options_bullet= bullet_voting(preference_matrix, voter, voting_scheme)


strategy_Compromising, number_of_options = Compromising(happiness_vector_borda, preference_matrix, voter, voting_scheme)
# risk_honest = risk_calculate(1,number_of_voters)#just let's discuss it over
risk_compromising = risk_calculate(number_of_options,number_of_voters)
print(strategy_Compromising)
print(number_of_options)
# print("risk honest =",risk_honest)
print("risk compromising =",risk_compromising)

tactical_voter(voting_scheme, preference_matrix, voter)
#for i in range(100):
#voter = choose_strategic_voter(preference_matrix,voting_scheme,"altruistic")
print("altruistic voter",voter)
