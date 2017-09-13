import numpy as np

x = np.eye(5) + np.ones(5)
x[2,1]=5
xmax = np.max(x, axis=1)
xmax_i = np.argmax(x, axis=1)

