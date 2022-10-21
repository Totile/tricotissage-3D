from operator import length_hint
import ezdxf
import numpy as np
from pytest import Instance
from visualisation import visualisation
from get_source_code import get_source_code

FILE_NAME = 'arete_5-8.dxf'
save_as = 'code2dxf.dxf'
get_source_code(FILE_NAME=FILE_NAME) # edits the file 'source_code.py' with the ezdxf code corresponding to 'FILE_NAME'

from source_code import layout

lines = layout.query("LINE") # all lines objects of the 'layout' stored in ezdxf.query.EntityQuery container

# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
doc = ezdxf.new('R2010')

# Add new entities to the modelspace:
msp = doc.modelspace()

# -------------------------- BUILDING THE FRAME --------------------------
eps = 1e-3 # tolerancy for float equalities

points_in_spline = []
points_in_frame = []
points = []

def is_on_frame(point1, point2):
    '''
    Parameters
    - pointi : an 2-dimensions array

    Output
    - Bool : wether or not the line formed by (point1, point2) is on the frame i.e. is vertical or horizontal
    '''
    x1, y1 = point1
    x2, y2 = point2
    is_vertical_line = (- eps < (x1 - x2)) and ((x1 - x2) < eps)
    is_horizontal_line = (- eps < (y1 - y2)) and ((y1 - y2) < eps)
    return is_vertical_line or is_horizontal_line

for line in lines:
    x_s, y_s, _ = line.dxf.start
    x_e, y_e, _ = line.dxf.end

    msp.add_line((x_s, y_s), (x_e, y_e))

    if is_on_frame((x_s, y_s), (x_e, y_e)):
        points_in_frame += [(x_s, y_s, 0., 0., 0.), (x_e, y_e, 0., 0., 0.)]
    else :
        points_in_spline += [(x_s, y_s, 0., 0., 0.), (x_e, y_e, 0., 0., 0.)]

    points += [(x_s, y_s, 0., 0., 0.), (x_e, y_e, 0., 0., 0.)]

# getting the dimensions of the skecth
X = np.array(points).T[0]
Y = np.array(points).T[1]
x_min = np.min(X)
x_max = np.max(X)
y_min = np.min(Y)
y_max = np.max(Y)

# -------------------------- BUILDING THE SPLINE STEP BY STEP --------------------------
points_Vec2 = [ezdxf.math.Vec2(U[:2]) for U in points] 

margin = 20

nb_nails = 45
length_nail = 10
width_nail = 3

spline = [] # a spline seen as its points list's
length_original_spline = len(points_in_spline)
points_in_spline.reverse()

i=0
for y in np.linspace(y_min + 20, y_max, nb_nails):
    #print(y_min, y_max, points_in_spline[i][1])
    while (i < length_original_spline) and (points_in_spline[i][1] < y): # looking for the last point of the original spline with a y-coordinate < y
        #print('True')
        spline.append(points_in_spline[i])
        i+=1

    # line at y
    line1 = ezdxf.entities.Line()
    line1.start = (x_min - margin, y)
    line1.end = (x_max + margin, y)
    line_start_end1 = [ezdxf.math.Vec2(line1.start), ezdxf.math.Vec2(line1.end)]

    # line at y + width_nail
    line2 = ezdxf.entities.Line()
    line2.start = (x_min - margin, y + width_nail)
    line2.end = (x_max + margin, y + width_nail)
    line_start_end2 = [ezdxf.math.Vec2(line2.start), ezdxf.math.Vec2(line2.end)]

    # looking for the intersection with line1
    intersection1 = ezdxf.math.intersect_polylines_2d(points_Vec2, line_start_end1)

    # looking for the intersection with line2
    intersection2 = ezdxf.math.intersect_polylines_2d(points_Vec2, line_start_end2)
    
    # adding the four points that set up the nail
    if (len(intersection1) > 1) and (len(intersection2) > 1):
        x_inter1, y_inter1 = intersection1[1]
        spline += [(x_inter1, y_inter1, 0., 0., 0.), (x_inter1 - length_nail, y_inter1, 0., 0., 0.)]

        x_inter2, y_inter2 = intersection2[1]
        spline += [(x_inter1 - length_nail, y_inter2, 0., 0., 0.), (x_inter2, y_inter2, 0., 0., 0.)]

    while (i < length_original_spline) and (points_in_spline[i][1] < y + width_nail): # looking for the last point of the original spline with a y-coordinate < y
        i+=1

spline.append(points_in_spline[-1][:2])
spline.append((x_max + 20, y_max, 0., 0., 0.))
spline.append((x_max + 20, y_min, 0., 0., 0.))
#spline.append(spline[0]) # the spline will be closed later in 'visu.py'

doc.saveas(f'./DXF_files/{save_as}')
visualisation(f'./DXF_files/{save_as}')