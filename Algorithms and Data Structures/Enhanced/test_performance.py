#!/usr/bin/env python3
"""
Test script to verify B-tree performance improvements
"""

import time
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_structures import BTree

def test_b_tree_performance(data_sizes=[10, 50, 100, 500, 1000]):
    """Test B-tree performance with different data sizes"""
    print("B-Tree Performance Test")
    print("=" * 40)
    
    for size in data_sizes:
        print(f"\nTesting with {size} elements...")
        
        # Create test data (reverse sorted for worst case)
        test_data = list(range(size, 0, -1))
        
        # Test B-tree insertion
        start_time = time.time()
        tree = BTree(degree=3)
        
        try:
            for item in test_data:
                tree.insert(item)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Verify the tree contains all elements
            result = tree.traverse()
            expected = sorted(test_data)
            
            if result == expected:
                print(f"✓ B-tree with {size} elements: {execution_time:.4f}s")
            else:
                print(f"✗ B-tree with {size} elements: CORRUPTED DATA")
                print(f"  Expected: {expected[:10]}...")
                print(f"  Got: {result[:10]}...")
                
        except Exception as e:
            print(f"✗ B-tree with {size} elements: ERROR - {e}")

def test_comparison_with_builtin(data_sizes=[10, 50, 100, 500, 1000]):
    """Compare B-tree performance with Python's built-in sorted"""
    print("\nB-Tree vs Built-in Sorted Comparison")
    print("=" * 40)
    
    for size in data_sizes:
        print(f"\nTesting with {size} elements...")
        
        # Create test data
        test_data = list(range(size, 0, -1))
        
        # Test B-tree
        start_time = time.time()
        tree = BTree(degree=3)
        for item in test_data:
            tree.insert(item)
        btree_result = tree.traverse()
        btree_time = time.time() - start_time
        
        # Test built-in sorted
        start_time = time.time()
        sorted_result = sorted(test_data)
        sorted_time = time.time() - start_time
        
        print(f"B-tree: {btree_time:.4f}s")
        print(f"Built-in sorted: {sorted_time:.4f}s")
        if sorted_time > 0:
            print(f"Ratio (B-tree/sorted): {btree_time/sorted_time:.1f}x")
        else:
            print("Ratio: Both too fast to measure accurately")

if __name__ == "__main__":
    print("Testing B-tree performance improvements...")
    
    # Test basic functionality
    test_b_tree_performance()
    
    # Test comparison with built-in
    test_comparison_with_builtin()
    
    print("\n" + "=" * 40)
    print("Performance test completed!")
    print("If all tests pass, the B-tree implementation is working correctly.")
