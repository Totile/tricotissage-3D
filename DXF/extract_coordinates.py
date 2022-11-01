from enum import unique
from loop import NAILS, FILE_NAMES

with open(f'/Users/yvesabraham/Desktop/taff/2A/Mecatro/DXF/coordinates.txt', 'w', encoding='utf-8') as f:
    for k, FILE_NAME in enumerate(FILE_NAMES):
        l_0 = len(NAILS[FILE_NAMES[0]])
        assert l_0 == len(NAILS[FILE_NAME])
        unique_id_arete = k
        for nail in NAILS[FILE_NAME]:
            f.write(f'{unique_id_arete}, {nail[0]}, {nail[1]} \n')
        #f.write('\n')
