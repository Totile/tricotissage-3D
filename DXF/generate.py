import ezdxf
import numpy as np
from visualisation import visualisation
from sketch_nails import generate_nails

FILE_NAME = './DXF_files/arete_1-16.dxf'
save_final_as = './DXF_files/production.dxf'

generate = generate_nails(from_file=FILE_NAME, 
                                nb_nails=15, 
                                length_nail=10,
                                width_nail=3)

spline, nails, holes = generate['spline'], generate['nails'], generate['holes']

# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
doc = ezdxf.new('R2010')
# Add new entities to the modelspace:
msp = doc.modelspace()

line = msp.add_lwpolyline(spline, dxfattribs={"layer": "MySketch"})
line.close(state=True)

for hole in holes:
    center, radius = hole
    msp.add_circle(center=center, radius=radius, dxfattribs={"layer": "MySketch"})

doc.saveas(save_final_as)
visualisation(save_final_as)