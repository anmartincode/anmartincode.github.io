class Graph:
    def __init__(self):
        self.adj = {}
        self.log = []

    def add_edge(self, u, v):
        self.adj.setdefault(u, []).append(v)
        self.log.append({'op': 'add_edge', 'from': u, 'to': v})

    def step(self):
        if self.log:
            return self.log.pop(0)
        return None 