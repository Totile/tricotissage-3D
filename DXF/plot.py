from source_code import layout
import numpy as np
import ezdxf

import matplotlib as mpl
import matplotlib.pyplot as plt
from command_orders import coordinates, rotation

from mpl_toolkits.mplot3d import Axes3D

Float = np.vectorize(float)

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = plt.axes(projection='3d')

# plot of the z-axis
J = np.linspace(0, 400, 100)
H = I = np.zeros(shape=(100, ))
ax.plot(H, I, J, label='z-axis')

with open(f'./command_orders_rotation.txt', 'r', encoding='utf-8') as command_orders:

    for unique_id_arete in coordinates:
        A = []
        B = []
        C = []
        for point in coordinates[unique_id_arete]:
            x, y, z  = point
            A.append(x)
            B.append(y)
            C.append(z)
        ax.plot(A, B, C, label=f'{unique_id_arete}')


    X, Y, Z = [], [], []
    n = 0
    for line in command_orders:
        if line == '\n':
            ax.plot(X, Y, Z, label=f'motif {n}')
            n += 1
            X, Y, Z = [], [], []
        else :
            line = line.strip()
            x, y, z = Float(line.split(', '))
            X.append(x)
            Y.append(y)
            Z.append(z)

    ax.set_aspect('auto')
    ax.legend()
    plt.show()