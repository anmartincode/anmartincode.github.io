#!/usr/bin/env python3
"""
Enhanced Data Structures Implementation
Includes Red-Black Trees, B-Trees, Skip Lists, Tries, and Disjoint Sets
"""

from typing import Optional, List, Any, Dict, Tuple
from enum import Enum
import random
import math

class Color(Enum):
    """Color enum for Red-Black Tree nodes"""
    RED = "red"
    BLACK = "black"

class RedBlackTreeNode:
    """Node class for Red-Black Tree"""
    
    def __init__(self, key: Any, color: Color = Color.RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    """Red-Black Tree implementation with self-balancing properties"""
    
    def __init__(self):
        self.nil = RedBlackTreeNode(None, Color.BLACK)
        self.root = self.nil
    
    def insert(self, key: Any) -> None:
        """Insert a key into the Red-Black Tree"""
        node = RedBlackTreeNode(key)
        node.left = self.nil
        node.right = self.nil
        
        y = None
        x = self.root
        
        # Find insertion position
        while x != self.nil:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        
        node.parent = y
        
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        
        # Fix Red-Black Tree properties
        self._fix_insert(node)
    
    def _fix_insert(self, node: RedBlackTreeNode) -> None:
        """Fix Red-Black Tree properties after insertion"""
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                if y.color == Color.RED:
                    node.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                y = node.parent.parent.left
                if y.color == Color.RED:
                    node.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)
        
        self.root.color = Color.BLACK
    
    def _left_rotate(self, x: RedBlackTreeNode) -> None:
        """Left rotation operation"""
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    
    def _right_rotate(self, x: RedBlackTreeNode) -> None:
        """Right rotation operation"""
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    
    def inorder_traversal(self) -> List[Any]:
        """Perform inorder traversal of the tree"""
        result = []
        self._inorder_helper(self.root, result)
        return result
    
    def _inorder_helper(self, node: RedBlackTreeNode, result: List[Any]) -> None:
        """Helper function for inorder traversal"""
        if node != self.nil:
            self._inorder_helper(node.left, result)
            result.append(node.key)
            self._inorder_helper(node.right, result)

class BTreeNode:
    """Node class for B-Tree"""
    
    def __init__(self, leaf: bool = True):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    """B-Tree implementation for database indexing"""
    
    def __init__(self, degree: int = 3):
        self.root = BTreeNode()
        self.degree = degree
        self.min_keys = degree - 1
        self.max_keys = 2 * degree - 1
    
    def insert(self, key: Any) -> None:
        """Insert a key into the B-Tree"""
        root = self.root
        
        # If root is full, split it
        if len(root.keys) == self.max_keys:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        
        self._insert_non_full(self.root, key)
    
    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Insert key into a non-full node"""
        i = len(node.keys) - 1
        
        if node.leaf:
            # Insert into leaf node
            while i >= 0 and key < node.keys[i]:
                node.keys.insert(i + 1, node.keys[i])
                i -= 1
            node.keys.insert(i + 1, key)
        else:
            # Find child to insert into
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            # Split child if full
            if len(node.children[i].keys) == self.max_keys:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            
            self._insert_non_full(node.children[i], key)
    
    def _split_child(self, parent: BTreeNode, child_index: int) -> None:
        """Split a full child node"""
        child = parent.children[child_index]
        new_node = BTreeNode(leaf=child.leaf)
        
        # Move keys
        mid = len(child.keys) // 2
        parent.keys.insert(child_index, child.keys[mid])
        new_node.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]
        
        # Move children if not leaf
        if not child.leaf:
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]
        
        parent.children.insert(child_index + 1, new_node)
    
    def traverse(self) -> List[Any]:
        """Traverse the B-Tree in order"""
        result = []
        self._traverse_helper(self.root, result)
        return result
    
    def _traverse_helper(self, node: BTreeNode, result: List[Any]) -> None:
        """Helper function for traversal"""
        if node is None:
            return
        
        for i in range(len(node.keys)):
            if not node.leaf:
                self._traverse_helper(node.children[i], result)
            result.append(node.keys[i])
        
        if not node.leaf:
            self._traverse_helper(node.children[-1], result)

class SkipListNode:
    """Node class for Skip List"""
    
    def __init__(self, key: Any, level: int):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    """Skip List implementation with probabilistic structure"""
    
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = SkipListNode(None, max_level)
    
    def _random_level(self) -> int:
        """Generate random level for a new node"""
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level
    
    def insert(self, key: Any) -> None:
        """Insert a key into the Skip List"""
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # Find position to insert
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        # If key already exists, update it
        if current and current.key == key:
            current.key = key
            return
        
        # Generate random level for new node
        new_level = self._random_level()
        
        # Update max level if necessary
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        
        # Create new node
        new_node = SkipListNode(key, new_level)
        
        # Update forward pointers
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
    
    def search(self, key: Any) -> Optional[SkipListNode]:
        """Search for a key in the Skip List"""
        current = self.header
        
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        
        current = current.forward[0]
        
        if current and current.key == key:
            return current
        return None
    
    def delete(self, key: Any) -> bool:
        """Delete a key from the Skip List"""
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # Find position to delete
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        # If key not found
        if not current or current.key != key:
            return False
        
        # Update forward pointers
        for i in range(self.level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]
        
        # Update max level
        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1
        
        return True
    
    def to_list(self) -> List[Any]:
        """Convert Skip List to sorted list"""
        result = []
        current = self.header.forward[0]
        while current:
            result.append(current.key)
            current = current.forward[0]
        return result

class TrieNode:
    """Node class for Trie"""
    
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

class Trie:
    """Trie data structure for efficient string operations"""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the Trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += 1
    
    def search(self, word: str) -> bool:
        """Search for a word in the Trie"""
        node = self._search_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with the given prefix"""
        return self._search_node(prefix) is not None
    
    def _search_node(self, word: str) -> Optional[TrieNode]:
        """Search for a node corresponding to the word"""
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def autocomplete(self, prefix: str, max_suggestions: int = 10) -> List[str]:
        """Get autocomplete suggestions for a prefix"""
        suggestions = []
        node = self._search_node(prefix)
        
        if node:
            self._collect_words(node, prefix, suggestions, max_suggestions)
        
        # Sort by frequency (most frequent first)
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [word for word, freq in suggestions[:max_suggestions]]
    
    def _collect_words(self, node: TrieNode, prefix: str, suggestions: List[Tuple[str, int]], max_count: int) -> None:
        """Collect words from a node"""
        if len(suggestions) >= max_count:
            return
        
        if node.is_end_of_word:
            suggestions.append((prefix, node.frequency))
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, suggestions, max_count)
    
    def get_all_words(self) -> List[str]:
        """Get all words in the Trie"""
        words = []
        self._collect_words(self.root, "", words, float('inf'))
        return [word for word, freq in words]

class DisjointSet:
    """Disjoint Set (Union-Find) data structure"""
    
    def __init__(self):
        self.parent = {}
        self.rank = {}
        self.size = {}
    
    def make_set(self, x: Any) -> None:
        """Create a new set containing element x"""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.size[x] = 1
    
    def find(self, x: Any) -> Any:
        """Find the representative of the set containing x"""
        if x not in self.parent:
            return None
        
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: Any, y: Any) -> None:
        """Union the sets containing x and y"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x is None or root_y is None:
            return
        
        if root_x == root_y:
            return
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
    
    def get_set_size(self, x: Any) -> int:
        """Get the size of the set containing x"""
        root = self.find(x)
        return self.size.get(root, 0) if root else 0
    
    def get_sets(self) -> Dict[Any, List[Any]]:
        """Get all sets as a dictionary mapping representatives to elements"""
        sets = {}
        for element in self.parent:
            root = self.find(element)
            if root not in sets:
                sets[root] = []
            sets[root].append(element)
        return sets
    
    def count_sets(self) -> int:
        """Count the number of disjoint sets"""
        return len(set(self.find(x) for x in self.parent))

# Example usage and testing
def test_enhanced_structures():
    """Test all enhanced data structures"""
    print("Testing Enhanced Data Structures")
    print("=" * 40)
    
    # Test Red-Black Tree
    print("\n1. Testing Red-Black Tree:")
    rb_tree = RedBlackTree()
    test_data = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
    for item in test_data:
        rb_tree.insert(item)
    print(f"Red-Black Tree inorder: {rb_tree.inorder_traversal()}")
    
    # Test B-Tree
    print("\n2. Testing B-Tree:")
    b_tree = BTree(degree=3)
    for item in test_data:
        b_tree.insert(item)
    print(f"B-Tree traversal: {b_tree.traverse()}")
    
    # Test Skip List
    print("\n3. Testing Skip List:")
    skip_list = SkipList()
    for item in test_data:
        skip_list.insert(item)
    print(f"Skip List: {skip_list.to_list()}")
    print(f"Search for 10: {skip_list.search(10) is not None}")
    
    # Test Trie
    print("\n4. Testing Trie:")
    trie = Trie()
    words = ["hello", "world", "help", "hero", "heroic", "heroism"]
    for word in words:
        trie.insert(word)
    print(f"Search 'hello': {trie.search('hello')}")
    print(f"Starts with 'he': {trie.starts_with('he')}")
    print(f"Autocomplete 'he': {trie.autocomplete('he')}")
    
    # Test Disjoint Set
    print("\n5. Testing Disjoint Set:")
    ds = DisjointSet()
    for i in range(10):
        ds.make_set(i)
    
    ds.union(1, 2)
    ds.union(2, 3)
    ds.union(4, 5)
    ds.union(6, 7)
    ds.union(5, 6)
    
    print(f"Find(1): {ds.find(1)}")
    print(f"Find(4): {ds.find(4)}")
    print(f"Find(7): {ds.find(7)}")
    print(f"Number of sets: {ds.count_sets()}")
    print(f"Set sizes: {[ds.get_set_size(i) for i in range(10)]}")

if __name__ == "__main__":
    test_enhanced_structures()
