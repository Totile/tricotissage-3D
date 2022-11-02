import ezdxf
import numpy as np
from visualisation import visualisation
from sketch_nails import generate_nails


FILE_NAMES = [f'/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/DXF_files/arete_{k}-16.dxf' for k in range(1, 17)]
#save_final_as = '/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/DXF_files/production.dxf'

length_absolute_path = len('/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/')

nb_nails=15
length_nail=10
width_nail=3

NAILS = {}

for k, FILE_NAME in enumerate(FILE_NAMES):
    save_as = FILE_NAME[:length_absolute_path] + 'Results/' + f'production_{k+1}.dxf'
    generate = generate_nails(from_file=FILE_NAME, 
                                    nb_nails=nb_nails, 
                                    length_nail=length_nail,
                                    width_nail=width_nail)

    spline = generate['spline']
    nails = generate['nails']
    holes = generate['holes']
    print(FILE_NAME)
    NAILS[FILE_NAME] = nails

    # Create a new DXF R2010 drawing, official DXF version name: "AC1024"
    doc = ezdxf.new('R2010')

    # Add new entities to the modelspace:
    msp = doc.modelspace()
    line = msp.add_lwpolyline(spline)
    line.close(state=True)

    for hole in holes:
        center, radius = hole
        msp.add_circle(center=center, radius=radius)

    doc.saveas(save_as)
    visualisation(save_as)