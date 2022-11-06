from source_code import layout
import numpy as np
import ezdxf

import matplotlib as mpl
import matplotlib.pyplot as plt
from command_orders_rotation import coordinates, rotation
from motifs import motif, motif_inter0, motif_inter1, motif_inter0_margin, motif_inter1_margin

from mpl_toolkits.mplot3d import Axes3D

Float = np.vectorize(float)

mpl.rcParams['legend.fontsize'] = 10
factor = 2
fig = plt.figure(figsize = [factor * 6.4, factor * 4.8])
ax = plt.axes(projection='3d')

with open(f'./command_orders_rotation.txt', 'r', encoding='utf-8') as command_orders:

    # ------------------------------------- VERIFICATION DE LA ROTATION --------------------------------
    
    """
    Z = np.linspace(0, 400, 100)
    X = Y = np.zeros(shape=(100, ))
    ax.plot(X, Y, Z, label='z-axis')

    H, I, J = [], [], []
    K, L, M = [], [], []
    motif_0 = motif(coordinates['0'], coordinates['1'])
    for x, y, z in motif_0:
        H.append(x)
        I.append(y)
        J.append(z)

        k, l, m = rotation([x, y, z], - 2 * np.pi / 32)
        K.append(k)
        L.append(l)
        M.append(m)
    ax.plot(H, I, J, label='original pattern 0', color='yellow', alpha=0.5)
    ax.plot(K, L, M, label='rotated pattern 0', color='green', alpha=0.5)
    """
    #ax.scatter(*rotation(motif_0[-1], - 2 * np.pi / 32), label='last point 0', color='orange', alpha=0.5)

    """
    A, B, C = [], [], []
    R, T, S = [], [], []
    motif_1 = motif(coordinates['1'], coordinates['2'])
    for x, y, z in motif_1:

        A.append(x)
        B.append(y)
        C.append(z)

        k, l, m = rotation([x, y, z],  - 2 * np.pi / 32 - 2 * np.pi / 16)
        R.append(k)
        T.append(l)
        S.append(m)
    ax.plot(A, B, C, label='original pattern 1', color='red', alpha=0.5)
    ax.plot(R, T, S, label='rotated pattern 1', color='blue', alpha=0.5)
    """
    #ax.scatter(*rotation(motif_1[0], - 2 * np.pi / 32 - 2 * np.pi / 16), label='first point 1', color='pink', alpha=0.5)

    # ------------------------------------- VERIFICATION DES POINTS INTERMEDIAIRES --------------------------------
    
    """
    Z = np.linspace(0, 400, 100)
    X = Y = np.zeros(shape=(100, ))
    ax.plot(X, Y, Z, label='z-axis')

    radial_offset = 40 # in millimeters

    H, I, J = [], [], []
    K, L, M = [], [], []
    A, B, C = [], [], []
    R, S, T = [], [], []
    motif_0 = motif(coordinates['0'], coordinates['1'])
    motif_0_inter = motif2(coordinates['0'], coordinates['1'], radial_offset)
    motif_0_inter_bis = motif3(coordinates['0'], coordinates['1'], radial_offset)
    print(motif_0_inter)
    for x, y, z in motif_0:
        H.append(x)
        I.append(y)
        J.append(z)

    for x, y, z in motif_0:
        k, l, m = rotation([x, y, z], - 2 * np.pi / 16)
        K.append(k)
        L.append(l)
        M.append(m)

    for point in motif_0_inter:
        x, y, z = rotation(point, - 2 * np.pi / 16)
        A.append(x)
        B.append(y)
        C.append(z)

    for point in motif_0_inter_bis:
        x, y, z = rotation(point, - np.pi / 16)
        R.append(x)
        S.append(y)
        T.append(z)

    #ax.plot(H, I, J, label='original pattern 0', color='blue', alpha=0.5)
    #ax.plot(K, L, M, label='rotated pattern 0', color='limegreen', alpha=1)
    #ax.plot(A, B, C, label='intermediate pattern 0', color='blue', alpha=0.5)
    ax.plot(R, S, T, label='intermediate pattern bis', color='blue', alpha=0.5)
    #ax.scatter(*motif_0_inter[-1], color='pink', label='last point')
    #ax.scatter(*rotation(motif_0_inter[-1], -2 * np.pi / 16), color='red', label='last point original pattern')
    """

    """
    A, B, C = [], [], []
    R, T, S = [], [], []
    motif_1 = motif(coordinates['1'], coordinates['2'])
    for x, y, z in motif_1:

        A.append(x)
        B.append(y)
        C.append(z)

        k, l, m = rotation([x, y, z],  - 2 * np.pi / 32 - 2 * np.pi / 16)
        R.append(k)
        T.append(l)
        S.append(m)
    ax.plot(A, B, C, label='original pattern 1', color='red', alpha=0.5)
    ax.plot(R, T, S, label='rotated pattern 1', color='blue', alpha=0.5)
    """
    radial_offset = 15 # in millimeters


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
    nb_arete = len(coordinates.keys())
    for i in range(nb_arete ):
        for x, y, z in motif_inter0_margin(coordinates[f'{i}'], coordinates[f'{(i + 1) % nb_arete}'], radial_offset, radius=2):
            X.append(x)
            Y.append(y)
            Z.append(z)

    ax.plot(X, Y, Z, color='blue',alpha=0.5)

    """
    U, V, W = [], [], []
    nb_arete = len(coordinates.keys())
    for i in range(nb_arete):
        for x, y, z in motif_inter0_margin(coordinates[f'{i}'], coordinates[f'{(i + 1) % nb_arete}'], radial_offset, radius=0.5):
            U.append(x)
            V.append(y)
            W.append(z)

    ax.plot(U, V, W, color='limegreen',alpha=0.5)
    """

    ax.set_aspect('auto')
    ax.legend()
    plt.show()