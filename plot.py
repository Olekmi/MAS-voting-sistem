import mas_assignment_1
import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np
np.random.seed(1)

def number_to_ascii(keys):
  keys_ascii = []
  for i in range(len(keys)):
    keys_ascii.append(chr(ord('@')+keys[i]+1))
  return keys_ascii
  
def join_strings_for_graph(keys,keys_ascii,values):
  text = []    
  for i in range(len(keys)):
    text.append(str(keys_ascii[i]) + ": " + str(values[i]))
  return text


colors = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', 30, colortype='rgb')
a = np.array([mas_assignment_1.happiness_voting_for_two[mas_assignment_1.voter-1],mas_assignment_1.happiness_voting_for_two[mas_assignment_1.voter-1],mas_assignment_1.happiness_antiplurality[mas_assignment_1.voter-1],mas_assignment_1.happiness_vector_borda[mas_assignment_1.voter-1]])
a_int = a.astype(int)

b = np.random.randint(low=0, high=9, size=4)
c = np.random.randint(low=0, high=9, size=4)
d = ['<b>Plurality<b>', '<b>Voting for two<b>', '<b>Antiplurality<b>', '<b>Borda<b>']

fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b> </b>','<b>Honest</b>', '<b>Compromising</b>', '<b>Bullet</b>'],
    line_color='white', fill_color='white',
    align='center',font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[d, a, b, c],
    line_color=['white',np.array(colors)[a_int],np.array(colors)[b], np.array(colors)[c]],
    fill_color=['white',np.array(colors)[a_int],np.array(colors)[b], np.array(colors)[c]],
    align='center', font=dict(color='black', size=12)
    ))
])

fig.update_layout(
    title={
        'text': "Happiness score",
        'y':0.9,
        'x':0.62,
        'xanchor': 'center',
        'yanchor': 'top'})

fig.show()

#-----------------------------------------------------------------------#
#OUTCOME WITH HONEST VOTING FOR 4 VOTING SCHEMES
colors_outcome = n_colors('rgb(255, 200, 200)', 'rgb(100, 0, 0)', 30, colortype='rgb')
keys_honest_plurality = list(mas_assignment_1.outcome_plurality)
keys_honest_voting_for_two = list(mas_assignment_1.outcome_voting_for_two)
keys_honest_antiplurality = list(mas_assignment_1.outcome_antiplurality)
keys_honest_borda = list(mas_assignment_1.outcome_borda)

values_honest_plurality= list(mas_assignment_1.outcome_plurality.values())
values_honest_voting_for_two= list(mas_assignment_1.outcome_voting_for_two.values())
values_honest_antiplurality = list(mas_assignment_1.outcome_antiplurality.values())
values_honest_borda = list(mas_assignment_1.outcome_borda.values())

keys_ascii_honest_plurality = number_to_ascii(keys_honest_plurality)
keys_ascii_honest_voting_for_two = number_to_ascii(keys_honest_voting_for_two)
keys_ascii_honest_antiplurality = number_to_ascii(keys_honest_antiplurality)
keys_ascii_honest_borda = number_to_ascii(keys_honest_borda)

text_honest_plurality = join_strings_for_graph(keys_honest_plurality,keys_ascii_honest_plurality,values_honest_plurality)
text_honest_voting_for_two = join_strings_for_graph(keys_honest_voting_for_two,keys_ascii_honest_voting_for_two,values_honest_voting_for_two)
text_honest_antiplurality = join_strings_for_graph(keys_honest_antiplurality,keys_ascii_honest_antiplurality,values_honest_antiplurality)
text_honest_borda = join_strings_for_graph(keys_honest_borda,keys_ascii_honest_borda,values_honest_borda)

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

