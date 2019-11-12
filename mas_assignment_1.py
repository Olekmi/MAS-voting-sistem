import numpy as np
import operator
import collections
import random

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
    return outcome

def happiness_score(outcome_indexes,index_preference_matrix):
    #we subtract the # of rows of preference matrix from  the current index of 
    #the preference of the player to get the highest index as the 1st one 
    distances = np.ones((outcome_indexes.shape[0],outcome_indexes.shape[1]), dtype=np.int32)
    
    for i in range(outcome_indexes.shape[1]):#col by col      
        for j in range(outcome_indexes.shape[0]):
            distances[j][i] = outcome_indexes[j][i] - index_preference_matrix[j]

#    print("distances\n",distances)
    happiness_score = distances * index_preference_matrix
#    print("happiness\n",happiness_score)
    return happiness_score

            
def translate_index_matrix(matrix):
    indexes = []
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            if (i == matrix.shape[1] - 1):
                indexes.append(matrix.shape[0] - j)
    indexes_numpy = np.asarray(indexes,dtype=np.int32)
    indexes_numpy = np.reshape(indexes_numpy,(matrix.shape[0],1))
    return indexes_numpy
            

def translate_index_dictionary(preference_matrix,outcome_dictionary):
    indexes= np.ones((preference_matrix.shape[0],preference_matrix.shape[1]), dtype=np.int32)
    for i in range(preference_matrix.shape[1]):
        for j in range(preference_matrix.shape[0]):
            indexes[j][i] = len(outcome_dictionary) - list(outcome_dictionary.keys()).index(preference_matrix[j][i])
    return indexes
    
    
def total_distance_players(happiness_score):
    total_sum = np.sum(happiness_score,axis=0)
    return np.reshape(total_sum,(total_sum.shape[0],1))  


  
    
def happiness_player(total_distance_players):
    happiness_player = 1/(1+np.abs(total_distance_players))
    return happiness_player
    
    
    
preference_matrix = gen_random_preference_matrix(number_of_preferences,number_of_voters)
print(preference_matrix)
outcome = calculate_outcome(preference_matrix)
print(outcome)


test= np.array([[1,2,3],
                [4,5,6]])
    
test2 = np.array([[4,1,5]])




indexes_matrix = translate_index_matrix(preference_matrix)
indexes_dict = translate_index_dictionary(preference_matrix,outcome)
happiness_scores = happiness_score(indexes_dict,indexes_matrix) 

total_distance_player = total_distance_players(happiness_scores)
print(total_distance_player)

total_happiness_player = happiness_player(total_distance_player)
print(total_happiness_player)

#Todo : implement strategic voting
#Burying, Compromising, Push over, Bullet voting
def Compromising(happiness_scoress,preference_matrix,voter):
    counter = 0
    vector_happiness = []
    new_happiness_score = []
    preference_matrix_A_acc = []
    if total_happiness_player[voter-1] != 1:#because the index starts frm 0
        print("We will improve your happiness.") 
        for j in range(preference_matrix.shape[0]):
            if j>0: #we do not change the top preference, only an alternative
                for g in range(preference_matrix.shape[0]-j-1):#we will iterate through options. 2nd will check everything, but 1st. 3rd, all, but 1st and 2nd, etc.
                    counter += 1
                    g = preference_matrix.shape[0] - g-1#inversing index
                    # print("g",g)
                    preference_matrix_A = preference_matrix
                    alternative_A = preference_matrix_A[j][voter-1]
                    preference_matrix_A[j][voter-1] = preference_matrix_A[g][voter-1]
                    preference_matrix_A[g][voter-1] = alternative_A
                    outcome_A = calculate_outcome(preference_matrix_A)
                    indexes_matrix_A = translate_index_matrix(preference_matrix_A)
                    indexes_dict_A = translate_index_dictionary(preference_matrix_A,outcome_A)
                    happiness_score_A = happiness_score(indexes_dict_A,indexes_matrix_A) 
                    total_distance_player_A = total_distance_players(happiness_score_A)
                    new_happiness_score = happiness_player(total_distance_player_A)
                    vector_happiness.append(new_happiness_score[voter-1])
                    preference_matrix_A_acc.append(preference_matrix_A)
        max_h = max(vector_happiness)  
        index_max = vector_happiness.index(max_h)
    else:
        print("We do not need to improve your happiness.") 
        index_max = 0
        preference_matrix_A_acc = [[1]]
    print("vector_happ after compromising voting",vector_happiness[index_max])
    return preference_matrix_A_acc[index_max]

strategy_Compromising = Compromising(total_happiness_player,preference_matrix,voter)
print(strategy_Compromising)
    

    
