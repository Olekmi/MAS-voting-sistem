# import mas_assignment_1
import numpy as np
import string
keys = np.array([[4,3,2],[3,2,1],[6,5,4]])
# keys_matrix = np.array([[],[],[]])
for j in range(keys.shape[0]):
  keys_ascii = []
  for i in range(keys.shape[1]):
    keys_ascii.append(chr(ord('@')+keys[j][i]+1))
  if j == 0:
    keys_matrix = keys_ascii
  else:
    keys_matrix = np.vstack((keys_matrix,keys_ascii))
  
  print(keys_matrix)

