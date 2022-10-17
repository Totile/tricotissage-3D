import ezdxf
import numpy as np
from sketch_line_3 import spline, points_in_frame, points_in_spline
from visualisation import visualisation

save_as = 'production.dxf'

# Create a new DXF R2010 drawing, official DXF version name: "AC1024"
doc = ezdxf.new('R2010')

# Add new entities to the modelspace:
msp = doc.modelspace()

"""for point in spline:
    msp.add_circle(center=point[:2], radius=1)"""


"""XF = np.array(points_in_frame).T[0]
YF = np.array(points_in_frame).T[1]
xF_min = np.min(XF)
xF_max = np.max(XF)
yF_min = np.min(YF)
yF_max = np.max(YF)"""

"""msp.add_circle(center=spline[-1][:2], radius=5) 
msp.add_circle(center=points_in_spline[-1][:2], radius=5) """
"""spline.append((xF_max, yF_max, 0., 0., 0.))
spline.append((xF_max, yF_min, 0., 0., 0.))"""
"""spline.append((xF_max, yF_max, 0., 0., 0.))
spline.append((xF_max, yF_max, 0., 0., 0.))"""

line = msp.add_lwpolyline(spline)
line.close(state=True)
doc.saveas(f'./DXF_files/{save_as}')
visualisation(f'./DXF_files/{save_as}')