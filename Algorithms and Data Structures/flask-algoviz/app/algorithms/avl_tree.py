class AVLTree:
    def __init__(self):
        self.root = None
        self.log = []

    def insert(self, value):
        # Placeholder for AVL insert logic
        self.log.append({'op': 'insert', 'value': value})

    def step(self):
        # Return the next operation for visualization
        if self.log:
            return self.log.pop(0)
        return None 