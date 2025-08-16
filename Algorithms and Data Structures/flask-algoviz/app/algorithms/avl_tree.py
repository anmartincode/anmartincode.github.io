class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.parent = None

class AVLTree:
    def __init__(self):
        self.root = None
        self.log = []
        self.operation_count = 0

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if node is not None:
            node.height = max(self.height(node.left), self.height(node.right)) + 1

    def right_rotate(self, y):
        """Right rotation for AVL tree balancing"""
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update parent pointers
        if T2:
            T2.parent = y
        x.parent = y.parent
        y.parent = x

        # Update heights
        self.update_height(y)
        self.update_height(x)

        # Log the rotation
        self.log.append({
            'op': 'rotate_right',
            'node': y.key,
            'new_root': x.key,
            'step': self.operation_count
        })
        self.operation_count += 1

        return x

    def left_rotate(self, x):
        """Left rotation for AVL tree balancing"""
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update parent pointers
        if T2:
            T2.parent = x
        y.parent = x.parent
        x.parent = y

        # Update heights
        self.update_height(x)
        self.update_height(y)

        # Log the rotation
        self.log.append({
            'op': 'rotate_left',
            'node': x.key,
            'new_root': y.key,
            'step': self.operation_count
        })
        self.operation_count += 1

        return y

    def insert(self, key):
        """Insert a new key into the AVL tree"""
        self.log.append({
            'op': 'insert_start',
            'value': key,
            'step': self.operation_count
        })
        self.operation_count += 1

        self.root = self._insert_recursive(self.root, key)
        
        self.log.append({
            'op': 'insert_complete',
            'value': key,
            'step': self.operation_count
        })
        self.operation_count += 1

    def _insert_recursive(self, node, key):
        """Recursive helper for insert operation"""
        # Standard BST insert
        if node is None:
            new_node = AVLNode(key)
            self.log.append({
                'op': 'create_node',
                'value': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            return new_node

        if key < node.key:
            self.log.append({
                'op': 'traverse_left',
                'current': node.key,
                'target': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            node.left = self._insert_recursive(node.left, key)
            if node.left:
                node.left.parent = node
        elif key > node.key:
            self.log.append({
                'op': 'traverse_right',
                'current': node.key,
                'target': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            node.right = self._insert_recursive(node.right, key)
            if node.right:
                node.right.parent = node
        else:
            # Duplicate key - log but don't insert
            self.log.append({
                'op': 'duplicate_key',
                'value': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            return node

        # Update height of current node
        self.update_height(node)

        # Get balance factor
        balance = self.balance_factor(node)

        # Log balance check
        self.log.append({
            'op': 'check_balance',
            'node': node.key,
            'balance': balance,
            'step': self.operation_count
        })
        self.operation_count += 1

        # Left Left Case
        if balance > 1 and key < node.left.key:
            self.log.append({
                'op': 'balance_left_left',
                'node': node.key,
                'step': self.operation_count
            })
            self.operation_count += 1
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            self.log.append({
                'op': 'balance_right_right',
                'node': node.key,
                'step': self.operation_count
            })
            self.operation_count += 1
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            self.log.append({
                'op': 'balance_left_right',
                'node': node.key,
                'step': self.operation_count
            })
            self.operation_count += 1
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            self.log.append({
                'op': 'balance_right_left',
                'node': node.key,
                'step': self.operation_count
            })
            self.operation_count += 1
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, key):
        """Delete a key from the AVL tree"""
        self.log.append({
            'op': 'delete_start',
            'value': key,
            'step': self.operation_count
        })
        self.operation_count += 1

        self.root = self._delete_recursive(self.root, key)
        
        self.log.append({
            'op': 'delete_complete',
            'value': key,
            'step': self.operation_count
        })
        self.operation_count += 1

    def _delete_recursive(self, node, key):
        """Recursive helper for delete operation"""
        if node is None:
            self.log.append({
                'op': 'key_not_found',
                'value': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            return node

        if key < node.key:
            self.log.append({
                'op': 'delete_traverse_left',
                'current': node.key,
                'target': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            self.log.append({
                'op': 'delete_traverse_right',
                'current': node.key,
                'target': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node to be deleted found
            self.log.append({
                'op': 'delete_node_found',
                'value': key,
                'step': self.operation_count
            })
            self.operation_count += 1

            # Node with only one child or no child
            if node.left is None:
                temp = node.right
                if temp:
                    temp.parent = node.parent
                return temp
            elif node.right is None:
                temp = node.left
                if temp:
                    temp.parent = node.parent
                return temp

            # Node with two children: get inorder successor
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete_recursive(node.right, temp.key)

        if node is None:
            return node

        # Update height
        self.update_height(node)

        # Get balance factor
        balance = self.balance_factor(node)

        # Log balance check
        self.log.append({
            'op': 'delete_check_balance',
            'node': node.key,
            'balance': balance,
            'step': self.operation_count
        })
        self.operation_count += 1

        # Left Left Case
        if balance > 1 and self.balance_factor(node.left) >= 0:
            return self.right_rotate(node)

        # Left Right Case
        if balance > 1 and self.balance_factor(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and self.balance_factor(node.right) <= 0:
            return self.left_rotate(node)

        # Right Left Case
        if balance < -1 and self.balance_factor(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def _get_min_value_node(self, node):
        """Get the node with minimum value in the subtree"""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, key):
        """Search for a key in the AVL tree"""
        self.log.append({
            'op': 'search_start',
            'value': key,
            'step': self.operation_count
        })
        self.operation_count += 1

        result = self._search_recursive(self.root, key)
        
        if result:
            self.log.append({
                'op': 'search_found',
                'value': key,
                'step': self.operation_count
            })
        else:
            self.log.append({
                'op': 'search_not_found',
                'value': key,
                'step': self.operation_count
            })
        self.operation_count += 1

        return result

    def _search_recursive(self, node, key):
        """Recursive helper for search operation"""
        if node is None or node.key == key:
            return node

        if key < node.key:
            self.log.append({
                'op': 'search_traverse_left',
                'current': node.key,
                'target': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            return self._search_recursive(node.left, key)
        else:
            self.log.append({
                'op': 'search_traverse_right',
                'current': node.key,
                'target': key,
                'step': self.operation_count
            })
            self.operation_count += 1
            return self._search_recursive(node.right, key)

    def inorder_traversal(self):
        """Perform inorder traversal of the tree"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """Recursive helper for inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def get_tree_structure(self):
        """Get the tree structure for visualization"""
        if not self.root:
            return None
        
        def build_structure(node):
            if node is None:
                return None
            
            return {
                'key': node.key,
                'height': node.height,
                'balance': self.balance_factor(node),
                'left': build_structure(node.left),
                'right': build_structure(node.right)
            }
        
        return build_structure(self.root)

    def step(self):
        """Return the next operation for visualization"""
        if self.log:
            return self.log.pop(0)
        return None 

    def reset(self):
        """Reset the tree and operation log"""
        self.root = None
        self.log = []
        self.operation_count = 0

    def get_statistics(self):
        """Get tree statistics"""
        def count_nodes(node):
            if node is None:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)

        def get_max_height(node):
            if node is None:
                return 0
            return max(get_max_height(node.left), get_max_height(node.right)) + 1

        return {
            'total_nodes': count_nodes(self.root),
            'height': get_max_height(self.root),
            'operations_performed': self.operation_count
        } 