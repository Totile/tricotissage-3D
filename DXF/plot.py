import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from command_orders import coordinates, motif

Float = np.vectorize(float)

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = plt.axes(projection='3d')

arete_0, arete_1 = coordinates['0'], coordinates['1']
MOTIF = motif(arete_0, arete_1)

for i in range(len(MOTIF) - 1):
    x1, y1, z1 = MOTIF[i]
    x2, y2, z2 = MOTIF[i+1]

    T = np.linspace(0, 1, 100)
    X = (1 - T) * x1 + T * x2
    Y = (1 - T) * y1 + T * y2
    Z = (1 - T) * z1 + T * z2
    ax.plot(X, Y, Z)


for unique_id_arete in coordinates:
    X = []
    Y = []
    Z = []
    for point in coordinates[unique_id_arete]:
        x, y, z  = point
        X.append(x)
        Y.append(y)
        Z.append(z)
    ax.plot(X, Y, Z, label=f'{unique_id_arete}')

ax.set_aspect('auto')
ax.legend()
plt.show()