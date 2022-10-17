from source_code import layout
import numpy as np
import ezdxf

#print(isinstance(spline, ezdxf.entities.Polyline),
#    isinstance(R12spline.render(layout=msp, segments=40), ezdxf.entities.Polyline))

lines = layout.query("LINE")


points = [(1, 2, 0., 0., 0.), (3, 4, 0., 0., 0.), (7, 4, 0., 0., 0.)]
print(np.array(points).T[0])
#print(len(lines))

