class Heap:
    def __init__(self, min_heap=True):
        self.data = []
        self.min_heap = min_heap
        self.log = []
        self.operation_count = 0

    def parent(self, index):
        """Get parent index of a given index"""
        return (index - 1) // 2

    def left_child(self, index):
        """Get left child index of a given index"""
        return 2 * index + 1

    def right_child(self, index):
        """Get right child index of a given index"""
        return 2 * index + 2

    def has_parent(self, index):
        """Check if a node has a parent"""
        return self.parent(index) >= 0

    def has_left_child(self, index):
        """Check if a node has a left child"""
        return self.left_child(index) < len(self.data)

    def has_right_child(self, index):
        """Check if a node has a right child"""
        return self.right_child(index) < len(self.data)

    def swap(self, index1, index2):
        """Swap two elements in the heap"""
        self.data[index1], self.data[index2] = self.data[index2], self.data[index1]
        
        self.log.append({
            'op': 'swap',
            'index1': index1,
            'index2': index2,
            'value1': self.data[index1],
            'value2': self.data[index2],
            'step': self.operation_count
        })
        self.operation_count += 1

    def peek(self):
        """Get the root element without removing it"""
        if len(self.data) == 0:
            return None
        
        self.log.append({
            'op': 'peek',
            'value': self.data[0],
            'step': self.operation_count
        })
        self.operation_count += 1
        
        return self.data[0]

    def size(self):
        """Get the size of the heap"""
        return len(self.data)

    def is_empty(self):
        """Check if the heap is empty"""
        return len(self.data) == 0

    def insert(self, value):
        """Insert a new value into the heap"""
        self.log.append({
            'op': 'insert_start',
            'value': value,
            'step': self.operation_count
        })
        self.operation_count += 1

        # Add the new element to the end
        self.data.append(value)
        
        self.log.append({
            'op': 'insert_append',
            'value': value,
            'index': len(self.data) - 1,
            'step': self.operation_count
        })
        self.operation_count += 1

        # Bubble up the new element
        self._bubble_up(len(self.data) - 1)
        
        self.log.append({
            'op': 'insert_complete',
            'value': value,
            'step': self.operation_count
        })
        self.operation_count += 1

    def _bubble_up(self, index):
        """Bubble up an element to maintain heap property"""
        while self.has_parent(index):
            parent_index = self.parent(index)
            
            # For min heap: if current is smaller than parent, swap
            # For max heap: if current is larger than parent, swap
            should_swap = (self.min_heap and self.data[index] < self.data[parent_index]) or \
                         (not self.min_heap and self.data[index] > self.data[parent_index])
            
            if should_swap:
                self.log.append({
                    'op': 'bubble_up_compare',
                    'current_index': index,
                    'parent_index': parent_index,
                    'current_value': self.data[index],
                    'parent_value': self.data[parent_index],
                    'should_swap': True,
                    'step': self.operation_count
                })
                self.operation_count += 1
                
                self.swap(index, parent_index)
                index = parent_index
            else:
                self.log.append({
                    'op': 'bubble_up_compare',
                    'current_index': index,
                    'parent_index': parent_index,
                    'current_value': self.data[index],
                    'parent_value': self.data[parent_index],
                    'should_swap': False,
                    'step': self.operation_count
                })
                self.operation_count += 1
                break

    def extract(self):
        """Extract the root element from the heap"""
        if self.is_empty():
            self.log.append({
                'op': 'extract_empty',
                'step': self.operation_count
            })
            self.operation_count += 1
            return None

        self.log.append({
            'op': 'extract_start',
            'root_value': self.data[0],
            'step': self.operation_count
        })
        self.operation_count += 1

        # Get the root element
        root = self.data[0]
        
        # Replace root with the last element
        self.data[0] = self.data[-1]
        self.data.pop()
        
        self.log.append({
            'op': 'extract_replace_root',
            'new_root_value': self.data[0] if self.data else None,
            'step': self.operation_count
        })
        self.operation_count += 1

        # Bubble down the new root
        if self.data:
            self._bubble_down(0)
        
        self.log.append({
            'op': 'extract_complete',
            'extracted_value': root,
            'step': self.operation_count
        })
        self.operation_count += 1

        return root

    def _bubble_down(self, index):
        """Bubble down an element to maintain heap property"""
        while self.has_left_child(index):
            # Find the smaller (min heap) or larger (max heap) child
            smaller_child_index = self.left_child(index)
            if self.has_right_child(index):
                right_child_index = self.right_child(index)
                
                # For min heap: choose smaller child
                # For max heap: choose larger child
                if (self.min_heap and self.data[right_child_index] < self.data[smaller_child_index]) or \
                   (not self.min_heap and self.data[right_child_index] > self.data[smaller_child_index]):
                    smaller_child_index = right_child_index

            # Check if we need to swap
            should_swap = (self.min_heap and self.data[index] > self.data[smaller_child_index]) or \
                         (not self.min_heap and self.data[index] < self.data[smaller_child_index])
            
            if should_swap:
                self.log.append({
                    'op': 'bubble_down_compare',
                    'current_index': index,
                    'child_index': smaller_child_index,
                    'current_value': self.data[index],
                    'child_value': self.data[smaller_child_index],
                    'should_swap': True,
                    'step': self.operation_count
                })
                self.operation_count += 1
                
                self.swap(index, smaller_child_index)
                index = smaller_child_index
            else:
                self.log.append({
                    'op': 'bubble_down_compare',
                    'current_index': index,
                    'child_index': smaller_child_index,
                    'current_value': self.data[index],
                    'child_value': self.data[smaller_child_index],
                    'should_swap': False,
                    'step': self.operation_count
                })
                self.operation_count += 1
                break

    def heapify(self, array):
        """Build a heap from an array"""
        self.log.append({
            'op': 'heapify_start',
            'array': array.copy(),
            'step': self.operation_count
        })
        self.operation_count += 1

        self.data = array.copy()
        
        # Start from the last non-leaf node and bubble down
        for i in range(self.parent(len(self.data) - 1), -1, -1):
            self._bubble_down(i)
        
        self.log.append({
            'op': 'heapify_complete',
            'result': self.data.copy(),
            'step': self.operation_count
        })
        self.operation_count += 1

    def heap_sort(self, array):
        """Sort an array using heap sort"""
        self.log.append({
            'op': 'heap_sort_start',
            'array': array.copy(),
            'step': self.operation_count
        })
        self.operation_count += 1

        # Build heap
        self.heapify(array)
        
        # Extract elements one by one
        sorted_array = []
        original_size = len(self.data)
        
        for i in range(original_size):
            sorted_array.append(self.extract())
        
        self.log.append({
            'op': 'heap_sort_complete',
            'result': sorted_array,
            'step': self.operation_count
        })
        self.operation_count += 1
        
        return sorted_array

    def delete(self, index):
        """Delete an element at a specific index"""
        if index >= len(self.data):
            self.log.append({
                'op': 'delete_invalid_index',
                'index': index,
                'step': self.operation_count
            })
            self.operation_count += 1
            return False

        self.log.append({
            'op': 'delete_start',
            'index': index,
            'value': self.data[index],
            'step': self.operation_count
        })
        self.operation_count += 1

        # Replace with the last element
        self.data[index] = self.data[-1]
        self.data.pop()
        
        # If we deleted the last element, we're done
        if index >= len(self.data):
            self.log.append({
                'op': 'delete_complete',
                'step': self.operation_count
            })
            self.operation_count += 1
            return True

        # Bubble up or down as needed
        if self.has_parent(index):
            parent_index = self.parent(index)
            should_bubble_up = (self.min_heap and self.data[index] < self.data[parent_index]) or \
                              (not self.min_heap and self.data[index] > self.data[parent_index])
            
            if should_bubble_up:
                self._bubble_up(index)
            else:
                self._bubble_down(index)
        else:
            self._bubble_down(index)

        self.log.append({
            'op': 'delete_complete',
            'step': self.operation_count
        })
        self.operation_count += 1
        return True

    def change_priority(self, index, new_value):
        """Change the priority of an element at a specific index"""
        if index >= len(self.data):
            self.log.append({
                'op': 'change_priority_invalid_index',
                'index': index,
                'step': self.operation_count
            })
            self.operation_count += 1
            return False

        old_value = self.data[index]
        
        self.log.append({
            'op': 'change_priority_start',
            'index': index,
            'old_value': old_value,
            'new_value': new_value,
            'step': self.operation_count
        })
        self.operation_count += 1

        self.data[index] = new_value
        
        # Determine whether to bubble up or down
        if self.has_parent(index):
            parent_index = self.parent(index)
            should_bubble_up = (self.min_heap and new_value < self.data[parent_index]) or \
                              (not self.min_heap and new_value > self.data[parent_index])
            
            if should_bubble_up:
                self._bubble_up(index)
            else:
                self._bubble_down(index)
        else:
            self._bubble_down(index)

        self.log.append({
            'op': 'change_priority_complete',
            'index': index,
            'old_value': old_value,
            'new_value': new_value,
            'step': self.operation_count
        })
        self.operation_count += 1
        return True

    def get_heap_structure(self):
        """Get the heap structure for visualization"""
        if not self.data:
            return None
        
        def build_tree(index):
            if index >= len(self.data):
                return None
            
            return {
                'value': self.data[index],
                'index': index,
                'left': build_tree(self.left_child(index)),
                'right': build_tree(self.right_child(index))
            }
        
        return build_tree(0)

    def step(self):
        """Return the next operation for visualization"""
        if self.log:
            return self.log.pop(0)
        return None

    def reset(self):
        """Reset the heap and operation log"""
        self.data = []
        self.log = []
        self.operation_count = 0

    def get_statistics(self):
        """Get heap statistics"""
        return {
            'size': len(self.data),
            'type': 'min' if self.min_heap else 'max',
            'operations_performed': self.operation_count,
            'height': self._calculate_height()
        }

    def _calculate_height(self):
        """Calculate the height of the heap"""
        if not self.data:
            return 0
        return len(bin(len(self.data))) - 2  # log2(n) + 1 