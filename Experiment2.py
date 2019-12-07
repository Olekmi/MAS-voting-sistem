#This experiment investigates what would happen if 50% of the voters have the same 
#preferences while the other half have random preferences
#We will have 4 scenarios:
###### Selfish agent
###### Altruistic agent
###### Agent among Majority
###### Agent among Minority

import numpy as np
import voting_schemes as vs
from mas_assignment_1 import  gen_random_preference_matrix, generate_fixed_pref_matrix, calculate_happiness, tactical_voter
from mas_assignment_1 import  choose_strategic_voter, risk_calculate, calculate_outcome, bullet_voting, Compromising
import matplotlib.pyplot as plt
import time
import scipy.stats as stats
import math


number_of_preferences = 5
number_of_voters = 10
number_of_experiments = 100
same_preference_half = generate_fixed_pref_matrix(number_of_preferences,0.5*number_of_voters)


total_happiness_borda = np.zeros(number_of_experiments)
total_happiness_plurality =  np.zeros(number_of_experiments)
total_happiness_voting_for_two =  np.zeros(number_of_experiments)
total_happiness_antiplurality =  np.zeros(number_of_experiments)

start_time_honnest_assessment = time.time()

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
    
print("Done calculating happiness without strategic voting")
x_data = np.zeros(number_of_experiments)
for i in range(number_of_experiments):
    x_data[i] = i

#plt.plot(x_data, total_happiness_borda,label="borda")
#plt.plot(x_data, total_happiness_plurality, label = "plurality")
#plt.plot(x_data, total_happiness_voting_for_two, label = "voting for two")
#plt.plot(x_data, total_happiness_antiplurality, label = "antiplurality")



#plt.hist(total_happiness_plurality)

#plt.legend()
#plt.show()

stop_watch = time.time() - start_time_honnest_assessment 

print("average honnest borda happiness", np.average(total_happiness_borda))
print("average honnest plurallity happiness",np.average(total_happiness_plurality))
print("average honnest voting for two happiness",np.average(total_happiness_voting_for_two))
print("average honnest antiplurality happiness",np.average(total_happiness_antiplurality))
print()
print("Standard deviation honnest borda happiness", np.std(total_happiness_borda))
print("Standard deviation honnest plurallity happiness",np.std(total_happiness_plurality))
print("Standard deviation honnest voting for two happiness",np.std(total_happiness_voting_for_two))
print("Standard deviation honnest antiplurality happiness",np.std(total_happiness_antiplurality))
print("Honnest happiness assessed after {duration_start:.3f} s".format(duration_start = stop_watch))



def moving_average(data_set, periods):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')

window_moving_average = 10
x_data_ma = np.zeros(number_of_experiments - window_moving_average+1)
for i in range(number_of_experiments - window_moving_average+1):
    x_data_ma[i] = i

#######################################
####### BEGINNING SCENARIO 1 ##########
####### SELFISH AGENT        ##########
#######################################

def experiment_selfish_agent():
    start_experiment = time.time()
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
    
    count_none_borda = 0
    count_none_vote_two = 0
    count_none_antiplurality = 0
    count_none_plurality = 0
    
    
    agent_behavior = "selfish"
    
    for i in range(number_of_experiments):
        random_preference_half = gen_random_preference_matrix(number_of_preferences,int(0.5*number_of_voters))
        preference_matrix = np.append(same_preference_half,random_preference_half,axis=1)
        
        borda_tactical_voter_index,borda_agent_type = choose_strategic_voter(preference_matrix,"borda",agent_behavior)
        _, overall_happiness_borda, _, _ = tactical_voter("borda",preference_matrix,borda_tactical_voter_index)
        selfish_total_happiness_borda[i] = overall_happiness_borda
        difference_selfish_total_happiness_borda[i] = overall_happiness_borda - total_happiness_borda[i]
        average_difference_selfish_total_happiness_borda[i] = overall_happiness_borda - np.average(total_happiness_borda)
        if(borda_agent_type == "none"):
            count_none_borda += 1
        
        
        vote_two_tactical_voter_index,vote_two_agent_type = choose_strategic_voter(preference_matrix,"vote2",agent_behavior)
        _, overall_happiness_vote_two, _, _ = tactical_voter("vote2",preference_matrix,borda_tactical_voter_index)
        selfish_total_happiness_voting_for_two[i] = overall_happiness_vote_two
        difference_selfish_total_happiness_voting_for_two[i] = overall_happiness_vote_two - total_happiness_voting_for_two[i]
        average_difference_selfish_total_happiness_voting_for_two[i] = overall_happiness_vote_two - np.average(total_happiness_voting_for_two)
        if(vote_two_agent_type == "none"):
            count_none_vote_two += 1
        
        antiplurality_tactical_voter_index,antiplurality_agent_type = choose_strategic_voter(preference_matrix,"anti_plurality",agent_behavior)
        _, overall_happiness_antiplurality, _, _ = tactical_voter("anti_plurality",preference_matrix,borda_tactical_voter_index)
        selfish_total_happiness_antiplurality[i] = overall_happiness_antiplurality
        difference_selfish_total_happiness_plurality[i] = overall_happiness_antiplurality - total_happiness_antiplurality[i]
        average_difference_selfish_total_happiness_antiplurality[i] = overall_happiness_antiplurality - np.average(total_happiness_antiplurality)
        if(antiplurality_agent_type == "none"):
            count_none_antiplurality += 1
        
        
        plurality_tactical_voter_index,plurality_agent_type = choose_strategic_voter(preference_matrix,"plurality",agent_behavior)
        _, overall_happiness_plurality, _, _ = tactical_voter("plurality",preference_matrix,borda_tactical_voter_index)
        selfish_total_happiness_plurality[i] = overall_happiness_plurality
        difference_selfish_total_happiness_plurality[i] = overall_happiness_plurality - total_happiness_plurality[i]
        average_difference_selfish_total_happiness_plurality[i] = overall_happiness_plurality - np.average(total_happiness_plurality)
        if(plurality_agent_type == "none"):
            count_none_plurality += 1
            
            
    mu_diff_selfish_total_happiness_borda = np.average(difference_selfish_total_happiness_borda)
    var_diff_selfish_total_happiness_borda = np.var(difference_selfish_total_happiness_borda)
    sigma_diff_selfish_total_happiness_borda = math.sqrt(var_diff_selfish_total_happiness_borda)
    x_diff_selfish_total_happiness_borda = np.linspace(mu_diff_selfish_total_happiness_borda - 3*sigma_diff_selfish_total_happiness_borda, mu_diff_selfish_total_happiness_borda + 3*sigma_diff_selfish_total_happiness_borda, number_of_experiments)
    
    mu_diff_selfish_total_happiness_plurality = np.average(difference_selfish_total_happiness_plurality)
    var_diff_selfish_total_happiness_plurality = np.var(difference_selfish_total_happiness_plurality)
    sigma_diff_selfish_total_happiness_plurality = math.sqrt(var_diff_selfish_total_happiness_plurality)
    x_diff_selfish_total_happiness_plurality = np.linspace(mu_diff_selfish_total_happiness_plurality - 3*sigma_diff_selfish_total_happiness_plurality, mu_diff_selfish_total_happiness_plurality + 3*sigma_diff_selfish_total_happiness_plurality, number_of_experiments)

    mu_diff_selfish_total_happiness_voting_for_two = np.average(difference_selfish_total_happiness_voting_for_two)
    var_diff_selfish_total_happiness_voting_for_two = np.var(difference_selfish_total_happiness_voting_for_two)
    sigma_diff_selfish_total_happiness_voting_for_two = math.sqrt(var_diff_selfish_total_happiness_voting_for_two)
    x_diff_selfish_total_happiness_voting_for_two = np.linspace(mu_diff_selfish_total_happiness_voting_for_two - 3*sigma_diff_selfish_total_happiness_voting_for_two, mu_diff_selfish_total_happiness_voting_for_two + 3*sigma_diff_selfish_total_happiness_voting_for_two, number_of_experiments)

    mu_diff_selfish_total_happiness_antiplurality = np.average(difference_selfish_total_happiness_antiplurality)
    var_diff_selfish_total_happiness_antiplurality = np.var(difference_selfish_total_happiness_antiplurality)
    sigma_diff_selfish_total_happiness_antiplurality = math.sqrt(var_diff_selfish_total_happiness_antiplurality)
    x_diff_selfish_total_happiness_antiplurality = np.linspace(mu_diff_selfish_total_happiness_antiplurality - 3* sigma_diff_selfish_total_happiness_antiplurality, mu_diff_selfish_total_happiness_antiplurality + 3*sigma_diff_selfish_total_happiness_antiplurality, number_of_experiments)


    plt.figure(figsize=(10,10))
#    plt.subplot(2, 1, 1)
    plt.plot(x_diff_selfish_total_happiness_borda, stats.norm.pdf(x_diff_selfish_total_happiness_borda, mu_diff_selfish_total_happiness_borda, sigma_diff_selfish_total_happiness_borda),label="borda, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_selfish_total_happiness_borda) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_selfish_total_happiness_borda))
    plt.plot(x_diff_selfish_total_happiness_plurality, stats.norm.pdf(x_diff_selfish_total_happiness_plurality, mu_diff_selfish_total_happiness_plurality, sigma_diff_selfish_total_happiness_plurality),label="plurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_selfish_total_happiness_plurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_selfish_total_happiness_plurality))
    plt.plot(x_diff_selfish_total_happiness_voting_for_two, stats.norm.pdf(x_diff_selfish_total_happiness_voting_for_two, mu_diff_selfish_total_happiness_voting_for_two, sigma_diff_selfish_total_happiness_voting_for_two), label = "vote2, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_selfish_total_happiness_voting_for_two) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_selfish_total_happiness_voting_for_two))
    plt.plot(x_diff_selfish_total_happiness_antiplurality, stats.norm.pdf(x_diff_selfish_total_happiness_antiplurality, mu_diff_selfish_total_happiness_antiplurality, sigma_diff_selfish_total_happiness_antiplurality), label = "antiplurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_selfish_total_happiness_antiplurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_selfish_total_happiness_antiplurality))


    plt.legend(fontsize='small')
    plt.title("Distribution of the change in overall happiness \nafter strategic voting when a strategic voter is a selfish agent")
    plt.xlabel("Change in overall happiness")
    plt.ylabel("Probability of the change")
#    
#    
#    
#    plt.subplot(2,1,2)    
    mu_avg_diff_selfish_tot_borda = np.average(average_difference_selfish_total_happiness_borda)
    var_avg_diff_selfish_tot_borda = np.var(average_difference_selfish_total_happiness_borda)
    sigma_avg_diff_selfish_tot_borda = math.sqrt(var_avg_diff_selfish_tot_borda)
    x_avg_diff_selfish_tot_borda = np.linspace(mu_avg_diff_selfish_tot_borda - 3*sigma_avg_diff_selfish_tot_borda, mu_avg_diff_selfish_tot_borda + 3*sigma_avg_diff_selfish_tot_borda, number_of_experiments)
    
    mu_avg_diff_selfish_tot_plurality = np.average(average_difference_selfish_total_happiness_plurality)
    var_avg_diff_selfish_tot_plurality = np.var(average_difference_selfish_total_happiness_plurality)
    sigma_avg_diff_selfish_tot_plurality = math.sqrt(var_avg_diff_selfish_tot_plurality)
    x_avg_diff_selfish_tot_plurality = np.linspace(mu_avg_diff_selfish_tot_plurality - 3*sigma_avg_diff_selfish_tot_plurality, mu_avg_diff_selfish_tot_plurality + 3*sigma_avg_diff_selfish_tot_plurality, number_of_experiments)

    mu_avg_diff_selfish_tot_voting_for_two = np.average(average_difference_selfish_total_happiness_plurality)
    var_avg_diff_selfish_tot_voting_for_two = np.var(average_difference_selfish_total_happiness_plurality)
    sigma_avg_diff_selfish_tot_voting_for_two = math.sqrt(var_avg_diff_selfish_tot_voting_for_two)
    x_avg_diff_selfish_tot_voting_for_two = np.linspace(mu_avg_diff_selfish_tot_voting_for_two - 3*sigma_avg_diff_selfish_tot_voting_for_two, mu_avg_diff_selfish_tot_voting_for_two + 3*sigma_avg_diff_selfish_tot_voting_for_two, number_of_experiments)

    mu_avg_diff_selfish_tot_antiplurality = np.average(average_difference_selfish_total_happiness_antiplurality)
    var_avg_diff_selfish_tot_antiplurality = np.var(average_difference_selfish_total_happiness_antiplurality)
    sigma_avg_diff_selfish_tot_antiplurality = math.sqrt(var_avg_diff_selfish_tot_antiplurality)
    x_avg_diff_selfish_tot_antiplurality = np.linspace(mu_avg_diff_selfish_tot_antiplurality - 3* sigma_avg_diff_selfish_tot_antiplurality, mu_avg_diff_selfish_tot_antiplurality + 3*sigma_avg_diff_selfish_tot_antiplurality, number_of_experiments)
    
    
#    plt.plot(x_avg_diff_selfish_tot_borda, stats.norm.pdf(x_avg_diff_selfish_tot_borda, mu_avg_diff_selfish_tot_borda, sigma_avg_diff_selfish_tot_borda),label="borda, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_selfish_total_happiness_borda) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_selfish_tot_borda))
#    plt.plot(x_avg_diff_selfish_tot_plurality, stats.norm.pdf(x_avg_diff_selfish_tot_plurality, mu_avg_diff_selfish_tot_plurality, sigma_avg_diff_selfish_tot_plurality),label="plurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_selfish_tot_plurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_selfish_tot_plurality))
#    plt.plot(x_avg_diff_selfish_tot_voting_for_two, stats.norm.pdf(x_avg_diff_selfish_tot_voting_for_two, mu_avg_diff_selfish_tot_voting_for_two, sigma_avg_diff_selfish_tot_voting_for_two), label = "vote2, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_selfish_tot_voting_for_two) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_selfish_tot_voting_for_two))
#    plt.plot(x_avg_diff_selfish_tot_antiplurality, stats.norm.pdf(x_avg_diff_selfish_tot_antiplurality, mu_avg_diff_selfish_tot_antiplurality, sigma_avg_diff_selfish_tot_antiplurality), label = "antiplurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_selfish_tot_antiplurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_selfish_tot_antiplurality))
#    
#    plt.legend(fontsize='small')
#    plt.title("Distribution of the difference of overall happiness from the average honest\nhappiness after strategic voting when a strategic voter is a selfish agent")
#    plt.xlabel("Change in the difference from the average honest happiness")
#    plt.ylabel("Probability of the change from the average honest happiness")
    plt.savefig("selfish_exp2_"+str(number_of_experiments)+".jpg")
    plt.show()
        
#    ma_diff_selfish_total_happiness_borda = moving_average(difference_selfish_total_happiness_borda, window_moving_average)
#    ma_diff_selfish_total_happiness_plurality = moving_average(difference_selfish_total_happiness_plurality, window_moving_average)
#    ma_diff_selfish_total_happiness_voting_for_two = moving_average(difference_selfish_total_happiness_voting_for_two, window_moving_average)
#    ma_diff_selfish_total_happiness_antiplurality = moving_average(difference_selfish_total_happiness_antiplurality, window_moving_average)
        
    
#    plt.figure(figsize=(10,15))
#    plt.subplot(2, 1, 1)
#    plt.plot(x_data_ma, ma_diff_selfish_total_happiness_borda,label="borda")
#    plt.plot(x_data_ma, ma_diff_selfish_total_happiness_plurality, label = "plurality")
#    plt.plot(x_data_ma, ma_diff_selfish_total_happiness_voting_for_two, label = "voting for two")
#    plt.plot(x_data_ma, ma_diff_selfish_total_happiness_antiplurality, label = "antiplurality")
#
#    plt.legend(fontsize='small')
#    plt.title("Difference of overall happiness after strategic voting \nwhen a strategic voter is a selfish agent")
#    plt.xlabel("Iterations")
#    plt.ylabel("Difference in overall happiness")
#    
#    
#    
#    plt.subplot(2,1,2)    
#    ma_avg_diff_selfish_total_happiness_borda = moving_average(average_difference_selfish_total_happiness_borda,window_moving_average)
#    ma_avg_diff_selfish_total_happiness_plurality = moving_average(average_difference_selfish_total_happiness_plurality,window_moving_average)
#    ma_avg_diff_selfish_total_happiness_voting_for_two = moving_average(average_difference_selfish_total_happiness_voting_for_two,window_moving_average)
#    ma_avg_diff_selfish_total_happiness_antiplurality = moving_average(average_difference_selfish_total_happiness_antiplurality,window_moving_average)
#
#    plt.plot(x_data_ma,ma_avg_diff_selfish_total_happiness_borda,label="borda")
#    plt.plot(x_data_ma,ma_avg_diff_selfish_total_happiness_plurality,label="plurality")
#    plt.plot(x_data_ma,ma_avg_diff_selfish_total_happiness_voting_for_two,label="voting for two")
#    plt.plot(x_data_ma,ma_avg_diff_selfish_total_happiness_antiplurality,label="antiplurality")
#
#    plt.legend(fontsize='small')
#    plt.title("Difference of overall happiness from the average happiness after strategic voting \nwhen a strategic voter is a selfish agent")
#    plt.xlabel("Iterations")
#    plt.ylabel("Difference in overall happiness from average happiness")
#    plt.show()
    duration_experiment = time.time() - start_experiment 
    print("Percentage of none agents for borda voting scheme",count_none_borda/number_of_experiments)
    print("Percentage of none agents for plurality voting scheme",count_none_plurality/number_of_experiments)
    print("Percentage of none agents for voting for two voting scheme",count_none_vote_two/number_of_experiments)
    print("Percentage of none agents for antiplurality voting scheme",count_none_antiplurality/number_of_experiments)
    print("Experiment about selfish agent done after {duration:.3f} s".format(duration = duration_experiment))
    
##################################
#### END PART SELFISH AGENT ######
##################################


#######################################
####### BEGINNING SCENARIO 2 ##########
####### ALTRUISTIC AGENT     ##########
#######################################
    
def experiment_altruistic_agent():
    start_experiment = time.time()
    altruistic_total_happiness_borda = np.zeros(number_of_experiments)
    altruistic_total_happiness_plurality =  np.zeros(number_of_experiments)
    altruistic_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    altruistic_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    
    difference_altruistic_total_happiness_borda = np.zeros(number_of_experiments)
    difference_altruistic_total_happiness_plurality =  np.zeros(number_of_experiments)
    difference_altruistic_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    difference_altruistic_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    average_difference_altruistic_total_happiness_borda = np.zeros(number_of_experiments)
    average_difference_altruistic_total_happiness_plurality =  np.zeros(number_of_experiments)
    average_difference_altruistic_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    average_difference_altruistic_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    count_none_borda = 0
    count_none_vote_two = 0
    count_none_antiplurality = 0
    count_none_plurality = 0
    
    agent_behavior = "altruistic"
    
    for i in range(number_of_experiments):
        random_preference_half = gen_random_preference_matrix(number_of_preferences,int(0.5*number_of_voters))
        preference_matrix = np.append(same_preference_half,random_preference_half,axis=1)
        
        borda_tactical_voter_index,borda_agent_type = choose_strategic_voter(preference_matrix,"borda",agent_behavior)
        _, overall_happiness_borda, _, _ = tactical_voter("borda",preference_matrix,borda_tactical_voter_index)
        altruistic_total_happiness_borda[i] = overall_happiness_borda
        difference_altruistic_total_happiness_borda[i] = overall_happiness_borda - total_happiness_borda[i]
        average_difference_altruistic_total_happiness_borda[i] = overall_happiness_borda - np.average(total_happiness_borda)
        if(borda_agent_type == "none"):
            count_none_borda += 1
        
        
        vote_two_tactical_voter_index,vote_two_agent_type = choose_strategic_voter(preference_matrix,"vote2",agent_behavior)
        _, overall_happiness_vote_two, _, _ = tactical_voter("vote2",preference_matrix,borda_tactical_voter_index)
        altruistic_total_happiness_voting_for_two[i] = overall_happiness_vote_two
        difference_altruistic_total_happiness_voting_for_two[i] = overall_happiness_vote_two - total_happiness_voting_for_two[i]
        average_difference_altruistic_total_happiness_voting_for_two[i] = overall_happiness_vote_two - np.average(total_happiness_voting_for_two)
        if(vote_two_agent_type == "none"):
            count_none_vote_two += 1
        
        antiplurality_tactical_voter_index,antiplurality_agent_type = choose_strategic_voter(preference_matrix,"anti_plurality",agent_behavior)
        _, overall_happiness_antiplurality, _, _ = tactical_voter("anti_plurality",preference_matrix,borda_tactical_voter_index)
        altruistic_total_happiness_antiplurality[i] = overall_happiness_antiplurality
        difference_altruistic_total_happiness_plurality[i] = overall_happiness_antiplurality - total_happiness_antiplurality[i]
        average_difference_altruistic_total_happiness_antiplurality[i] = overall_happiness_antiplurality - np.average(total_happiness_antiplurality)
        if(antiplurality_agent_type == "none"):
            count_none_antiplurality += 1
        
        
        plurality_tactical_voter_index,plurality_agent_type = choose_strategic_voter(preference_matrix,"plurality",agent_behavior)
        _, overall_happiness_plurality, _, _ = tactical_voter("plurality",preference_matrix,borda_tactical_voter_index)
        altruistic_total_happiness_plurality[i] = overall_happiness_plurality
        difference_altruistic_total_happiness_plurality[i] = overall_happiness_plurality - total_happiness_plurality[i]
        average_difference_altruistic_total_happiness_plurality[i] = overall_happiness_plurality - np.average(total_happiness_plurality)
        if(plurality_agent_type == "none"):
            count_none_plurality += 1
            
    mu_diff_altruistic_total_happiness_borda = np.average(difference_altruistic_total_happiness_borda)
    var_diff_altruistic_total_happiness_borda = np.var(difference_altruistic_total_happiness_borda)
    sigma_diff_altruistic_total_happiness_borda = math.sqrt(var_diff_altruistic_total_happiness_borda)
    x_diff_altruistic_total_happiness_borda = np.linspace(mu_diff_altruistic_total_happiness_borda - 3*sigma_diff_altruistic_total_happiness_borda, mu_diff_altruistic_total_happiness_borda + 3*sigma_diff_altruistic_total_happiness_borda, number_of_experiments)
    
    mu_diff_altruistic_total_happiness_plurality = np.average(difference_altruistic_total_happiness_plurality)
    var_diff_altruistic_total_happiness_plurality = np.var(difference_altruistic_total_happiness_plurality)
    sigma_diff_altruistic_total_happiness_plurality = math.sqrt(var_diff_altruistic_total_happiness_plurality)
    x_diff_altruistic_total_happiness_plurality = np.linspace(mu_diff_altruistic_total_happiness_plurality - 3*sigma_diff_altruistic_total_happiness_plurality, mu_diff_altruistic_total_happiness_plurality + 3*sigma_diff_altruistic_total_happiness_plurality, number_of_experiments)

    mu_diff_altruistic_total_happiness_voting_for_two = np.average(difference_altruistic_total_happiness_voting_for_two)
    var_diff_altruistic_total_happiness_voting_for_two = np.var(difference_altruistic_total_happiness_voting_for_two)
    sigma_diff_altruistic_total_happiness_voting_for_two = math.sqrt(var_diff_altruistic_total_happiness_voting_for_two)
    x_diff_altruistic_total_happiness_voting_for_two = np.linspace(mu_diff_altruistic_total_happiness_voting_for_two - 3*sigma_diff_altruistic_total_happiness_voting_for_two, mu_diff_altruistic_total_happiness_voting_for_two + 3*sigma_diff_altruistic_total_happiness_voting_for_two, number_of_experiments)

    mu_diff_altruistic_total_happiness_antiplurality = np.average(difference_altruistic_total_happiness_antiplurality)
    var_diff_altruistic_total_happiness_antiplurality = np.var(difference_altruistic_total_happiness_antiplurality)
    sigma_diff_altruistic_total_happiness_antiplurality = math.sqrt(var_diff_altruistic_total_happiness_antiplurality)
    x_diff_altruistic_total_happiness_antiplurality = np.linspace(mu_diff_altruistic_total_happiness_antiplurality - 3* sigma_diff_altruistic_total_happiness_antiplurality, mu_diff_altruistic_total_happiness_antiplurality + 3*sigma_diff_altruistic_total_happiness_antiplurality, number_of_experiments)


    plt.figure(figsize=(10,10))
#    plt.subplot(2, 1, 1)
    plt.plot(x_diff_altruistic_total_happiness_borda, stats.norm.pdf(x_diff_altruistic_total_happiness_borda, mu_diff_altruistic_total_happiness_borda, sigma_diff_altruistic_total_happiness_borda),label="borda, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_altruistic_total_happiness_borda) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_altruistic_total_happiness_borda))
    plt.plot(x_diff_altruistic_total_happiness_plurality, stats.norm.pdf(x_diff_altruistic_total_happiness_plurality, mu_diff_altruistic_total_happiness_plurality, sigma_diff_altruistic_total_happiness_plurality),label="plurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_altruistic_total_happiness_plurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_altruistic_total_happiness_plurality))
    plt.plot(x_diff_altruistic_total_happiness_voting_for_two, stats.norm.pdf(x_diff_altruistic_total_happiness_voting_for_two, mu_diff_altruistic_total_happiness_voting_for_two, sigma_diff_altruistic_total_happiness_voting_for_two), label = "vote2, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_altruistic_total_happiness_voting_for_two) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_altruistic_total_happiness_voting_for_two))
    plt.plot(x_diff_altruistic_total_happiness_antiplurality, stats.norm.pdf(x_diff_altruistic_total_happiness_antiplurality, mu_diff_altruistic_total_happiness_antiplurality, sigma_diff_altruistic_total_happiness_antiplurality), label = "antiplurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_altruistic_total_happiness_antiplurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_altruistic_total_happiness_antiplurality))


    plt.legend(fontsize='small')
    plt.title("Distribution of the change in overall happiness \nafter strategic voting when a strategic voter is an altruistic agent")
    plt.xlabel("Change in overall happiness")
    plt.ylabel("Probability of the change")
#    
#    
#    
#    plt.subplot(2,1,2)    
    mu_avg_diff_altruistic_tot_borda = np.average(average_difference_altruistic_total_happiness_borda)
    var_avg_diff_altruistic_tot_borda = np.var(average_difference_altruistic_total_happiness_borda)
    sigma_avg_diff_altruistic_tot_borda = math.sqrt(var_avg_diff_altruistic_tot_borda)
    x_avg_diff_altruistic_tot_borda = np.linspace(mu_avg_diff_altruistic_tot_borda - 3*sigma_avg_diff_altruistic_tot_borda, mu_avg_diff_altruistic_tot_borda + 3*sigma_avg_diff_altruistic_tot_borda, number_of_experiments)
    
    mu_avg_diff_altruistic_tot_plurality = np.average(average_difference_altruistic_total_happiness_plurality)
    var_avg_diff_altruistic_tot_plurality = np.var(average_difference_altruistic_total_happiness_plurality)
    sigma_avg_diff_altruistic_tot_plurality = math.sqrt(var_avg_diff_altruistic_tot_plurality)
    x_avg_diff_altruistic_tot_plurality = np.linspace(mu_avg_diff_altruistic_tot_plurality - 3*sigma_avg_diff_altruistic_tot_plurality, mu_avg_diff_altruistic_tot_plurality + 3*sigma_avg_diff_altruistic_tot_plurality, number_of_experiments)

    mu_avg_diff_altruistic_tot_voting_for_two = np.average(average_difference_altruistic_total_happiness_plurality)
    var_avg_diff_altruistic_tot_voting_for_two = np.var(average_difference_altruistic_total_happiness_plurality)
    sigma_avg_diff_altruistic_tot_voting_for_two = math.sqrt(var_avg_diff_altruistic_tot_voting_for_two)
    x_avg_diff_altruistic_tot_voting_for_two = np.linspace(mu_avg_diff_altruistic_tot_voting_for_two - 3*sigma_avg_diff_altruistic_tot_voting_for_two, mu_avg_diff_altruistic_tot_voting_for_two + 3*sigma_avg_diff_altruistic_tot_voting_for_two, number_of_experiments)

    mu_avg_diff_altruistic_tot_antiplurality = np.average(average_difference_altruistic_total_happiness_antiplurality)
    var_avg_diff_altruistic_tot_antiplurality = np.var(average_difference_altruistic_total_happiness_antiplurality)
    sigma_avg_diff_altruistic_tot_antiplurality = math.sqrt(var_avg_diff_altruistic_tot_antiplurality)
    x_avg_diff_altruistic_tot_antiplurality = np.linspace(mu_avg_diff_altruistic_tot_antiplurality - 3* sigma_avg_diff_altruistic_tot_antiplurality, mu_avg_diff_altruistic_tot_antiplurality + 3*sigma_avg_diff_altruistic_tot_antiplurality, number_of_experiments)
    
    
#    plt.plot(x_avg_diff_altruistic_tot_borda, stats.norm.pdf(x_avg_diff_altruistic_tot_borda, mu_avg_diff_altruistic_tot_borda, sigma_avg_diff_altruistic_tot_borda),label="borda, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_altruistic_total_happiness_borda) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_altruistic_tot_borda))
#    plt.plot(x_avg_diff_altruistic_tot_plurality, stats.norm.pdf(x_avg_diff_altruistic_tot_plurality, mu_avg_diff_altruistic_tot_plurality, sigma_avg_diff_altruistic_tot_plurality),label="plurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_altruistic_tot_plurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_altruistic_tot_plurality))
#    plt.plot(x_avg_diff_altruistic_tot_voting_for_two, stats.norm.pdf(x_avg_diff_altruistic_tot_voting_for_two, mu_avg_diff_altruistic_tot_voting_for_two, sigma_avg_diff_altruistic_tot_voting_for_two), label = "vote2, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_altruistic_tot_voting_for_two) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_altruistic_tot_voting_for_two))
#    plt.plot(x_avg_diff_altruistic_tot_antiplurality, stats.norm.pdf(x_avg_diff_altruistic_tot_antiplurality, mu_avg_diff_altruistic_tot_antiplurality, sigma_avg_diff_altruistic_tot_antiplurality), label = "antiplurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_altruistic_tot_antiplurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_altruistic_tot_antiplurality))
#    
#    plt.legend(fontsize='small')
#    plt.title("Distribution of the difference of overall happiness from the average honest\nhappiness after strategic voting when a strategic voter is an altruistic agent")
#    plt.xlabel("Change in the difference from the average honest happiness")
#    plt.ylabel("Probability of the change from the average honest happiness")
    plt.savefig("altruistic_exp2_"+str(number_of_experiments)+".jpg")
    plt.show()
    
    
    
    duration_experiment = time.time() - start_experiment 
    print("Percentage of none agents for borda voting scheme",count_none_borda/number_of_experiments)
    print("Percentage of none agents for plurality voting scheme",count_none_plurality/number_of_experiments)
    print("Percentage of none agents for voting for two voting scheme",count_none_vote_two/number_of_experiments)
    print("Percentage of none agents for antiplurality voting scheme",count_none_antiplurality/number_of_experiments)
    print("Experiment about altruistic agent done after {duration:.3f} s".format(duration = duration_experiment))
    
    #    ma_diff_altruistic_total_happiness_borda = moving_average(difference_altruistic_total_happiness_borda, window_moving_average)
#    ma_diff_altruistic_total_happiness_plurality = moving_average(difference_altruistic_total_happiness_plurality, window_moving_average)
#    ma_diff_altruistic_total_happiness_voting_for_two = moving_average(difference_altruistic_total_happiness_voting_for_two, window_moving_average)
#    ma_diff_altruistic_total_happiness_antiplurality = moving_average(difference_altruistic_total_happiness_antiplurality, window_moving_average)
#   
#    
#    plt.figure(figsize=(10,15))
#    plt.subplot(2, 1, 1)
#    plt.plot(x_data_ma, ma_diff_altruistic_total_happiness_borda,label="borda")
#    plt.plot(x_data_ma, ma_diff_altruistic_total_happiness_plurality, label = "plurality")
#    plt.plot(x_data_ma, ma_diff_altruistic_total_happiness_voting_for_two, label = "voting for two")
#    plt.plot(x_data_ma, ma_diff_altruistic_total_happiness_antiplurality, label = "antiplurality")
    
#    ma_avg_diff_altruistic_total_happiness_borda = moving_average(average_difference_altruistic_total_happiness_borda,window_moving_average)
#    ma_avg_diff_altruistic_total_happiness_plurality = moving_average(average_difference_altruistic_total_happiness_plurality,window_moving_average)
#    ma_avg_diff_altruistic_total_happiness_voting_for_two = moving_average(average_difference_altruistic_total_happiness_voting_for_two,window_moving_average)
#    ma_avg_diff_altruistic_total_happiness_antiplurality = moving_average(average_difference_altruistic_total_happiness_antiplurality,window_moving_average)
#
#    plt.plot(x_data_ma,ma_avg_diff_altruistic_total_happiness_borda,label="borda")
#    plt.plot(x_data_ma,ma_avg_diff_altruistic_total_happiness_plurality,label="plurality")
#    plt.plot(x_data_ma,ma_avg_diff_altruistic_total_happiness_voting_for_two,label="voting for two")
#    plt.plot(x_data_ma,ma_avg_diff_altruistic_total_happiness_antiplurality,label="antiplurality")
#
    

#####################################
#### END PART ALTRUISTIC AGENT ######
#####################################

#######################################
####### BEGINNING SCENARIO 3 ##########
####### MAJORITY AGENT       ##########
#######################################
    
def experiment_majority_agent():
    start_experiment = time.time()
    majority_total_happiness_borda = np.zeros(number_of_experiments)
    majority_total_happiness_plurality =  np.zeros(number_of_experiments)
    majority_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    majority_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    
    difference_majority_total_happiness_borda = np.zeros(number_of_experiments)
    difference_majority_total_happiness_plurality =  np.zeros(number_of_experiments)
    difference_majority_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    difference_majority_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    average_difference_majority_total_happiness_borda = np.zeros(number_of_experiments)
    average_difference_majority_total_happiness_plurality =  np.zeros(number_of_experiments)
    average_difference_majority_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    average_difference_majority_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    majority_voter_index = 0
    
    for i in range(number_of_experiments):
        random_preference_half = gen_random_preference_matrix(number_of_preferences,int(0.5*number_of_voters))
        preference_matrix = np.append(same_preference_half,random_preference_half,axis=1)
    
        
            
        _, overall_happiness_borda, _, _ = tactical_voter("borda",preference_matrix,majority_voter_index)
        majority_total_happiness_borda[i] = overall_happiness_borda
        difference_majority_total_happiness_borda[i] = overall_happiness_borda - total_happiness_borda[i]
        average_difference_majority_total_happiness_borda[i] = overall_happiness_borda - np.average(total_happiness_borda)
    
        
        
        _, overall_happiness_vote_two, _, _ = tactical_voter("vote2",preference_matrix,majority_voter_index)
        majority_total_happiness_voting_for_two[i] = overall_happiness_vote_two
        difference_majority_total_happiness_voting_for_two[i] = overall_happiness_vote_two - total_happiness_voting_for_two[i]
        average_difference_majority_total_happiness_voting_for_two[i] = overall_happiness_vote_two - np.average(total_happiness_voting_for_two)
    
        
        _, overall_happiness_antiplurality, _, _ = tactical_voter("anti_plurality",preference_matrix,majority_voter_index)
        majority_total_happiness_antiplurality[i] = overall_happiness_antiplurality
        difference_majority_total_happiness_plurality[i] = overall_happiness_antiplurality - total_happiness_antiplurality[i]
        average_difference_majority_total_happiness_antiplurality[i] = overall_happiness_antiplurality - np.average(total_happiness_antiplurality)
    
        
        
        _, overall_happiness_plurality, _, _ = tactical_voter("plurality",preference_matrix,majority_voter_index)
        majority_total_happiness_plurality[i] = overall_happiness_plurality
        difference_majority_total_happiness_plurality[i] = overall_happiness_plurality - total_happiness_plurality[i]
        average_difference_majority_total_happiness_plurality[i] = overall_happiness_plurality - np.average(total_happiness_plurality)
 
    mu_diff_majority_total_happiness_borda = np.average(difference_majority_total_happiness_borda)
    var_diff_majority_total_happiness_borda = np.var(difference_majority_total_happiness_borda)
    sigma_diff_majority_total_happiness_borda = math.sqrt(var_diff_majority_total_happiness_borda)
    x_diff_majority_total_happiness_borda = np.linspace(mu_diff_majority_total_happiness_borda - 3*sigma_diff_majority_total_happiness_borda, mu_diff_majority_total_happiness_borda + 3*sigma_diff_majority_total_happiness_borda, number_of_experiments)
    
    mu_diff_majority_total_happiness_plurality = np.average(difference_majority_total_happiness_plurality)
    var_diff_majority_total_happiness_plurality = np.var(difference_majority_total_happiness_plurality)
    sigma_diff_majority_total_happiness_plurality = math.sqrt(var_diff_majority_total_happiness_plurality)
    x_diff_majority_total_happiness_plurality = np.linspace(mu_diff_majority_total_happiness_plurality - 3*sigma_diff_majority_total_happiness_plurality, mu_diff_majority_total_happiness_plurality + 3*sigma_diff_majority_total_happiness_plurality, number_of_experiments)

    mu_diff_majority_total_happiness_voting_for_two = np.average(difference_majority_total_happiness_voting_for_two)
    var_diff_majority_total_happiness_voting_for_two = np.var(difference_majority_total_happiness_voting_for_two)
    sigma_diff_majority_total_happiness_voting_for_two = math.sqrt(var_diff_majority_total_happiness_voting_for_two)
    x_diff_majority_total_happiness_voting_for_two = np.linspace(mu_diff_majority_total_happiness_voting_for_two - 3*sigma_diff_majority_total_happiness_voting_for_two, mu_diff_majority_total_happiness_voting_for_two + 3*sigma_diff_majority_total_happiness_voting_for_two, number_of_experiments)

    mu_diff_majority_total_happiness_antiplurality = np.average(difference_majority_total_happiness_antiplurality)
    var_diff_majority_total_happiness_antiplurality = np.var(difference_majority_total_happiness_antiplurality)
    sigma_diff_majority_total_happiness_antiplurality = math.sqrt(var_diff_majority_total_happiness_antiplurality)
    x_diff_majority_total_happiness_antiplurality = np.linspace(mu_diff_majority_total_happiness_antiplurality - 3* sigma_diff_majority_total_happiness_antiplurality, mu_diff_majority_total_happiness_antiplurality + 3*sigma_diff_majority_total_happiness_antiplurality, number_of_experiments)


    plt.figure(figsize=(10,10))
#    plt.subplot(2, 1, 1)
    plt.plot(x_diff_majority_total_happiness_borda, stats.norm.pdf(x_diff_majority_total_happiness_borda, mu_diff_majority_total_happiness_borda, sigma_diff_majority_total_happiness_borda),label="borda, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_majority_total_happiness_borda) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_majority_total_happiness_borda))
    plt.plot(x_diff_majority_total_happiness_plurality, stats.norm.pdf(x_diff_majority_total_happiness_plurality, mu_diff_majority_total_happiness_plurality, sigma_diff_majority_total_happiness_plurality),label="plurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_majority_total_happiness_plurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_majority_total_happiness_plurality))
    plt.plot(x_diff_majority_total_happiness_voting_for_two, stats.norm.pdf(x_diff_majority_total_happiness_voting_for_two, mu_diff_majority_total_happiness_voting_for_two, sigma_diff_majority_total_happiness_voting_for_two), label = "vote2, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_majority_total_happiness_voting_for_two) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_majority_total_happiness_voting_for_two))
    plt.plot(x_diff_majority_total_happiness_antiplurality, stats.norm.pdf(x_diff_majority_total_happiness_antiplurality, mu_diff_majority_total_happiness_antiplurality, sigma_diff_majority_total_happiness_antiplurality), label = "antiplurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_majority_total_happiness_antiplurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_majority_total_happiness_antiplurality))


    plt.legend(fontsize='small')
    plt.title("Distribution of the change in overall happiness \nafter strategic voting when a strategic voter is part of the majority")
    plt.xlabel("Change in overall happiness")
    plt.ylabel("Probability of the change")
#    
#    
#    
#    plt.subplot(2,1,2)    
    mu_avg_diff_majority_tot_borda = np.average(average_difference_majority_total_happiness_borda)
    var_avg_diff_majority_tot_borda = np.var(average_difference_majority_total_happiness_borda)
    sigma_avg_diff_majority_tot_borda = math.sqrt(var_avg_diff_majority_tot_borda)
    x_avg_diff_majority_tot_borda = np.linspace(mu_avg_diff_majority_tot_borda - 3*sigma_avg_diff_majority_tot_borda, mu_avg_diff_majority_tot_borda + 3*sigma_avg_diff_majority_tot_borda, number_of_experiments)
    
    mu_avg_diff_majority_tot_plurality = np.average(average_difference_majority_total_happiness_plurality)
    var_avg_diff_majority_tot_plurality = np.var(average_difference_majority_total_happiness_plurality)
    sigma_avg_diff_majority_tot_plurality = math.sqrt(var_avg_diff_majority_tot_plurality)
    x_avg_diff_majority_tot_plurality = np.linspace(mu_avg_diff_majority_tot_plurality - 3*sigma_avg_diff_majority_tot_plurality, mu_avg_diff_majority_tot_plurality + 3*sigma_avg_diff_majority_tot_plurality, number_of_experiments)

    mu_avg_diff_majority_tot_voting_for_two = np.average(average_difference_majority_total_happiness_plurality)
    var_avg_diff_majority_tot_voting_for_two = np.var(average_difference_majority_total_happiness_plurality)
    sigma_avg_diff_majority_tot_voting_for_two = math.sqrt(var_avg_diff_majority_tot_voting_for_two)
    x_avg_diff_majority_tot_voting_for_two = np.linspace(mu_avg_diff_majority_tot_voting_for_two - 3*sigma_avg_diff_majority_tot_voting_for_two, mu_avg_diff_majority_tot_voting_for_two + 3*sigma_avg_diff_majority_tot_voting_for_two, number_of_experiments)

    mu_avg_diff_majority_tot_antiplurality = np.average(average_difference_majority_total_happiness_antiplurality)
    var_avg_diff_majority_tot_antiplurality = np.var(average_difference_majority_total_happiness_antiplurality)
    sigma_avg_diff_majority_tot_antiplurality = math.sqrt(var_avg_diff_majority_tot_antiplurality)
    x_avg_diff_majority_tot_antiplurality = np.linspace(mu_avg_diff_majority_tot_antiplurality - 3* sigma_avg_diff_majority_tot_antiplurality, mu_avg_diff_majority_tot_antiplurality + 3*sigma_avg_diff_majority_tot_antiplurality, number_of_experiments)
    
    
#    plt.plot(x_avg_diff_majority_tot_borda, stats.norm.pdf(x_avg_diff_majority_tot_borda, mu_avg_diff_majority_tot_borda, sigma_avg_diff_majority_tot_borda),label="borda, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_majority_total_happiness_borda) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_majority_tot_borda))
#    plt.plot(x_avg_diff_majority_tot_plurality, stats.norm.pdf(x_avg_diff_majority_tot_plurality, mu_avg_diff_majority_tot_plurality, sigma_avg_diff_majority_tot_plurality),label="plurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_majority_tot_plurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_majority_tot_plurality))
#    plt.plot(x_avg_diff_majority_tot_voting_for_two, stats.norm.pdf(x_avg_diff_majority_tot_voting_for_two, mu_avg_diff_majority_tot_voting_for_two, sigma_avg_diff_majority_tot_voting_for_two), label = "vote2, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_majority_tot_voting_for_two) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_majority_tot_voting_for_two))
#    plt.plot(x_avg_diff_majority_tot_antiplurality, stats.norm.pdf(x_avg_diff_majority_tot_antiplurality, mu_avg_diff_majority_tot_antiplurality, sigma_avg_diff_majority_tot_antiplurality), label = "antiplurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_majority_tot_antiplurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_majority_tot_antiplurality))
#    
#    plt.legend(fontsize='small')
#    plt.title("Distribution of the difference of overall happiness from the average honest\nhappiness after strategic voting when a strategic voter is part of the majority")
#    plt.xlabel("Change in the difference from the average honest happiness")
#    plt.ylabel("Probability of the change from the average honest happiness")
    plt.savefig("majority_exp2_"+str(number_of_experiments)+".jpg")
    plt.show()





       
#    ma_diff_majority_total_happiness_borda = moving_average(difference_majority_total_happiness_borda, window_moving_average)
#    ma_diff_majority_total_happiness_plurality = moving_average(difference_majority_total_happiness_plurality, window_moving_average)
#    ma_diff_majority_total_happiness_voting_for_two = moving_average(difference_majority_total_happiness_voting_for_two, window_moving_average)
#    ma_diff_majority_total_happiness_antiplurality = moving_average(difference_majority_total_happiness_antiplurality, window_moving_average)
#        
#    
#    plt.figure(figsize=(10,15))
#    plt.subplot(2, 1, 1)
#    plt.plot(x_data_ma, ma_diff_majority_total_happiness_borda,label="borda")
#    plt.plot(x_data_ma, ma_diff_majority_total_happiness_plurality, label = "plurality")
#    plt.plot(x_data_ma, ma_diff_majority_total_happiness_voting_for_two, label = "voting for two")
#    plt.plot(x_data_ma, ma_diff_majority_total_happiness_antiplurality, label = "antiplurality")
#
#    plt.legend(fontsize='small')
#    plt.title("Difference of overall happiness after strategic voting \nwhen a strategic voter is part of the majority")
#    plt.xlabel("Iterations")
#    plt.ylabel("Difference in overall happiness")
#    
#    
#    
#    plt.subplot(2,1,2)    
#    ma_avg_diff_majority_total_happiness_borda = moving_average(average_difference_majority_total_happiness_borda,window_moving_average)
#    ma_avg_diff_majority_total_happiness_plurality = moving_average(average_difference_majority_total_happiness_plurality,window_moving_average)
#    ma_avg_diff_majority_total_happiness_voting_for_two = moving_average(average_difference_majority_total_happiness_voting_for_two,window_moving_average)
#    ma_avg_diff_majority_total_happiness_antiplurality = moving_average(average_difference_majority_total_happiness_antiplurality,window_moving_average)
#
#    plt.plot(x_data_ma,ma_avg_diff_majority_total_happiness_borda,label="borda")
#    plt.plot(x_data_ma,ma_avg_diff_majority_total_happiness_plurality,label="plurality")
#    plt.plot(x_data_ma,ma_avg_diff_majority_total_happiness_voting_for_two,label="voting for two")
#    plt.plot(x_data_ma,ma_avg_diff_majority_total_happiness_antiplurality,label="antiplurality")
#
#    plt.legend(fontsize='small')
#    plt.title("Difference of overall happiness from the average happiness after strategic voting \nwhen a strategic voter is part of the majority")
#    plt.xlabel("Iterations")
#    plt.ylabel("Difference in overall happiness from average happiness")
#    plt.show()
    duration_experiment = time.time() - start_experiment 
    print("Experiment about majority agent done after {duration:.3f} s".format(duration = duration_experiment))

#####################################
#### END PART MAJORITY AGENT   ######
#####################################



#######################################
####### BEGINNING SCENARIO 4 ##########
####### MINORITY AGENT       ##########
#######################################

def experiment_minority_agent():
    start_experiment = time.time()
    minority_total_happiness_borda = np.zeros(number_of_experiments)
    minority_total_happiness_plurality =  np.zeros(number_of_experiments)
    minority_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    minority_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    
    difference_minority_total_happiness_borda = np.zeros(number_of_experiments)
    difference_minority_total_happiness_plurality =  np.zeros(number_of_experiments)
    difference_minority_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    difference_minority_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    average_difference_minority_total_happiness_borda = np.zeros(number_of_experiments)
    average_difference_minority_total_happiness_plurality =  np.zeros(number_of_experiments)
    average_difference_minority_total_happiness_voting_for_two =  np.zeros(number_of_experiments)
    average_difference_minority_total_happiness_antiplurality =  np.zeros(number_of_experiments)
    
    minority_voter_index = np.random.randint(5,10)
    
    for i in range(number_of_experiments):
        random_preference_half = gen_random_preference_matrix(number_of_preferences,int(0.5*number_of_voters))
        preference_matrix = np.append(same_preference_half,random_preference_half,axis=1)
            
        _, overall_happiness_borda, _, _ = tactical_voter("borda",preference_matrix,minority_voter_index)
        minority_total_happiness_borda[i] = overall_happiness_borda
        difference_minority_total_happiness_borda[i] = overall_happiness_borda - total_happiness_borda[i]
        average_difference_minority_total_happiness_borda[i] = overall_happiness_borda - np.average(total_happiness_borda)
    
        
        
        _, overall_happiness_vote_two, _, _ = tactical_voter("vote2",preference_matrix,minority_voter_index)
        minority_total_happiness_voting_for_two[i] = overall_happiness_vote_two
        difference_minority_total_happiness_voting_for_two[i] = overall_happiness_vote_two - total_happiness_voting_for_two[i]
        average_difference_minority_total_happiness_voting_for_two[i] = overall_happiness_vote_two - np.average(total_happiness_voting_for_two)
    
        
        _, overall_happiness_antiplurality, _, _ = tactical_voter("anti_plurality",preference_matrix,minority_voter_index)
        minority_total_happiness_antiplurality[i] = overall_happiness_antiplurality
        difference_minority_total_happiness_plurality[i] = overall_happiness_antiplurality - total_happiness_antiplurality[i]
        average_difference_minority_total_happiness_antiplurality[i] = overall_happiness_antiplurality - np.average(total_happiness_antiplurality)
    
        
        
        _, overall_happiness_plurality, _, _ = tactical_voter("plurality",preference_matrix,minority_voter_index)
        minority_total_happiness_plurality[i] = overall_happiness_plurality
        difference_minority_total_happiness_plurality[i] = overall_happiness_plurality - total_happiness_plurality[i]
        average_difference_minority_total_happiness_plurality[i] = overall_happiness_plurality - np.average(total_happiness_plurality)
        
    
#    ma_diff_minority_total_happiness_borda = moving_average(difference_minority_total_happiness_borda, window_moving_average)
#    ma_diff_minority_total_happiness_plurality = moving_average(difference_minority_total_happiness_plurality, window_moving_average)
#    ma_diff_minority_total_happiness_voting_for_two = moving_average(difference_minority_total_happiness_voting_for_two, window_moving_average)
#    ma_diff_minority_total_happiness_antiplurality = moving_average(difference_minority_total_happiness_antiplurality, window_moving_average)
#        
#    
#    plt.figure(figsize=(10,15))
#    plt.subplot(2, 1, 1)
##    plt.plot(x_data, difference_minority_total_happiness_borda,label="borda")
##    plt.plot(x_data, difference_minority_total_happiness_plurality, label = "plurality")
##    plt.plot(x_data, difference_minority_total_happiness_voting_for_two, label = "voting for two")
##    plt.plot(x_data, difference_minority_total_happiness_antiplurality, label = "antiplurality")
#    
#    plt.plot(x_data_ma, ma_diff_minority_total_happiness_borda,label="borda")
#    plt.plot(x_data_ma, ma_diff_minority_total_happiness_plurality, label = "plurality")
#    plt.plot(x_data_ma, ma_diff_minority_total_happiness_voting_for_two, label = "voting for two")
#    plt.plot(x_data_ma, ma_diff_minority_total_happiness_antiplurality, label = "antiplurality")
#
#    plt.legend(fontsize='small')
#    plt.title("Difference of overall happiness after strategic voting \nwhen a strategic voter is part of the minority")
#    plt.xlabel("Iterations")
#    plt.ylabel("Difference in overall happiness")
#    
#    
#    
#    plt.subplot(2,1,2)
##    plt.plot(x_data,average_difference_minority_total_happiness_borda,label="borda")
##    plt.plot(x_data,average_difference_minority_total_happiness_plurality,label="plurality")
##    plt.plot(x_data,average_difference_minority_total_happiness_voting_for_two,label="voting for two")
##    plt.plot(x_data,average_difference_minority_total_happiness_antiplurality,label="antiplurality")
#    
#    ma_avg_diff_minority_total_happiness_borda = moving_average(average_difference_minority_total_happiness_borda,window_moving_average)
#    ma_avg_diff_minority_total_happiness_plurality = moving_average(average_difference_minority_total_happiness_plurality,window_moving_average)
#    ma_avg_diff_minority_total_happiness_voting_for_two = moving_average(average_difference_minority_total_happiness_voting_for_two,window_moving_average)
#    ma_avg_diff_minority_total_happiness_antiplurality = moving_average(average_difference_minority_total_happiness_antiplurality,window_moving_average)
#
#    plt.plot(x_data_ma,ma_avg_diff_minority_total_happiness_borda,label="borda")
#    plt.plot(x_data_ma,ma_avg_diff_minority_total_happiness_plurality,label="plurality")
#    plt.plot(x_data_ma,ma_avg_diff_minority_total_happiness_voting_for_two,label="voting for two")
#    plt.plot(x_data_ma,ma_avg_diff_minority_total_happiness_antiplurality,label="antiplurality")
        
    mu_diff_minority_total_happiness_borda = np.average(difference_minority_total_happiness_borda)
    var_diff_minority_total_happiness_borda = np.var(difference_minority_total_happiness_borda)
    sigma_diff_minority_total_happiness_borda = math.sqrt(var_diff_minority_total_happiness_borda)
    x_diff_minority_total_happiness_borda = np.linspace(mu_diff_minority_total_happiness_borda - 3*sigma_diff_minority_total_happiness_borda, mu_diff_minority_total_happiness_borda + 3*sigma_diff_minority_total_happiness_borda, number_of_experiments)
    
    mu_diff_minority_total_happiness_plurality = np.average(difference_minority_total_happiness_plurality)
    var_diff_minority_total_happiness_plurality = np.var(difference_minority_total_happiness_plurality)
    sigma_diff_minority_total_happiness_plurality = math.sqrt(var_diff_minority_total_happiness_plurality)
    x_diff_minority_total_happiness_plurality = np.linspace(mu_diff_minority_total_happiness_plurality - 3*sigma_diff_minority_total_happiness_plurality, mu_diff_minority_total_happiness_plurality + 3*sigma_diff_minority_total_happiness_plurality, number_of_experiments)

    mu_diff_minority_total_happiness_voting_for_two = np.average(difference_minority_total_happiness_voting_for_two)
    var_diff_minority_total_happiness_voting_for_two = np.var(difference_minority_total_happiness_voting_for_two)
    sigma_diff_minority_total_happiness_voting_for_two = math.sqrt(var_diff_minority_total_happiness_voting_for_two)
    x_diff_minority_total_happiness_voting_for_two = np.linspace(mu_diff_minority_total_happiness_voting_for_two - 3*sigma_diff_minority_total_happiness_voting_for_two, mu_diff_minority_total_happiness_voting_for_two + 3*sigma_diff_minority_total_happiness_voting_for_two, number_of_experiments)

    mu_diff_minority_total_happiness_antiplurality = np.average(difference_minority_total_happiness_antiplurality)
    var_diff_minority_total_happiness_antiplurality = np.var(difference_minority_total_happiness_antiplurality)
    sigma_diff_minority_total_happiness_antiplurality = math.sqrt(var_diff_minority_total_happiness_antiplurality)
    x_diff_minority_total_happiness_antiplurality = np.linspace(mu_diff_minority_total_happiness_antiplurality - 3* sigma_diff_minority_total_happiness_antiplurality, mu_diff_minority_total_happiness_antiplurality + 3*sigma_diff_minority_total_happiness_antiplurality, number_of_experiments)


    plt.figure(figsize=(10,10))
#    plt.subplot(2, 1, 1)
    plt.plot(x_diff_minority_total_happiness_borda, stats.norm.pdf(x_diff_minority_total_happiness_borda, mu_diff_minority_total_happiness_borda, sigma_diff_minority_total_happiness_borda),label="borda, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_minority_total_happiness_borda) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_minority_total_happiness_borda))
    plt.plot(x_diff_minority_total_happiness_plurality, stats.norm.pdf(x_diff_minority_total_happiness_plurality, mu_diff_minority_total_happiness_plurality, sigma_diff_minority_total_happiness_plurality),label="plurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_minority_total_happiness_plurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_minority_total_happiness_plurality))
    plt.plot(x_diff_minority_total_happiness_voting_for_two, stats.norm.pdf(x_diff_minority_total_happiness_voting_for_two, mu_diff_minority_total_happiness_voting_for_two, sigma_diff_minority_total_happiness_voting_for_two), label = "vote2, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_minority_total_happiness_voting_for_two) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_minority_total_happiness_voting_for_two))
    plt.plot(x_diff_minority_total_happiness_antiplurality, stats.norm.pdf(x_diff_minority_total_happiness_antiplurality, mu_diff_minority_total_happiness_antiplurality, sigma_diff_minority_total_happiness_antiplurality), label = "antiplurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_minority_total_happiness_antiplurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_diff_minority_total_happiness_antiplurality))


    plt.legend(fontsize='small')
    plt.title("Distribution of the change in overall happiness \nafter strategic voting when a strategic voter is part of the minority")
    plt.xlabel("Change in overall happiness")
    plt.ylabel("Probability of the change")
#    
#    
#    
#    plt.subplot(2,1,2)    
    mu_avg_diff_minority_tot_borda = np.average(average_difference_minority_total_happiness_borda)
    var_avg_diff_minority_tot_borda = np.var(average_difference_minority_total_happiness_borda)
    sigma_avg_diff_minority_tot_borda = math.sqrt(var_avg_diff_minority_tot_borda)
    x_avg_diff_minority_tot_borda = np.linspace(mu_avg_diff_minority_tot_borda - 3*sigma_avg_diff_minority_tot_borda, mu_avg_diff_minority_tot_borda + 3*sigma_avg_diff_minority_tot_borda, number_of_experiments)
    
    mu_avg_diff_minority_tot_plurality = np.average(average_difference_minority_total_happiness_plurality)
    var_avg_diff_minority_tot_plurality = np.var(average_difference_minority_total_happiness_plurality)
    sigma_avg_diff_minority_tot_plurality = math.sqrt(var_avg_diff_minority_tot_plurality)
    x_avg_diff_minority_tot_plurality = np.linspace(mu_avg_diff_minority_tot_plurality - 3*sigma_avg_diff_minority_tot_plurality, mu_avg_diff_minority_tot_plurality + 3*sigma_avg_diff_minority_tot_plurality, number_of_experiments)

    mu_avg_diff_minority_tot_voting_for_two = np.average(average_difference_minority_total_happiness_plurality)
    var_avg_diff_minority_tot_voting_for_two = np.var(average_difference_minority_total_happiness_plurality)
    sigma_avg_diff_minority_tot_voting_for_two = math.sqrt(var_avg_diff_minority_tot_voting_for_two)
    x_avg_diff_minority_tot_voting_for_two = np.linspace(mu_avg_diff_minority_tot_voting_for_two - 3*sigma_avg_diff_minority_tot_voting_for_two, mu_avg_diff_minority_tot_voting_for_two + 3*sigma_avg_diff_minority_tot_voting_for_two, number_of_experiments)

    mu_avg_diff_minority_tot_antiplurality = np.average(average_difference_minority_total_happiness_antiplurality)
    var_avg_diff_minority_tot_antiplurality = np.var(average_difference_minority_total_happiness_antiplurality)
    sigma_avg_diff_minority_tot_antiplurality = math.sqrt(var_avg_diff_minority_tot_antiplurality)
    x_avg_diff_minority_tot_antiplurality = np.linspace(mu_avg_diff_minority_tot_antiplurality - 3* sigma_avg_diff_minority_tot_antiplurality, mu_avg_diff_minority_tot_antiplurality + 3*sigma_avg_diff_minority_tot_antiplurality, number_of_experiments)
    
    
#    plt.plot(x_avg_diff_minority_tot_borda, stats.norm.pdf(x_avg_diff_minority_tot_borda, mu_avg_diff_minority_tot_borda, sigma_avg_diff_minority_tot_borda),label="borda, "+r'$\mu={avg:.1f},$'.format(avg=mu_diff_minority_total_happiness_borda) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_minority_tot_borda))
#    plt.plot(x_avg_diff_minority_tot_plurality, stats.norm.pdf(x_avg_diff_minority_tot_plurality, mu_avg_diff_minority_tot_plurality, sigma_avg_diff_minority_tot_plurality),label="plurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_minority_tot_plurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_minority_tot_plurality))
#    plt.plot(x_avg_diff_minority_tot_voting_for_two, stats.norm.pdf(x_avg_diff_minority_tot_voting_for_two, mu_avg_diff_minority_tot_voting_for_two, sigma_avg_diff_minority_tot_voting_for_two), label = "vote2, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_minority_tot_voting_for_two) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_minority_tot_voting_for_two))
#    plt.plot(x_avg_diff_minority_tot_antiplurality, stats.norm.pdf(x_avg_diff_minority_tot_antiplurality, mu_avg_diff_minority_tot_antiplurality, sigma_avg_diff_minority_tot_antiplurality), label = "antiplurality, "+r'$\mu={avg:.1f},$'.format(avg=mu_avg_diff_minority_tot_antiplurality) + r'$\sigma={sig:.1f}$'.format(sig=sigma_avg_diff_minority_tot_antiplurality))
    
#    plt.legend(fontsize='small')
#    plt.title("Distribution of the difference of overall happiness from the average honest\nhappiness after strategic voting when a strategic voter is part of the minority")
#    plt.xlabel("Change in the difference from the average honest happiness")
#    plt.ylabel("Probability of the change from the average honest happiness")
    plt.savefig("minority_exp2_"+str(number_of_experiments)+".jpg")
    plt.show()
    
    duration_experiment = time.time() - start_experiment 
    print("Experiment about minority agent done after {duration:.3f} s".format(duration = duration_experiment))

#####################################
#### END PART MINORITY AGENT   ######
#####################################


##########################
#### FUNCTIONS CALLS #####
##########################
    
#experiment_selfish_agent()
#experiment_altruistic_agent()
experiment_majority_agent()
#experiment_minority_agent()



    
    
    
    







    

    
    
    
    

    
    
    
    








    



