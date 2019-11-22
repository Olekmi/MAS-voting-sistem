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
from mas_assignment_1 import *
import matplotlib.pyplot as plt


def scheme_risk_assessment(number_of_voters, number_of_experiments):
    risk_matrix_borda = np.zeros((number_of_voters,number_of_experiments))
    risk_matrix_plurality =  np.zeros((number_of_voters,number_of_experiments))
    risk_matrix_vote2 =  np.zeros((number_of_voters,number_of_experiments))
    risk_matrix_antiplurality =  np.zeros((number_of_voters,number_of_experiments))
    for i in range(number_of_experiments):
        preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
        #risk_average_borda = 0
        #risk_average_vote2 = 0
        #risk_average_antiplurality = 0
        #risk_average_plurality = 0
        for voter in range(number_of_voters):
            _, _, _, risk_matrix_borda[voter,i]=tactical_voter("borda", preference_matrix, voter)
            _, _, _, risk_matrix_vote2[voter,i]=tactical_voter("vote2", preference_matrix, voter)
            _, _, _, risk_matrix_antiplurality[voter,i]=tactical_voter("anti_plurality", preference_matrix, voter)
            _, _, _, risk_matrix_plurality[voter,i]=tactical_voter("plurality", preference_matrix, voter)
           # print("AAAAA")
            #print(risk_borda)
            #risk_average_borda +=risk_borda
            #risk_average_vote2 +=risk_vote2
            #risk_average_antiplurality +=risk_antiplurality
            #risk_average_plurality +=risk_plurality
        #risk_average_borda *= (1/number_of_voters)
        #risk_average_vote2 *= (1/number_of_voters)
        #risk_average_antiplurality *= (1/number_of_voters)
        #risk_average_plurality *= (1/number_of_voters)
        
        #risk_vector_borda[i] = risk_average_borda
        #risk_vector_vote2[i] = risk_average_vote2
        #risk_vector_antiplurality[i] = risk_average_antiplurality
        #risk_vector_plurality[i] = risk_average_plurality
    print("Done")
    x_data = np.zeros(number_of_experiments)
    for i in range(number_of_experiments):
        x_data[i] = i
    plt.plot(x_data, np.amax(risk_matrix_borda, axis=0))
    plt.plot(x_data, np.amax(risk_matrix_plurality, axis=0))
    plt.plot(x_data, np.amax(risk_matrix_vote2, axis=0))
    plt.plot(x_data, np.amax(risk_matrix_antiplurality, axis=0))
    plt.show()

    print("average borda risk", np.average(np.amax(risk_matrix_borda, axis=0)))
    print("average plurallity risk",np.average(np.amax(risk_matrix_plurality, axis=0)))
    print("average voting for two risk",np.average(np.amax(risk_matrix_vote2, axis=0)))
    print("average antiplurality risk",np.average(np.amax(risk_matrix_antiplurality, axis=0)))




#voting_scheme = "borda"
def massive_voting(number_of_experiments):
    total_happiness_borda = np.zeros(number_of_experiments)
    total_happiness_plurality =  np.zeros(number_of_experiments)
    total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    total_happiness_antiplurality =  np.zeros(number_of_experiments)



    for i in range(number_of_experiments):
        preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
        

#HAPPINESS WITH HONEST VOTING
        outcome_borda = vs.borda_calculate_outcome(preference_matrix)
        outcome_plurality = vs.plurality_calculate_outcome(preference_matrix)
        outcome_voting_for_two = vs.voting_for_two_calculate_outcome(preference_matrix)
        outcome_antiplurality = vs.antiplurality_calculate_outcome(preference_matrix)
#print(outcome_borda)
        happiness_vector_borda = calculate_happiness(preference_matrix, outcome_borda)
        happiness_vector_plurality = calculate_happiness(preference_matrix, outcome_plurality)
        happiness_voting_for_two = calculate_happiness(preference_matrix, outcome_voting_for_two)
        happiness_antiplurality = calculate_happiness(preference_matrix, outcome_antiplurality)

        total_happiness_borda[i] = np.sum(happiness_vector_borda)
        total_happiness_plurality[i] =np.sum(happiness_vector_plurality)
        total_happiness_voting_for_two[i] =np.sum(happiness_voting_for_two)
        total_happiness_antiplurality[i] = np.sum(happiness_antiplurality)



#print("HAPPINESS:\n", np.vstack(happiness_vector_borda), "\n\n")
    print("Done")
    x_data = np.zeros(number_of_experiments)
    for i in range(number_of_experiments):
        x_data[i] = i
#y_borda = total_happiness_borda
#y_plurality = total_happiness_plurality
#y_voting_for_two = total_happiness_voting_for_two
#y_antiplurality = total_happiness_antiplurality

    plt.plot(x_data, total_happiness_borda)
    plt.plot(x_data, total_happiness_plurality)
    plt.plot(x_data, total_happiness_voting_for_two)
    plt.plot(x_data, total_happiness_antiplurality)
    plt.show()

    print("average borda happiness", np.average(total_happiness_borda))
    print("average plurallity happiness",np.average(total_happiness_plurality))
    print("average voting for two happiness",np.average(total_happiness_voting_for_two))
    print("average antiplurality happiness",np.average(total_happiness_antiplurality))

    print("Standard deviation borda happiness", np.std(total_happiness_borda))
    print("Standard deviation pplurallity happiness",np.std(total_happiness_plurality))
    print("Standard deviation voting for two happiness",np.std(total_happiness_voting_for_two))
    print("Standard deviation antiplurality happiness",np.std(total_happiness_antiplurality))


#MAIN

number_of_preferences = 5
number_of_voters = 10
number_of_experiments = 100




voter = 0

#massive_voting(number_of_experiments)
scheme_risk_assessment(number_of_voters, number_of_experiments)