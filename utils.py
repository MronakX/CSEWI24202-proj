import math

def load_map(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    # origin map
    m = {}
    for line in lines:
        if line.startswith('b'):
            parts = line.split() 
            x, z, y = map(int, parts[1:4]) 
            block_type = parts[4] 
            m[(x, y, z)] = block_type # (x, y, z) -> block_type
    return m

def is_reachable(m, x, y, z):
    return m.get((x, y, z)) == 'solid' and m.get((x, y, z + 1)) != 'solid'

def edge_distance(start, target):
    x1, y1, z1 = start
    x2, y2, z2 = target
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return distance
# def edge_distance(x1, y1, z1, x2, y2, z2):
#     distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
#     return distance