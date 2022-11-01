# generate a .py file using the `ezdxf` module from a .dxf file
# the type of objects created in the .py file might be complex
# in our use we have first tested this piece of code on a .dxf that was very similar to our final material and then modified `sketch_line.py` to meet our needs 

import ezdxf
from ezdxf.addons.dxf2code import entities_to_code, block_to_code
from visualisation import visualisation

def get_source_code(FILE_NAME):
    doc = ezdxf.readfile(FILE_NAME)
    msp = doc.modelspace()
    source = entities_to_code(msp)

    with open(f'/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/source_code.py', mode='wt') as f:
        f.write("import ezdxf\ndoc = ezdxf.new('R2010')\nlayout = doc.modelspace()")
        f.write(source.import_str())
        f.write('\n\n')
        f.write(source.code_str())
        f.write('\n')