import ezdxf
import numpy as np
#from sketch_line_3 import spline
from visualisation import visualisation
from sketch_nails import generate_nails


FILE_NAME = '/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/DXF_files/arete_1-16.dxf'
save_final_as = '/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/DXF_files/production.dxf'

generate = generate_nails(from_file=FILE_NAME, 
                                nb_nails=15, 
                                length_nail=10,
                                width_nail=3)

spline = generate['spline']
nails = generate['nails']

# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
doc = ezdxf.new('R2010')

# Add new entities to the modelspace:
msp = doc.modelspace()
line = msp.add_lwpolyline(spline)
line.close(state=True)
#msp.add_circle((-20, 0), 5)

doc.saveas(save_final_as)
visualisation(save_final_as)