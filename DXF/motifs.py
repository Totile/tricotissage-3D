import numpy as np

def rotation(x, rho):
    """
    Implements the rotation around the z-axis of angle rho
    """
    R = np.array([[np.cos(rho), - np.sin(rho), 0],
        [np.sin(rho), np.cos(rho), 0],
        [0, 0, 1]])
    return np.dot(R, x)

def normalize(v):
    norm = np.linalg.norm(v)
    eps = 1e-4
    if (norm > - eps) and (eps > norm): 
       return v
    return v / norm

def to_the_right(couple, radius):
    '''
    list : a list of n-dimensionnal arrays
    '''
    point_down, point_up = couple
    point_down[1] += radius 
    point_down[2] -= radius 

    point_up[1] += radius
    point_up[2] += radius 

    return(point_down, point_up)

def to_the_left(couple, radius):
    '''
    list : a list of n-dimensionnal arrays
    '''
    point_up, point_down = couple
    point_up[1] -= radius 
    point_up[2] += radius 

    point_down[1] -= radius
    point_down[2] -= radius 

    return(point_up, point_down)

def up(point, radius):
    point[2] += radius
    return point

def down(point, radius):
    point[2] -= radius
    return point

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

def motif_inter0(list_1, list_2, radial_offset):

    assert (len(list_1) == len(list_2)) and (len(list_1) > 1)
    
    couples_1 = [(list_1[i], list_1[i + 1])[::-1] for i in range(len(list_1) - 1)]
    couples_2 = [(list_2[i], list_2[i + 1]) for i in range(len(list_2) - 1)] # the motif turns "clockwise"
    
    # nb of couples of the form (l[i], l[i+1]) where i < len(l) - 1 is exactly len(l) - 1 !

    length = len(couples_1)

    motif = []

    intermediate_points = [] ##

    def inter(u, v, radial_offset, to):
        """
        u is the first one, v the second one
        """
        res = np. array(u) + (np.array(v) - np.array(u))/2
        x, y, z = (np.array(v) - np.array(u))
        if to == 'right': #to the "right", ascending on the y-axis
            normal = normalize(rotation([x, y, 0], -np.pi / 2)) # a normal vector of the plane containing a line parallel to the z-axis and the line passing through u and v
        elif to == 'left':
            normal = normalize(rotation([x, y, 0], np.pi / 2))

        return list(res + radial_offset * normal)

    last = np.array(0)

    for i1 in range(length):

        print(last)
        if last.any() : # "if any of the coordinates of last is non nul"
            intermediate_point = inter(last, couples_1[i1][0], radial_offset, to='left') ##
            motif.append(intermediate_point)

        motif += [*couples_1[i1]]
        last = couples_1[i1][-1]

        for i2 in range(length):
            intermediate_point = inter(last, couples_2[i2][0], radial_offset, to='right') ##
            motif.append(intermediate_point)
            motif += [*couples_2[i2]]
            last = couples_2[i2][-1]

            if i2 < length - 1 :
                intermediate_point = inter(last, couples_1[i1][0], radial_offset, to='left') ##
                motif.append(intermediate_point)
                motif += [*couples_1[i1]] # must note be done if it the last "couple_2"
                last = couples_1[i1][-1]

            if (i2 == length - 1) and (i1 == length - 1):
                intermediate_point = inter(last, couples_1[-1][0], radial_offset, to='left') ##
                motif.append(intermediate_point)
                motif.append(couples_1[-1][0])

    return motif

def motif_inter1(list_1, list_2, radial_offset):

    assert (len(list_1) == len(list_2)) and (len(list_1) > 1)
    
    couples_1 = [(list_1[i], list_1[i + 1])[::-1] for i in range(len(list_1) - 1)]
    couples_2 = [(list_2[i], list_2[i + 1]) for i in range(len(list_2) - 1)] # the motif turns "clockwise"
    
    # nb of couples of the form (l[i], l[i+1]) where i < len(l) - 1 is exactly len(l) - 1 !

    length = len(couples_1)

    motif = []

    intermediate_points = [] ##

    def inter(u, v, radial_offset, to):
        """
        u is the first one, v the second one
        """
        res = np. array(u) + (np.array(v) - np.array(u))/2
        x, y, z = (np.array(v) - np.array(u))
        normal = np.array((1., 0., 0.))

        return list(res + radial_offset * normal)

    last = np.array(0)

    for i1 in range(length):

        if last.any() : # "if any of the coordinates of last is non nul"
            intermediate_point = inter(last, couples_1[i1][0], radial_offset, to='left') ##
            motif.append(intermediate_point)

        motif += [*couples_1[i1]]
        last = couples_1[i1][-1]

        for i2 in range(length):
            intermediate_point = inter(last, couples_2[i2][0], radial_offset, to='right') ##
            motif.append(intermediate_point)
            motif += [*couples_2[i2]]
            last = couples_2[i2][-1]

            if i2 < length - 1 :
                intermediate_point = inter(last, couples_1[i1][0], radial_offset, to='left') ##
                motif.append(intermediate_point)
                motif += [*couples_1[i1]] # must note be done if it the last "couple_2"
                last = couples_1[i1][-1]

            if (i2 == length - 1) and (i1 == length - 1):
                intermediate_point = inter(last, couples_1[-1][0], radial_offset, to='left') ##
                motif.append(intermediate_point)
                motif.append(couples_1[-1][0])

    return motif

def to_the_right(couple, radius):
    '''
    list : a list of n-dimensionnal arrays
    '''
    radius = radius/(np.sqrt(2))
    point_down, point_up = couple
    point_down[1] += radius 
    point_down[2] -= radius 

    point_up[1] += radius
    point_up[2] += radius 

    return(point_down, point_up)

def to_the_left(couple, radius):
    '''
    list : a list of n-dimensionnal arrays
    '''
    radius = radius/(np.sqrt(2))
    point_up, point_down = couple
    point_up[1] -= radius 
    point_up[2] += radius 

    point_down[1] -= radius
    point_down[2] -= radius 

    return(point_up, point_down)

def up(point, radius):
    point[2] += radius
    return point

def down(point, radius):
    point[2] -= radius
    return point

def margin(point, vertical, horizontal, radius):
    v = int(vertical == 'down')
    h = int(horizontal == 'left')
    point[1] += (1 - 2 * v) * radius
    point[2] += (1 - 2 * h) * radius
    return point

def motif_inter1_margin(list_1, list_2, radial_offset, radius):

    assert (len(list_1) == len(list_2)) and (len(list_1) > 1)
    
    couples_1 = [(list_1[i], list_1[i + 1])[::-1] for i in range(len(list_1) - 1)]
    couples_2 = [(list_2[i], list_2[i + 1]) for i in range(len(list_2) - 1)] # the motif turns "clockwise"
    
    # nb of couples of the form (l[i], l[i+1]) where i < len(l) - 1 is exactly len(l) - 1 !

    length = len(couples_1)

    motif = []

    intermediate_points = [] ##

    def inter(u, v, radial_offset, to):
        """
        u is the first one, v the second one
        """
        res = np. array(u) + (np.array(v) - np.array(u))/2
        x, y, z = (np.array(v) - np.array(u))
        normal = np.array((1., 0., 0.))

        return list(res + radial_offset * normal)

    last = np.array(0)

    for i1 in range(length):

        if last.any() : # "if any of the coordinates of last is non nul"
            intermediate_point = inter(last, couples_1[i1][0], radial_offset, to='left') ##
            motif.append(up(intermediate_point, radius))

        motif += [*to_the_left(couples_1[i1], radius)]
        last = couples_1[i1][-1]

        for i2 in range(length):
            intermediate_point = inter(last, couples_2[i2][0], radial_offset, to='right') ##
            motif.append(intermediate_point)
            motif += [*to_the_right(couples_2[i2], radius)]
            last = couples_2[i2][-1]

            if i2 < length - 1 :
                intermediate_point = inter(last, couples_1[i1][0], radial_offset, to='left') ##
                motif.append(intermediate_point)
                motif += [*to_the_left(couples_1[i1], radius)] # must note be done if it the last "couple_2"
                last = couples_1[i1][-1]

            if (i2 == length - 1) and (i1 == length - 1):
                intermediate_point = inter(last, couples_1[-1][0], radial_offset, to='left') ##
                motif.append(intermediate_point)
                motif.append(margin(couples_1[-1][0], vertical='up', horizontal='left', radius=radius))

    return motif

def motif_inter0_margin(list_1, list_2, radial_offset, radius):

    assert (len(list_1) == len(list_2)) and (len(list_1) > 1)
    
    couples_1 = [(list_1[i], list_1[i + 1])[::-1] for i in range(len(list_1) - 1)]
    couples_2 = [(list_2[i], list_2[i + 1]) for i in range(len(list_2) - 1)] # the motif turns "clockwise"
    
    # nb of couples of the form (l[i], l[i+1]) where i < len(l) - 1 is exactly len(l) - 1 !

    length = len(couples_1)

    motif = []

    intermediate_points = [] ##

    def inter(u, v, radial_offset, to):
        """
        u is the first one, v the second one
        """
        res = np. array(u) + (np.array(v) - np.array(u))/2
        x, y, z = (np.array(v) - np.array(u))
        if to == 'right': #to the "right", ascending on the y-axis
            normal = normalize(rotation([x, y, 0], -np.pi / 2)) # a normal vector of the plane containing a line parallel to the z-axis and the line passing through u and v
        elif to == 'left':
            normal = normalize(rotation([x, y, 0], np.pi / 2))

        return list(res + radial_offset * normal)

    last = np.array(0)

    for i1 in range(length):

        if last.any() : # "if any of the coordinates of last is non nul"
            intermediate_point = inter(last, couples_1[i1][0], radial_offset, to='left') ##
            motif.append(up(intermediate_point, radius))

        motif += [*to_the_left(couples_1[i1], radius)]
        last = couples_1[i1][-1]

        for i2 in range(length):
            intermediate_point = inter(last, couples_2[i2][0], radial_offset, to='right') ##
            motif.append(intermediate_point)
            motif += [*to_the_right(couples_2[i2], radius)]
            last = couples_2[i2][-1]

            if i2 < length - 1 :
                intermediate_point = inter(last, couples_1[i1][0], radial_offset, to='left') ##
                motif.append(intermediate_point)
                motif += [*to_the_left(couples_1[i1], radius)] # must note be done if it the last "couple_2"
                last = couples_1[i1][-1]

            if (i2 == length - 1) and (i1 == length - 1):
                intermediate_point = inter(last, couples_1[-1][0], radial_offset, to='left') ##
                motif.append(intermediate_point)
                motif.append(margin(couples_1[-1][0], vertical='up', horizontal='left', radius=radius))

    return motif