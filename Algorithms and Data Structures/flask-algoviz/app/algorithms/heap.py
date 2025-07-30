class Heap:
    def __init__(self, min_heap=True):
        self.data = []
        self.min_heap = min_heap
        self.log = []

    def insert(self, value):
        # Placeholder for heap insert logic
        self.log.append({'op': 'insert', 'value': value})

    def step(self):
        if self.log:
            return self.log.pop(0)
        return None 