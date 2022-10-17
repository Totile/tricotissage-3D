import ezdxf
from ezdxf.addons.dxf2code import entities_to_code, block_to_code
from visualisation import visualisation

def get_source_code(FILE_NAME):
    doc = ezdxf.readfile(f'./DXF_files/{FILE_NAME}')
    msp = doc.modelspace()
    source = entities_to_code(msp)

    """# create source code for a block definition
    block_source = block_to_code(doc.blocks['MyBlock'])

    # merge source code objects
    source.merge(block_source)"""

    with open(f'source_code.py', mode='wt') as f:
        f.write("import ezdxf\ndoc = ezdxf.new('R2010')\nlayout = doc.modelspace()")
        f.write(source.import_str())
        f.write('\n\n')
        f.write(source.code_str())
        f.write('\n')

"""doc = ezdxf.readfile('./DXF_files/arete_fermee.dxf')
visualisation('./DXF_files/arete_fermee.dxf')"""