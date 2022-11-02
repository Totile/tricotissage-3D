from source_code import layout
import numpy as np
import ezdxf

with open(f'/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/coordinates.txt', 'r', encoding='utf-8') as coordinates:
    lines = coordinates.readlines()
    #print(lines[-1].split(',')[0])

rho = np.pi / 2
R = np.array([[np.cos(rho), - np.sin(rho), 0],
        [np.sin(rho), np.cos(rho), 0],
        [0, 0, 1]])
x= np.array([1, 0, 0])

def motif(list_1, list_2):

    assert (len(list_1) == len(list_2)) and (len(list_1) > 1)
    
    couples_1 = [(list_1[i], list_1[i + 1])[::-1] for i in range(len(list_1) - 1)]
    couples_2 = [(list_2[i], list_2[i + 1]) for i in range(len(list_2) - 1)] # the motif turns "clockwise"
    
    # nb of couples of the form (l[i], l[i+1]) where i < len(l) - 1 is exactly len(l) - 1 !

    length = len(couples_1)

    motif = []

    for i1 in range(length):
        motif += [*couples_1[i1]]
        for i2 in range(length):
            motif += [*couples_2[i2]]
            if i2 < length - 1 :
                motif += [*couples_1[i1]] # must note be done if it the last "couple_2"
            if (i2 == length - 1) and (i1 == length - 1):
                motif.append(couples_1[-1][0])

    return motif

#print(motif([(0, 0), (0, 1), (0, 2), (0, 3)], [(1, 0), (1, 1), (1, 2), (1, 3)]))
def tostr(point):
        res = ''
        for x in point :
            res += str(x)
            res += ', '
        return res[:-2]

hole = [(1, 0), 3]

center, radius = hole

print(center, radius)
