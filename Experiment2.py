#This experiment investigates what would happen if 50% of the voters have the same 
#preferences while the other half have random preferences
#We will choose the strategic voter as a selfish agent, meaning it wants to increase its own happiness


import numpy as np
import voting_schemes as vs
from mas_assignment_1 import  gen_random_preference_matrix, generate_fixed_pref_matrix, calculate_happiness, choose_strategic_voter
import matplotlib.pyplot as plt


number_of_preferences = 5
number_of_voters = 10
number_of_experiments = 1000

total_happiness_borda = np.zeros(number_of_experiments)
total_happiness_plurality =  np.zeros(number_of_experiments)
total_happiness_voting_for_two =  np.zeros(number_of_experiments)
total_happiness_antiplurality =  np.zeros(number_of_experiments)

average_happiness_borda = np.zeros(number_of_experiments)
average_happiness_plurality =  np.zeros(number_of_experiments)
average_happiness_voting_for_two =  np.zeros(number_of_experiments)
average_happiness_antiplurality =  np.zeros(number_of_experiments)


same_preference_half = generate_fixed_pref_matrix(number_of_preferences,0.5*number_of_voters)

for i in range(number_of_experiments):
    random_preference_half = gen_random_preference_matrix(number_of_preferences,int(0.5*number_of_voters))
    preference_matrix = np.append(same_preference_half,random_preference_half,axis=1)
    
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

#plt.plot(x_data, total_happiness_borda)
#plt.plot(x_data, total_happiness_plurality)
#plt.plot(x_data, total_happiness_voting_for_two)
#plt.plot(x_data, total_happiness_antiplurality)
#plt.show()

print("average borda happiness", np.average(total_happiness_borda))
print("average pplurallity happiness",np.average(total_happiness_plurality))
print("average voting for two happiness",np.average(total_happiness_voting_for_two))
print("average antiplurality happiness",np.average(total_happiness_antiplurality))

print("Standard deviation borda happiness", np.std(total_happiness_borda))
print("Standard deviation pplurallity happiness",np.std(total_happiness_plurality))
print("Standard deviation voting for two happiness",np.std(total_happiness_voting_for_two))
print("Standard deviation antiplurality happiness",np.std(total_happiness_antiplurality))

for i in range(number_of_experiments):
    random_preference_half = gen_random_preference_matrix(number_of_preferences,int(0.5*number_of_voters))
    preference_matrix = np.append(same_preference_half,random_preference_half,axis=1)
    selfish_voter_index = choose_strategic_voter(preference_matrix,)




    



