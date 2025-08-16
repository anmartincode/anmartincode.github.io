from collections import deque, defaultdict
import heapq

class Graph:
    def __init__(self, directed=False):
        self.adj = defaultdict(list)
        self.weights = {}
        self.directed = directed
        self.log = []
        self.operation_count = 0

    def add_edge(self, u, v, weight=1):
        """Add an edge from u to v with optional weight"""
        self.adj[u].append(v)
        self.weights[(u, v)] = weight
        
        # If undirected, add reverse edge
        if not self.directed:
            self.adj[v].append(u)
            self.weights[(v, u)] = weight

        self.log.append({
            'op': 'add_edge',
            'from': u,
            'to': v,
            'weight': weight,
            'step': self.operation_count
        })
        self.operation_count += 1

    def remove_edge(self, u, v):
        """Remove an edge from u to v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
            if (u, v) in self.weights:
                del self.weights[(u, v)]
            
            if not self.directed and u in self.adj[v]:
                self.adj[v].remove(u)
                if (v, u) in self.weights:
                    del self.weights[(v, u)]

            self.log.append({
                'op': 'remove_edge',
                'from': u,
                'to': v,
                'step': self.operation_count
            })
            self.operation_count += 1

    def add_vertex(self, vertex):
        """Add a vertex to the graph"""
        if vertex not in self.adj:
            self.adj[vertex] = []
            self.log.append({
                'op': 'add_vertex',
                'vertex': vertex,
                'step': self.operation_count
            })
            self.operation_count += 1

    def remove_vertex(self, vertex):
        """Remove a vertex and all its edges"""
        if vertex in self.adj:
            # Remove all edges to this vertex
            for u in list(self.adj.keys()):
                if vertex in self.adj[u]:
                    self.adj[u].remove(vertex)
                    if (u, vertex) in self.weights:
                        del self.weights[(u, vertex)]
            
            # Remove the vertex
            del self.adj[vertex]
            
            self.log.append({
                'op': 'remove_vertex',
                'vertex': vertex,
                'step': self.operation_count
            })
            self.operation_count += 1

    def bfs(self, start):
        """Breadth-First Search from start vertex"""
        self.log.append({
            'op': 'bfs_start',
            'start': start,
            'step': self.operation_count
        })
        self.operation_count += 1

        if start not in self.adj:
            return []

        visited = set()
        queue = deque([start])
        visited.add(start)
        result = [start]

        while queue:
            vertex = queue.popleft()
            
            self.log.append({
                'op': 'bfs_visit',
                'vertex': vertex,
                'step': self.operation_count
            })
            self.operation_count += 1

            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    result.append(neighbor)
                    
                    self.log.append({
                        'op': 'bfs_discover',
                        'from': vertex,
                        'to': neighbor,
                        'step': self.operation_count
                    })
                    self.operation_count += 1

        self.log.append({
            'op': 'bfs_complete',
            'result': result,
            'step': self.operation_count
        })
        self.operation_count += 1

        return result

    def dfs(self, start):
        """Depth-First Search from start vertex"""
        self.log.append({
            'op': 'dfs_start',
            'start': start,
            'step': self.operation_count
        })
        self.operation_count += 1

        if start not in self.adj:
            return []

        visited = set()
        result = []

        def dfs_recursive(vertex):
            visited.add(vertex)
            result.append(vertex)
            
            self.log.append({
                'op': 'dfs_visit',
                'vertex': vertex,
                'step': self.operation_count
            })
            self.operation_count += 1

            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    self.log.append({
                        'op': 'dfs_discover',
                        'from': vertex,
                        'to': neighbor,
                        'step': self.operation_count
                    })
                    self.operation_count += 1
                    dfs_recursive(neighbor)

        dfs_recursive(start)

        self.log.append({
            'op': 'dfs_complete',
            'result': result,
            'step': self.operation_count
        })
        self.operation_count += 1

        return result

    def dijkstra(self, start, end=None):
        """Dijkstra's shortest path algorithm"""
        self.log.append({
            'op': 'dijkstra_start',
            'start': start,
            'end': end,
            'step': self.operation_count
        })
        self.operation_count += 1

        if start not in self.adj:
            return {}

        distances = {vertex: float('infinity') for vertex in self.adj}
        distances[start] = 0
        previous = {}
        pq = [(0, start)]
        visited = set()

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)
            
            if current_vertex in visited:
                continue

            visited.add(current_vertex)
            
            self.log.append({
                'op': 'dijkstra_visit',
                'vertex': current_vertex,
                'distance': current_distance,
                'step': self.operation_count
            })
            self.operation_count += 1

            for neighbor in self.adj[current_vertex]:
                weight = self.weights.get((current_vertex, neighbor), 1)
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))
                    
                    self.log.append({
                        'op': 'dijkstra_relax',
                        'from': current_vertex,
                        'to': neighbor,
                        'new_distance': distance,
                        'step': self.operation_count
                    })
                    self.operation_count += 1

            if end and current_vertex == end:
                break

        self.log.append({
            'op': 'dijkstra_complete',
            'distances': distances,
            'step': self.operation_count
        })
        self.operation_count += 1

        return distances, previous

    def get_shortest_path(self, start, end):
        """Get the shortest path from start to end"""
        distances, previous = self.dijkstra(start, end)
        
        if distances[end] == float('infinity'):
            return None

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()

        self.log.append({
            'op': 'shortest_path',
            'start': start,
            'end': end,
            'path': path,
            'distance': distances[end],
            'step': self.operation_count
        })
        self.operation_count += 1

        return path, distances[end]

    def has_cycle(self):
        """Check if the graph has a cycle using DFS"""
        self.log.append({
            'op': 'cycle_detection_start',
            'step': self.operation_count
        })
        self.operation_count += 1

        visited = set()
        rec_stack = set()

        def has_cycle_dfs(vertex):
            visited.add(vertex)
            rec_stack.add(vertex)
            
            self.log.append({
                'op': 'cycle_dfs_visit',
                'vertex': vertex,
                'step': self.operation_count
            })
            self.operation_count += 1

            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    if has_cycle_dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    self.log.append({
                        'op': 'cycle_found',
                        'vertex': vertex,
                        'neighbor': neighbor,
                        'step': self.operation_count
                    })
                    self.operation_count += 1
                    return True

            rec_stack.remove(vertex)
            return False

        for vertex in self.adj:
            if vertex not in visited:
                if has_cycle_dfs(vertex):
                    self.log.append({
                        'op': 'cycle_detection_complete',
                        'result': True,
                        'step': self.operation_count
                    })
                    self.operation_count += 1
                    return True

        self.log.append({
            'op': 'cycle_detection_complete',
            'result': False,
            'step': self.operation_count
        })
        self.operation_count += 1
        return False

    def topological_sort(self):
        """Topological sort using DFS (only for DAGs)"""
        self.log.append({
            'op': 'topological_sort_start',
            'step': self.operation_count
        })
        self.operation_count += 1

        if not self.directed:
            return None

        visited = set()
        temp_visited = set()
        result = []

        def topological_dfs(vertex):
            if vertex in temp_visited:
                return False  # Cycle detected
            if vertex in visited:
                return True

            temp_visited.add(vertex)
            
            self.log.append({
                'op': 'topological_dfs_visit',
                'vertex': vertex,
                'step': self.operation_count
            })
            self.operation_count += 1

            for neighbor in self.adj[vertex]:
                if not topological_dfs(neighbor):
                    return False

            temp_visited.remove(vertex)
            visited.add(vertex)
            result.append(vertex)
            return True

        for vertex in self.adj:
            if vertex not in visited:
                if not topological_dfs(vertex):
                    self.log.append({
                        'op': 'topological_sort_cycle',
                        'step': self.operation_count
                    })
                    self.operation_count += 1
                    return None

        result.reverse()
        
        self.log.append({
            'op': 'topological_sort_complete',
            'result': result,
            'step': self.operation_count
        })
        self.operation_count += 1

        return result

    def get_adjacency_matrix(self):
        """Get adjacency matrix representation"""
        vertices = list(self.adj.keys())
        n = len(vertices)
        matrix = [[0] * n for _ in range(n)]
        
        for i, u in enumerate(vertices):
            for j, v in enumerate(vertices):
                if v in self.adj[u]:
                    matrix[i][j] = self.weights.get((u, v), 1)

        return matrix, vertices

    def get_degree(self, vertex):
        """Get the degree of a vertex"""
        if vertex not in self.adj:
            return 0
        return len(self.adj[vertex])

    def is_connected(self):
        """Check if the graph is connected"""
        if not self.adj:
            return True
        
        start_vertex = next(iter(self.adj))
        visited = set()
        
        def dfs_connected(vertex):
            visited.add(vertex)
            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    dfs_connected(neighbor)
        
        dfs_connected(start_vertex)
        return len(visited) == len(self.adj)

    def get_connected_components(self):
        """Get all connected components"""
        visited = set()
        components = []

        def dfs_component(vertex, component):
            visited.add(vertex)
            component.append(vertex)
            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    dfs_component(neighbor, component)

        for vertex in self.adj:
            if vertex not in visited:
                component = []
                dfs_component(vertex, component)
                components.append(component)

        return components

    def step(self):
        """Return the next operation for visualization"""
        if self.log:
            return self.log.pop(0)
        return None

    def reset(self):
        """Reset the graph and operation log"""
        self.adj.clear()
        self.weights.clear()
        self.log = []
        self.operation_count = 0

    def get_statistics(self):
        """Get graph statistics"""
        total_edges = sum(len(neighbors) for neighbors in self.adj.values())
        if not self.directed:
            total_edges //= 2
        
        return {
            'vertices': len(self.adj),
            'edges': total_edges,
            'directed': self.directed,
            'operations_performed': self.operation_count
        } 