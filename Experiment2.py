#This experiment investigates what would happen if 50% of the voters have the same 
#preferences while the other half have random preferences
#We will have 4 scenarios:
###### selfish agent
###### altruistic agent
###### agent among majority
###### agent among minority

import re
import numpy as np
import voting_schemes as vs
from mas_assignment_1 import  gen_random_preference_matrix, generate_fixed_pref_matrix, calculate_happiness, tactical_voter
from mas_assignment_1 import  choose_strategic_voter, risk_calculate, calculate_outcome, bullet_voting, Compromising
import matplotlib.pyplot as plt


number_of_preferences = 5
number_of_voters = 10
number_of_experiments = 100
same_preference_half = generate_fixed_pref_matrix(number_of_preferences,0.5*number_of_voters)


total_happiness_borda = np.zeros(number_of_experiments)
total_happiness_plurality =  np.zeros(number_of_experiments)
total_happiness_voting_for_two =  np.zeros(number_of_experiments)
total_happiness_antiplurality =  np.zeros(number_of_experiments)


for i in range(number_of_experiments):
    random_preference_half = gen_random_preference_matrix(number_of_preferences,int(0.5*number_of_voters))
    preference_matrix = np.append(same_preference_half,random_preference_half,axis=1)
    #HAPPINESS WITH HONEST VOTING
    outcome_borda = vs.borda_calculate_outcome(preference_matrix)
    outcome_plurality = vs.plurality_calculate_outcome(preference_matrix)
    outcome_voting_for_two = vs.voting_for_two_calculate_outcome(preference_matrix)
    outcome_antiplurality = vs.antiplurality_calculate_outcome(preference_matrix)

    
    happiness_vector_borda = calculate_happiness(preference_matrix, outcome_borda)
    happiness_vector_plurality = calculate_happiness(preference_matrix, outcome_plurality)
    happiness_voting_for_two = calculate_happiness(preference_matrix, outcome_voting_for_two)
    happiness_antiplurality = calculate_happiness(preference_matrix, outcome_antiplurality)

    total_happiness_borda[i] = np.sum(happiness_vector_borda)
    total_happiness_plurality[i] =np.sum(happiness_vector_plurality)
    total_happiness_voting_for_two[i] =np.sum(happiness_voting_for_two)
    total_happiness_antiplurality[i] = np.sum(happiness_antiplurality)
    
print("Done")
x_data = np.zeros(number_of_experiments)
for i in range(number_of_experiments):
    x_data[i] = i

#plt.plot(x_data, total_happiness_borda,label="borda")
#plt.plot(x_data, total_happiness_plurality, label = "plurality")
#plt.plot(x_data, total_happiness_voting_for_two, label = "voting for two")
#plt.plot(x_data, total_happiness_antiplurality, label = "antiplurality")
#plt.hist(total_happiness_borda, color = 'blue', edgecolor = 'black')

#plt.hist(total_happiness_plurality)

#plt.legend()
#plt.show()

print("average honnest borda happiness", np.average(total_happiness_borda))
print("average honnest plurallity happiness",np.average(total_happiness_plurality))
print("average honnest voting for two happiness",np.average(total_happiness_voting_for_two))
print("average honnest antiplurality happiness",np.average(total_happiness_antiplurality))
print()
print("Standard deviation honnest borda happiness", np.std(total_happiness_borda))
print("Standard deviation honnest plurallity happiness",np.std(total_happiness_plurality))
print("Standard deviation honnest voting for two happiness",np.std(total_happiness_voting_for_two))
print("Standard deviation honnest antiplurality happiness",np.std(total_happiness_antiplurality))

#scenario 1
#selfish agent

selfish_total_happiness_borda = np.zeros(number_of_experiments)
selfish_total_happiness_plurality =  np.zeros(number_of_experiments)
selfish_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
selfish_total_happiness_antiplurality =  np.zeros(number_of_experiments)


difference_selfish_total_happiness_borda = np.zeros(number_of_experiments)
difference_selfish_total_happiness_plurality =  np.zeros(number_of_experiments)
difference_selfish_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
difference_selfish_total_happiness_antiplurality =  np.zeros(number_of_experiments)

average_difference_selfish_total_happiness_borda = np.zeros(number_of_experiments)
average_difference_selfish_total_happiness_plurality =  np.zeros(number_of_experiments)
average_difference_selfish_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
average_difference_selfish_total_happiness_antiplurality =  np.zeros(number_of_experiments)






agent_behavior = "selfish"

for i in range(number_of_experiments):
    random_preference_half = gen_random_preference_matrix(number_of_preferences,int(0.5*number_of_voters))
    preference_matrix = np.append(same_preference_half,random_preference_half,axis=1)
    
    borda_tactical_voter_index = choose_strategic_voter(preference_matrix,"borda",agent_behavior)[0]
    _, overall_happiness_borda, _, _ = tactical_voter("borda",preference_matrix,borda_tactical_voter_index)
    selfish_total_happiness_borda[i] = overall_happiness_borda
    difference_selfish_total_happiness_borda[i] = overall_happiness_borda - total_happiness_borda[i]
    average_difference_selfish_total_happiness_borda[i] = overall_happiness_borda - np.average(total_happiness_borda)
    
    
    vote_two_tactical_voter_index = choose_strategic_voter(preference_matrix,"vote2",agent_behavior)[0]
    _, overall_happiness_vote_two, _, _ = tactical_voter("vote2",preference_matrix,borda_tactical_voter_index)
    selfish_total_happiness_voting_for_two[i] = overall_happiness_vote_two
    difference_selfish_total_happiness_voting_for_two[i] = overall_happiness_vote_two - total_happiness_voting_for_two[i]
    average_difference_selfish_total_happiness_voting_for_two = overall_happiness_vote_two - np.average(total_happiness_voting_for_two)
    
    antiplurality_tactical_voter_index = choose_strategic_voter(preference_matrix,"anti_plurality",agent_behavior)[0]
    _, overall_happiness_antiplurality, _, _ = tactical_voter("anti_plurality",preference_matrix,borda_tactical_voter_index)
    selfish_total_happiness_antiplurality[i] = overall_happiness_antiplurality
    difference_selfish_total_happiness_plurality[i] = overall_happiness_antiplurality - total_happiness_antiplurality[i]
    average_difference_selfish_total_happiness_antiplurality = overall_happiness_antiplurality - np.average(total_happiness_antiplurality)
    
    plurality_tactical_voter_index = choose_strategic_voter(preference_matrix,"plurality",agent_behavior)[0]
    _, overall_happiness_plurality, _, _ = tactical_voter("plurality",preference_matrix,borda_tactical_voter_index)
    selfish_total_happiness_plurality[i] = overall_happiness_plurality
    difference_selfish_total_happiness_plurality[i] = overall_happiness_plurality - total_happiness_plurality[i]
    average_difference_selfish_total_happiness_plurality = overall_happiness_plurality - np.average(total_happiness_plurality)
    
    
    
    

    
    
    
    








    



