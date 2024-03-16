import numpy as np
from utils import load_map, is_reachable, edge_distance
from collections import deque
from queue import PriorityQueue

class RealTimeGraph:
    def __init__(self, file_path, position = (0, 0, 0), target = (1, 1, 1), view = 5, Fsafe=3, jump_height=1, K=3):
        self.m = load_map(file_path) # (x, y, z) -> block_type
        self.position = position
        self.target = target
        self.graph = {}

        self.view = view
        self.Fsafe = Fsafe
        self.jump_height = jump_height
        self.K = K
        self.build_init_graph()
    
    def is_inview(self, x, y, z):
        return max(abs(np.array([x, y, z]) - np.array(self.position))) <= self.view

    def build_init_graph(self):
        for (x, y, z), block_type in self.m.items():
            if self.is_inview(x, y, z):
                edge_list = self.graph.setdefault((x, y, z), [])
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    for dz in range(self.jump_height, -self.Fsafe - 1, -1):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if nz < z and self.m.get((nx, ny, z)) == 'solid':
                            continue
                        elif is_reachable(self.m, nx, ny, nz):
                            distance = edge_distance((x, y, z), (nx, ny, nz))
                            edge_list.append(((nx, ny, nz), distance))
                            break
    
    def update_graph(self):
        # position is moving
        for (x, y, z), block_type in self.m.items():
            if self.is_inview(x, y, z):
                edge_list = self.graph.setdefault((x, y, z), []) # if not exist, create an empty list and then find the edges
                                                     # if exist, just insert new edges
                
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    for dz in range(self.jump_height, -self.Fsafe - 1, -1):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        distance = edge_distance((x, y, z), (nx, ny, nz))
                        if ((nx, ny, nz), distance) not in edge_list:
                            if nz < z and self.m.get((nx, ny, z)) == 'solid':
                                continue
                            elif is_reachable(self.m, nx, ny, nz):
                                # distance = edge_distance((x, y, z), (nx, ny, nz))
                                if ((nx, ny, nz), distance) not in self.graph[(x, y, z)]:
                                    edge_list.append(((nx, ny, nz), distance))
                                break
    
    # static path finding
    def a_star_search(self):
        open_set = PriorityQueue()
        start = self.position
        open_set.put((start, 0))
        
        came_from = {}
        '''Dijkstra's algorithm'''
        g_score = {node: float('inf') for node in self.graph}
        g_score[start] = 0
        
        f_score = {node: float('inf') for node in self.graph}
        f_score[start] = edge_distance(start, self.target)
        
        while not open_set.empty():
            current = open_set.get()[0]  # Get node with lowest f_score value
            if current == self.target:
                path = [current]
                total_cost = g_score[current]  # Total cost to reach the goal
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path, total_cost
            
            for neighbor, distance in self.graph[current]:
                tentative_g_score = g_score[current] + distance
                
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + edge_distance(neighbor, self.target)
                    open_set.put((neighbor, f_score[neighbor]))
        
        return False, 0 

    def move_agent_and_update(self):
        frontier = deque([(tuple(self.position), [])])
        visited = set()
        while frontier:
            # BFS
            # print(frontier.popleft())
            current_node, path = frontier.popleft() # np.array, path
            if current_node == self.target:
                self.position = current_node
                return path + [current_node]
            
            visited.add(tuple(current_node))
            # print("graph", self.graph)
            for neighbor, distance in self.graph[current_node]:
                if neighbor not in visited:
                    frontier.append([neighbor, path + [current_node]])
            
            self.position = current_node
            self.update_graph()
        return None

    def control_agent(self):
        path = None
        while path is None:
            path = self.move_agent_and_update()

            if path is None:
                print("No path found. Moving to a new position")
        
        for node in path:
            print("Moving to", node)
        print("Reached the target.")


if __name__ == "__main__":
    file_path = 'benchmark/simple/world-dump.txt'
    rtg = RealTimeGraph(file_path, view=1, position=(0, 0, 0), target=(2, 2, 0))
    rtg.control_agent()

    # rtg_static = RealTimeGraph(file_path, view=50, position=(0, 0, 0), target=(2, 2, 0))
    # print(rtg_static.graph)
    # path, cost = rtg_static.a_star_search()
    # print(path, cost)
