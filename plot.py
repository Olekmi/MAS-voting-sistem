import mas_assignment_1
import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np
import util

#-----------------------------------------------------------------------#
#OUTCOME WITH HONEST VOTING FOR 4 VOTING SCHEMES
keys_honest_plurality = list(mas_assignment_1.outcome_plurality)
keys_honest_voting_for_two = list(mas_assignment_1.outcome_voting_for_two)
keys_honest_antiplurality = list(mas_assignment_1.outcome_antiplurality)
keys_honest_borda = list(mas_assignment_1.outcome_borda)

values_honest_plurality= list(mas_assignment_1.outcome_plurality.values())
values_honest_voting_for_two= list(mas_assignment_1.outcome_voting_for_two.values())
values_honest_antiplurality = list(mas_assignment_1.outcome_antiplurality.values())
values_honest_borda = list(mas_assignment_1.outcome_borda.values())

keys_ascii_honest_plurality = util.number_to_ascii(keys_honest_plurality)
keys_ascii_honest_voting_for_two = util.number_to_ascii(keys_honest_voting_for_two)
keys_ascii_honest_antiplurality = util.number_to_ascii(keys_honest_antiplurality)
keys_ascii_honest_borda = util.number_to_ascii(keys_honest_borda)

text_honest_plurality = util.join_strings_for_graph(keys_honest_plurality,keys_ascii_honest_plurality,values_honest_plurality)
text_honest_voting_for_two = util.join_strings_for_graph(keys_honest_voting_for_two,keys_ascii_honest_voting_for_two,values_honest_voting_for_two)
text_honest_antiplurality = util.join_strings_for_graph(keys_honest_antiplurality,keys_ascii_honest_antiplurality,values_honest_antiplurality)
text_honest_borda = util.join_strings_for_graph(keys_honest_borda,keys_ascii_honest_borda,values_honest_borda)



#----------Outcome of honest voting for all schemes------------
colors = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', max(values_honest_borda)+1, colortype='rgb')
fig_outcome = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Plurality<b>','<b>Voting for two<b>', '<b>Antiplurality<b>', '<b>Borda<b>'],
    line_color='white', fill_color='white',
    align='center',font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[text_honest_plurality, text_honest_voting_for_two, text_honest_antiplurality, text_honest_borda],
    line_color=[np.array(colors)[values_honest_plurality],np.array(colors)[values_honest_voting_for_two],np.array(colors)[values_honest_antiplurality], np.array(colors)[values_honest_borda]],
    fill_color=[np.array(colors)[values_honest_plurality],np.array(colors)[values_honest_voting_for_two],np.array(colors)[values_honest_antiplurality], np.array(colors)[values_honest_borda]],
    align='center', font=dict(color='black', size=12)
    ))
])

fig_outcome.update_layout(
    title={
        'text': "Outcome for honest voting",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})        

fig_outcome.show()

#----------Happiness for all schemes and all strategies for an agent------------
colors = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', max(values_honest_borda)+1, colortype='rgb')
a = np.round(np.array([mas_assignment_1.happiness_vector_plurality[mas_assignment_1.voter_compromising_plurality],mas_assignment_1.happiness_voting_for_two[mas_assignment_1.voter_compromising_voting_for_two],mas_assignment_1.happiness_antiplurality[mas_assignment_1.voter_compromising_anti_plurality],mas_assignment_1.happiness_vector_borda[mas_assignment_1.voter_compromising_borda]]),2)
a_int = a.astype(int)
b = np.array([mas_assignment_1.happiness_vector_plurality_agent,mas_assignment_1.happiness_voting_for_two_agent,mas_assignment_1.happiness_antiplurality_agent,mas_assignment_1.happiness_vector_borda_agent])
b_int = a.astype(int)
c = np.array([mas_assignment_1.happiness_vector_plurality_bagent,mas_assignment_1.happiness_voting_for_two_bagent,mas_assignment_1.happiness_antiplurality_bagent,mas_assignment_1.happiness_vector_borda_bagent])
c_int = a.astype(int)
d = ['<b>Plurality<b>', '<b>Voting for two<b>', '<b>Antiplurality<b>', '<b>Borda<b>']

fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b> </b>','<b>Honest</b>', '<b>Compromising</b>', '<b>Bullet</b>'],
    line_color='white', fill_color='white',
    align='center',font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[d, a, b, c],
    line_color=['white',np.array(colors)[a_int],np.array(colors)[b_int], np.array(colors)[c_int]],
    fill_color=['white',np.array(colors)[a_int],np.array(colors)[b_int], np.array(colors)[c_int]],
    align='center', font=dict(color='black', size=12)
    ))
])

fig.update_layout(
    title={
        'text': "Happiness score for optimized selfish agent",
        'y':0.9,
        'x':0.62,
        'xanchor': 'center',
        'yanchor': 'top'})

fig.show()

#----------Overall Happiness for all schemes and all strategies for altruistic agent------------
a = np.round(np.array([mas_assignment_1.happiness_overall_vector_plurality,mas_assignment_1.happiness_overall_voting_for_two,mas_assignment_1.happiness_overall_antiplurality,mas_assignment_1.happiness_overall_vector_borda]),2)
a_int = a.astype(int)
b = np.round(np.array([mas_assignment_1.compromising_alt_plurality[0][2],mas_assignment_1.compromising_alt_voting_for_two[0][2],mas_assignment_1.compromising_alt_anti_plurality[0][2],mas_assignment_1.compromising_alt_borda[0][2]]),2)
b_int = a.astype(int)
c = np.round(np.array([mas_assignment_1.bullet_alt_plurality[0][2],mas_assignment_1.bullet_alt_voting_for_two[0][2],mas_assignment_1.bullet_alt_anti_plurality[0][2],mas_assignment_1.bullet_alt_borda[0][2]]),2)
c_int = a.astype(int)
d = ['<b>Plurality<b>', '<b>Voting for two<b>', '<b>Antiplurality<b>', '<b>Borda<b>']

fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b> </b>','<b>Honest</b>', '<b>Compromising</b>', '<b>Bullet</b>'],
    line_color='white', fill_color='white',
    align='center',font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[d, a, b, c],
    line_color=['white',np.array(colors)[a_int],np.array(colors)[b_int], np.array(colors)[c_int]],
    fill_color=['white',np.array(colors)[a_int],np.array(colors)[b_int], np.array(colors)[c_int]],
    align='center', font=dict(color='black', size=12)
    ))
])

fig.update_layout(
    title={
        'text': "Happiness score for optimized altruistic agent",
        'y':0.9,
        'x':0.62,
        'xanchor': 'center',
        'yanchor': 'top'})

fig.show()