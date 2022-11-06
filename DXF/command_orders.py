import numpy as np

# offset is the vector 'origin of the robot -> origin of the structure'
# lengths must be entered in millimeters
lx = 0
ly = 0
lz = 0
offset = np.array((lx, ly, lz))

theta = 2 * np.pi / 16

def polar2cartesian(k, r, h):
    """
    given the coordinates of a notche on an "arete", returns the cartesian 
    coordinates in the direct orthonormal referiential of the robot

    Parameters 
    - k : the index of the arete on which is placed the notch
    - r : the distance of the notch to the center of the structure (should be < 0 in "coordinates.txt")
    - h : the height at which is placed the notch on the arete 
          (the origin is considered the upper face of the plateau on which the aretes are set)
    """
    r = np.abs(r)
    phi = k * theta
    z = h
    return np.array((r * np.cos(phi), r * np.sin(phi), z))

def rotation(x, rho):
    """
    Implements the rotation around the z-axis of angle rho
    """
    R = np.array([[np.cos(rho), - np.sin(rho), 0],
        [np.sin(rho), np.cos(rho), 0],
        [0, 0, 1]])
    return np.dot(R, x)

def frame2robot(x):
    return x + offset

def radian2degree(angle):
    return angle * 180 / np.pi

def motif(list_1, list_2):
    """
    From two lists of points, this function generates the 
    ordered sequence of points that represents the desired pattern 

    Parameters 
    - list_1, list_2 : sequences of n-dimensionnal arrays that are respectiviliy inscribed in two parallel (and vertical) lines (say l_1 and l_2) 

    Output
    - a sequence of n-dimensionnal arrays forming the desired pattern (if it's browsed in order and by joining the neighboring points)
    """

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


# we assume that the structure is installed so that the "arete" 0 (in "coordinates.txt") 
# is parallel to the y-axis in the direction of the robot (OA,-ex) > 0

with open(f'./coordinates.txt', 'r', encoding='utf-8') as coordinates_file:
    
    join_on = '\n'

    # creating a dictionnary whose keys are the number of the arete (from 0 to 15) and whose elements is 
    # the list of notches' coordinates on each arete
    coordinates = {}

    for line in coordinates_file:
        unique_id_arete, r, h = line.split(',')
        coordinates.setdefault(str(unique_id_arete), []).append(polar2cartesian(float(unique_id_arete),
                                                                                 float(r), 
                                                                                 float(h)))
    
    nb_aretes = len(coordinates.keys())
    
    def tostr(point):
        res = ''
        for x in point :
            res += str(x)
            res += ', '
        return res[:-2]

    with open(f'./command_orders.txt', 'w', encoding='utf-8') as orders:
        
        # INITIALISATION
        # rotation du plateau pour se trouver dans la configuration initiale
        orders.write('\n') #orders.write('rotation initiale\n\n') ## orders.write(f"rotation_plateau_angle {- radian2degree(theta)/2}\n\n") 
        n = 0

        # RECURRENCE
        while n < nb_aretes :

            phi = n * theta - theta / 2
            
            list_1 = [frame2robot(coordinate) for coordinate in coordinates[f'{n}']]
            list_2 = [frame2robot(coordinate) for coordinate in coordinates[f'{(n+1) % nb_aretes}']]
            motif_ = motif(list_1, list_2)
            for point in motif_:
                orders.write(tostr(point) + '\n')
            orders.write('\n') #orders.write(f"\nrotation_plateau_angle {radian2degree(theta)}\n\n") 
            n += 1