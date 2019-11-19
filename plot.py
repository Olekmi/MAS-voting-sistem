import mas_assignment_1
import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np
np.random.seed(1)

colors = n_colors('rgb(255, 200, 200)', 'rgb(200, 0, 0)', 9, colortype='rgb')
# a = np.array([mas_assignment_1.happiness_vector_plurality[mas_assignment_1.voter-1],mas_assignment_1.happiness_vector_voting_for_two[mas_assignment_1.voter-1],mas_assignment_1.happiness_vector_antiplurality[mas_assignment_1.voter-1],mas_assignment_1.happiness_vector_borda[mas_assignment_1.voter-1]])
a = np.array([mas_assignment_1.happiness_vector_plurality[mas_assignment_1.voter-1],0.5,0.6,mas_assignment_1.happiness_vector_borda[mas_assignment_1.voter-1]])
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