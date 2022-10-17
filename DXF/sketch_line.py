from operator import length_hint
import ezdxf
import numpy as np
from pytest import Instance
from visualisation import visualisation
from get_source_code import get_source_code

FILE_NAME = 'arete_fermee.dxf'
get_source_code(FILE_NAME=FILE_NAME) # edits the file 'source_code.py' with the ezdxf code corresponding to 'FILE_NAME'

from source_code import e 

# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
doc = ezdxf.new('R2010')

# Add new entities to the modelspace:
msp = doc.modelspace()

#print(isinstance(e, ezdxf.entities.LWPolyline)) -> returns True

# getting the dimensions of the sketch
x_max, x_min = 0, 0
y_max, y_min = 0, 0

#print(e.get_points(format='xyseb'))
points = [u[:2] for u in e.get_points(format='xyseb')]
X = np.array(points).T[0]
Y = np.array(points).T[1]

points_Vec2 = [ezdxf.math.Vec2(U) for U in points]

for x in X:
    if x > x_max:
        x_max = x
    if x < x_min:
        x_min = x

for y in Y:
    if y > y_max:
        y_max = y
    if y < y_min:
        y_min = y

"""for U in points_Vec2:
    msp.add_circle(center=U, radius=5)"""

margin = 50
length_nail = 40
nb_nails = 25
width_nail = 20

for y in np.linspace(y_min, y_max, nb_nails):
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
    #print(len(intersection1))
    #msp.add_circle(center=intersection1[0], radius=20)

    # looking for the intersection with line2
    intersection2 = ezdxf.math.intersect_polylines_2d(points_Vec2, line_start_end2)
    #print(len(intersection2))
    #msp.add_circle(center=intersection2[0], radius=20)

    if intersection1 and intersection2:
        # ploting the nail from the intersection point
        x_inter1, y_inter1 = intersection1[0]
        msp.add_line((x_inter1 - length_nail, y_inter1), (x_inter1, y_inter1))

        x_inter2, y_inter2 = intersection2[0]
        msp.add_line((x_inter1 - length_nail, y_inter2), (x_inter2, y_inter2))

        center = ezdxf.math.Vec2(x_inter1 - length_nail, y_inter1 + width_nail/2)
        radius = width_nail / 2
        msp.add_arc(center=center, radius=radius, start_angle=90, end_angle=-90, is_counter_clockwise=True) 



msp.add_lwpolyline(points)
doc.saveas('./DXF_files/code2dxf.dxf')
visualisation('./DXF_files/code2dxf.dxf')