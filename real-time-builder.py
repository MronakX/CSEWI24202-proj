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
        self.graph = self.build_init_graph(view)
        self.graph2 = self.build_init_graph(5)
    
    def is_inview(self, x, y, z, view):
        diff = abs(np.array([x, y, z]) - np.array(self.position))
        return max(diff[0], diff[1]) <= view

    def build_init_graph(self, view):
        graph = {}
        for (x, y, z), block_type in self.m.items():
            if self.is_inview(x, y, z, view):
                edge_list = graph.setdefault((x, y, z), [])
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    for dz in range(self.jump_height, -self.Fsafe - 1, -1):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if self.is_inview(nx, ny, nz, view):
                            if nz < z and self.m.get((nx, ny, z)) == 'solid':
                                continue
                            elif is_reachable(self.m, nx, ny, nz):
                                distance = edge_distance((x, y, z), (nx, ny, nz))
                                edge_list.append(((nx, ny, nz), distance))
                                break
        return graph
    
    def update_graph(self, view):
        # position is moving
        # print('---updating graph---')
        # print('all node', self.m.keys())
        # print('current position', self.position)
        for (x, y, z), block_type in self.m.items():
            if self.is_inview(x, y, z, view):
                # print('update', x, y, z)
                edge_list = self.graph.setdefault((x, y, z), []) # if not exist, create an empty list and then find the edges
                                                     # if exist, just insert new edges
                # print('original edge_list', edge_list)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    for dz in range(self.jump_height, -self.Fsafe - 1, -1):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        distance = edge_distance((x, y, z), (nx, ny, nz))
                        if self.is_inview(nx, ny, nz, view):
                            if ((nx, ny, nz), distance) not in edge_list:
                                if nz < z and self.m.get((nx, ny, z)) == 'solid':
                                    # print('blocked by sky', nx, ny, nz)
                                    continue
                                elif is_reachable(self.m, nx, ny, nz):
                                    # distance = edge_distance((x, y, z), (nx, ny, nz))
                                    # print('is reachable', nx, ny, nz)
                                    if ((nx, ny, nz), distance) not in self.graph[(x, y, z)]:
                                        edge_list.append(((nx, ny, nz), distance))
                                    break
                        # else:
                #             print('is not in view', nx, ny, nz)
                # print('updated edge_list', edge_list)
    
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

    def move_agent_and_update_with_cost(self):
        frontier = PriorityQueue()
        frontier.put((0, self.position))

        came_from = {}
        g_score = {node: float('inf') for node in self.graph}
        g_score[self.position] = 0

        f_score = {node: float('inf') for node in self.graph}
        f_score[self.position] = edge_distance(self.position, self.target)


        while not frontier.empty():
            # BFS
            # print(frontier.get())
            # print('g_score', g_score)
            # print('graph', self.graph)
            current_cost, current_node = frontier.get()
            if current_node == self.target:
                path = [current_node]
                total_cost = g_score[current_node]
                while current_node in came_from:
                    current_node = came_from[current_node]
                    path.append(current_node)
                path.reverse()
                return path, total_cost
            
            self.position = current_node
            self.update_graph(self.view)
            for node in self.graph:
                if node not in g_score:
                    g_score[node] = float('inf')
            
            for neighbor, distance in self.graph[current_node]:
                tentative_g_score = g_score[current_node] + distance
            
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + edge_distance(neighbor, self.target)
                    frontier.put((f_score[neighbor], neighbor))


        return False, 0

    def move_agent_and_update(self):
        frontier = deque([(tuple(self.position), [])])
        visited = set()

    
        while frontier:
            # BFS
            # print(frontier.popleft())
            # print('graph', self.graph)
            # print('graph2', self.graph2)
            current_node, path = frontier.popleft() # np.array, path
            # print('current_node', current_node)
            # print('neightbor', self.graph[current_node])
            # print('acctual neighbor', self.graph2[current_node])
            if current_node == self.target:
                self.position = current_node
                return path + [current_node]
            
            if current_node not in visited:
                visited.add(tuple(current_node))

            self.position = current_node
            self.update_graph(self.view)
            # print("graph", self.graph)
            for neighbor, distance in self.graph[current_node]:
                if neighbor not in visited:
                    frontier.append([neighbor, path + [current_node]])
            
            # print('frontier', frontier)

            
        return None

    def control_agent(self):
        path, cost = self.move_agent_and_update_with_cost()

        if path is None:
            print("No path found. Moving to a new position")
    
        for node in path:
            print("Moving to", node)
        print('total cost', cost)
        print("Reached the target.")


if __name__ == "__main__":
    # file_path = '/Users/liuyulin/Documents/GitHub/CSEWI24202-proj/benchmark/skyblock/world-dump.txt'
    file_path = 'benchmark/simple/world-dump.txt'
    rtg = RealTimeGraph(file_path, view=1, position=(0, 0, 0), target=(2, 2, 0))
    path, cost = rtg.control_agent()

    # rtg_static = RealTimeGraph(file_path, view=50, position=(0, 0, 0), target=(2, 2, 0))
    # print(rtg_static.graph)
    # path, cost = rtg_static.a_star_search()
    # print(path, cost)
