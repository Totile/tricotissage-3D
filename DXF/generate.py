import ezdxf
import numpy as np
#from sketch_line_3 import spline
from visualisation import visualisation
from sketch_nails import generate_nails

FILE_NAME = './DXF_files/arete_5-8.dxf'
save_final_as = './DXF_files/production.dxf'

spline = generate_nails(from_file=FILE_NAME, 
                                nb_nails=35, 
                                length_nail=10,
                                width_nail=3)

# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
doc = ezdxf.new('R2010')

# Add new entities to the modelspace:
msp = doc.modelspace()

line = msp.add_lwpolyline(spline)
line.close(state=True)
doc.saveas(save_final_as)
visualisation(save_final_as)