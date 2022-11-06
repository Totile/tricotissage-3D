import numpy as np
from motifs import motif, motif_inter0, motif_inter1, motif_inter0_margin, motif_inter1_margin

## N.B. there is currently 5 differents "motifs" implemented. They all draw the same pattern but have diffrent characterics :

## motif(list_1, list_2) :  from two lists of points that represent the positions of the pins on two neighboring edges 
# (each list is supposed to be ordered by the "key = lambda point : point[2]" in the ascending order, which is the z coordinate of each point ),
# generates the desired pattern

## motif_inter0(list_1, list_2, radial_offset) :  does the same job by adding intermediate points when moving from an edge to the other 
# so that the wire does not interfere with the robot. The intermediate point is the medium point plus radial_off * normal where normal is a normal vector 
# to the plane containing the line (point 1, point2) and containing a line parallel to the z-axis (the plane is vertical)

## motif_inter1(list_1, list_2, radial_offset) :  same thing as in motif_inter0 but defining normal in the different way, normal = np.arra([1., 0., 0.]),
# thus should be used whan rotation each "motif" between every two neighboring edge around the z-axis to overlay them as it shoul be done to command the robot

## motif_inter0_margin(list_1, list_2, radial_offset, radius) and motif_inter1_margin(list_1, list_2, radial_offset, radius) work exactly as their cousins 
# but adding a appropriate margin to each coordinate so that the robot goes around the pins instead of on the pins. The margin depends on the parameter
# radius which makes sure that the robot stays at a distance "radius" each pin. "radius" is supposed to be in mm.

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

# we assume that the structure is installed so that the "arete" 0 (in "coordinates.txt") 
# is parallel to the y-axis in the direction of the robot (OA,-ex) > 0

radial_offset = 10 # in millimeters

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

    with open(f'./command_orders_rotation.txt', 'w', encoding='utf-8') as orders:
        
        # INITIALISATION
        # rotation of the tray to the initial configuration
        orders.write('\n') #orders.write('rotation initiale\n\n') ## orders.write(f"rotation_plateau_angle {- radian2degree(theta)/2}\n\n") 
        n = 0

        # RECURRENCE
        while n < nb_aretes :

            phi = - n * theta - theta / 2
            #print(phi)
            
            list_1 = [frame2robot(rotation(coordinate, phi)) for coordinate in coordinates[f'{n}']]
            list_2 = [frame2robot(rotation(coordinate, phi)) for coordinate in coordinates[f'{(n+1) % nb_aretes}']]
            motif_ = motif_inter1(list_1, list_2, radial_offset)
            for point in motif_:
                orders.write(tostr(point) + '\n')
            # rotation of the plate to move to the next pair of edges
            orders.write('\n') #orders.write(f"\nrotation_plateau_angle {radian2degree(theta)}\n\n") 
            n += 1