import ezdxf
import numpy as np
from visualisation import visualisation
from get_source_code import get_source_code
from importlib import reload 

# the name of the .dxf file generated from informations of the original .dxf file interpreted in python
save_dxf2code_as = '/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/DXF_files/code2dxf.dxf' 

def generate_nails(from_file, nb_nails, length_nail, width_nail, save_as=save_dxf2code_as):
    
    import source_code
    
    get_source_code(FILE_NAME=from_file) # edits the file 'source_code.py' with the ezdxf code corresponding to 'FILE_NAME'

    source_code = reload(source_code)
    layout = source_code.layout
    
    lines = layout.query("LINE") # all lines objects of the 'layout' stored in ezdxf.query.EntityQuery container
    arcs = layout.query("Spline")

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
        Based on the assumption that the line (point1, point2) is on the frame iff its either vertical or horizontal

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

        #msp.add_line((x_s, y_s), (x_e, y_e))

        if is_on_frame((x_s, y_s), (x_e, y_e)):
            points_in_frame += [(x_s, y_s, 0., 0., 0.), (x_e, y_e, 0., 0., 0.)]
        else :
            points_in_spline += [(x_s, y_s, 0., 0., 0.), (x_e, y_e, 0., 0., 0.)]

        points += [(x_s, y_s, 0., 0., 0.), (x_e, y_e, 0., 0., 0.)]


    # getting the dimensions of the skecth
    def extremal_coordinates(points_):
        X = np.array(points).T[0]
        Y = np.array(points).T[1]
        x_min = np.min(X)
        x_max = np.max(X)
        y_min = np.min(Y)
        y_max = np.max(Y)
        return(x_min, x_max, y_min, y_max)
    
    x_min, x_max, y_min, y_max = extremal_coordinates(points)

    # -------------------------- CONVERT RELATIVE COORDINATES INTO ABSOLUTE ONES --------------------------   
    def relative2absolute(U, offset=(x_max, y_min)):
        """
        Parameter
        U : a n-dimensionnal array where the first two dimensions represent the coordinates along the x-axis and the y-axis
        """
        try :
            dx, dy = offset
            x, y, *_ = U
            x-=dx
            y-=dy
        except:
            print()
        return (x, y) + (len(U) - 2)*(0.,)
    
    points = [relative2absolute(point) for point in points]
    points_in_frame = [relative2absolute(point) for point in points_in_frame]
    points_in_spline = [relative2absolute(point) for point in points_in_spline]
    
    nails = []

    for line in lines:
        x_s, y_s, _ = line.dxf.start
        x_e, y_e, _ = line.dxf.end

        msp.add_line(relative2absolute((x_s, y_s)), relative2absolute((x_e, y_e)))

    x_min, x_max, y_min, y_max = extremal_coordinates(points) #should have changed as we've modified `points`

    # -------------------------- BUILDING THE SPLINE STEP BY STEP --------------------------
    points_Vec2 = [ezdxf.math.Vec2(U[:2]) for U in points] 

    margin_for_plot = 20

    spline = [] # a spline seen as its points list's
    length_original_spline = len(points_in_spline)
    points_in_spline.reverse()

    bottom_margin = 20

    i=0
    for y in np.linspace(y_min + bottom_margin, y_max, nb_nails):
        while (i < length_original_spline) and (points_in_spline[i][1] < y): # looking for the last point of the original spline with a y-coordinate < y
            #print('True', i)
            spline.append(points_in_spline[i])
            i+=1

        # line at y
        line1 = ezdxf.entities.Line()
        line1.start = (x_min - margin_for_plot, y)
        line1.end = (x_max + margin_for_plot, y)
        line_start_end1 = [ezdxf.math.Vec2(line1.start), ezdxf.math.Vec2(line1.end)]

        # line at y + width_nail
        line2 = ezdxf.entities.Line()
        line2.start = (x_min - margin_for_plot, y + width_nail)
        line2.end = (x_max + margin_for_plot, y + width_nail)
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
        
            # saving the "coordinate of the nail"
            nails.append((x_inter1 - length_nail, (y_inter1 + y_inter2) / 2))

        while (i < length_original_spline) and (points_in_spline[i][1] < y + width_nail): # looking for the last point of the original spline with a y-coordinate < y
            i+=1

    # -------------------------- MODIFY THE FRAME TO ADD THE NOTCHES --------------------------
    
    new_new_frame = []
    
    distance2outer_radius_up = 6
    distance_between_notches_up = 22
    width_notches_up = 8
    height_notches_up = 5
    nb_notches_up = 2

    distance2outer_radius_down = 12.5
    distance_between_notches_down = 40
    width_notches_down = 5
    height_notches_down = 5
    nb_notches_down = 2

    Dx_vertical = 30
    Dx_diagonal = 30
    Dy_vertical = 40
    Dy_diagonal = 50

    x_inf_up = -55
    x_inf_down = -130

    e = 1e-5

    X_up = [point[0] for point in points_in_frame if e > np.abs(point[1] - y_max)]
    X_down = [point[0] for point in points_in_frame if e > np.abs(point[1] - y_min)]

    x_min_up = min(X_up)
    x_min_down = min(X_down)

    new_new_frame.append((x_min_up, y_max))
    #msp.add_circle(center=(x_min_up, y_max), radius=5)

    new_new_frame.append((x_min_up, y_max + Dx_vertical))
    #msp.add_circle(center=(x_min_up, y_max + Dx_vertical), radius=5)

    new_new_frame.append((x_inf_up, y_max + Dx_vertical + Dx_diagonal))
    #msp.add_circle(center=(x_inf_up, y_max + Dx_vertical + Dx_diagonal), radius=5)

    y_sup = y_max + Dx_vertical + Dx_diagonal

    for i in range(nb_notches_up):

        new_new_frame.append((x_inf_up + distance2outer_radius_up + i * (distance_between_notches_up + width_notches_up), y_sup, 0., 0., 0.))
        new_new_frame.append((x_inf_up + distance2outer_radius_up + i * (distance_between_notches_up + width_notches_up), y_sup + height_notches_up, 0., 0., 0.))
        new_new_frame.append((x_inf_up + distance2outer_radius_up + i * (distance_between_notches_up + width_notches_up) + width_notches_up, y_sup + height_notches_up, 0., 0., 0.))
        new_new_frame.append((x_inf_up + distance2outer_radius_up + i * (distance_between_notches_up + width_notches_up) + width_notches_up, y_sup, 0., 0., 0.))

    new_new_frame.append((x_max, y_max + Dx_vertical + Dx_diagonal))
    #msp.add_circle(center=(x_max, y_max + Dx_vertical + Dx_diagonal), radius=5)

    new_new_frame.append((x_max, y_max))
    #msp.add_circle(center=(x_max, y_max), radius=5)

    new_new_frame.append((x_max, y_min)) # no longer compulsory with the next point
    #msp.add_circle(center=(x_max, y_min), radius=5)

    new_new_frame.append((x_max, y_min - Dy_diagonal - Dy_vertical, 0., 0., 0.))

    y_inf = y_min - Dy_diagonal -Dy_vertical

    for i in reversed(range(nb_notches_down)):
        #print(i)
        new_new_frame.append((x_inf_down + distance2outer_radius_down + i * (distance_between_notches_down + width_notches_down) + width_notches_down, y_inf))
        new_new_frame.append((x_inf_down + distance2outer_radius_down + i * (distance_between_notches_down + width_notches_down) + width_notches_down, y_inf - height_notches_down))
        new_new_frame.append((x_inf_down + distance2outer_radius_down + i * (distance_between_notches_down + width_notches_down), y_inf - height_notches_down))
        new_new_frame.append((x_inf_down + distance2outer_radius_down + i * (distance_between_notches_down + width_notches_down), y_inf))
        
        
    new_new_frame.append((x_inf_down, y_min - Dy_diagonal - Dy_vertical, 0., 0., 0.))
    new_new_frame.append((x_min, y_min - Dy_vertical, 0., 0., 0.))
    # -----------------------------------------------------------------------------------------
    
    spline += new_new_frame

    doc.saveas(save_dxf2code_as)
    visualisation(save_dxf2code_as)

    offset_x = 20

    nails = [relative2absolute(nail, offset=(offset_x, height_notches_down)) for nail in nails]

    return {'spline' : spline, 'nails' : nails}