import math
import numpy as np

# Assuming data format: {(x, y, z): 'block_type'}
m_xyz = {}  # input map
m_xy2xyz = {}
original_graph = {}
viewed_graph = {}
Fsafe = 3
jump_height = 1 

view_range = 5

world_txt_filename = 'benchmark/simple/world-dump.txt'

with open(world_txt_filename, 'r') as file:
    lines = file.readlines()

for line in lines:
    if line.startswith('b'):
        parts = line.split() 
        x, z, y = map(int, parts[1:4]) 
        block_type = parts[4] 
        m_xyz[(x, y, z)] = block_type
        m_xy2xyz.setdefault((x,y), []).append((x, y, z))
        

def add_edge(graph, x1, y1, z1, x2, y2, z2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    graph.setdefault((x1, y1, z1), []).append(((x2, y2, z2), distance))
    
def is_reachable(x, y, z):
    return m_xyz.get((x, y, z)) == 'solid' and m_xyz.get((x, y, z + 1)) != 'solid'

def construct_original_graph():
    for (x, y, z), block_type in m_xyz.items():
        # if not is_reachable(x, y, z):
        #     continue
        original_graph.setdefault((x, y), [])
        viewed_graph.setdefault((x, y), [])
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]: # we only consider moving 4 dirs
            for dz in range(jump_height, -Fsafe - 1, -1):
                nx, ny, nz = x + dx, y + dy, z # ignore z
                add_edge(original_graph, x, y, z, nx, ny, nz)
                add_edge(viewed_graph, x, y, z, nx, ny, nz)
                

def update_viewed_graph(cur_pos, view_range):
    cur_x, cur_y, _ = cur_pos
    x_range = (cur_x - view_range, cur_x + view_range + 1)
    y_range = (cur_y - view_range, cur_y + view_range + 1)
    for x in x_range:
        for y in y_range:
            xyz_list = m_xy2xyz[(x, y)]
            for (x, y, z) in xyz_list:
                viewed_graph[(x,y)] = []   # empty the original edge
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]: # we only consider moving 4 dirs
                    for dz in range(jump_height, -Fsafe - 1, -1):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if nz < z and m_xyz.get((nx, ny, z)) == 'solid':
                            continue
                        elif is_reachable(nx, ny, nz):
                            add_edge(viewed_graph, x, y, z, nx, ny, nz)
                            break