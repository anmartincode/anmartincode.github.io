#!/usr/bin/env python3
"""
Enhanced Algorithms Implementation
Includes advanced sorting, searching, and graph algorithms with performance analysis
"""

import time
import random
import heapq
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from collections import defaultdict, deque
import numpy as np
import matplotlib.pyplot as plt

@dataclass
class AlgorithmResult:
    """Data class for algorithm execution results"""
    algorithm_name: str
    execution_time: float
    memory_usage: float
    input_size: int
    operations_count: int
    result: Any
    complexity: str

class AdvancedSortingAlgorithms:
    """Advanced sorting algorithms with performance tracking"""
    
    @staticmethod
    def quicksort_optimized(arr: List[Any], operations_counter: List[int] = None) -> List[Any]:
        """Optimized quicksort with median-of-three pivot selection"""
        if operations_counter is None:
            operations_counter = [0]
        
        def partition(low: int, high: int) -> int:
            # Median-of-three pivot selection
            mid = (low + high) // 2
            pivot_candidates = [arr[low], arr[mid], arr[high]]
            pivot_candidates.sort()
            pivot = pivot_candidates[1]
            
            # Find pivot index
            if pivot == arr[low]:
                pivot_idx = low
            elif pivot == arr[mid]:
                pivot_idx = mid
            else:
                pivot_idx = high
            
            # Swap pivot to end
            arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
            pivot = arr[high]
            
            i = low - 1
            for j in range(low, high):
                operations_counter[0] += 1
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        def quicksort_helper(low: int, high: int):
            if low < high:
                pi = partition(low, high)
                quicksort_helper(low, pi - 1)
                quicksort_helper(pi + 1, high)
        
        quicksort_helper(0, len(arr) - 1)
        return arr
    
    @staticmethod
    def mergesort_optimized(arr: List[Any], operations_counter: List[int] = None) -> List[Any]:
        """Optimized mergesort with in-place merging for small arrays"""
        if operations_counter is None:
            operations_counter = [0]
        
        def merge(left: List[Any], right: List[Any]) -> List[Any]:
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                operations_counter[0] += 1
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        if len(arr) <= 1:
            return arr
        
        # Use insertion sort for small arrays
        if len(arr) <= 10:
            return AdvancedSortingAlgorithms.insertion_sort(arr, operations_counter)
        
        mid = len(arr) // 2
        left = AdvancedSortingAlgorithms.mergesort_optimized(arr[:mid], operations_counter)
        right = AdvancedSortingAlgorithms.mergesort_optimized(arr[mid:], operations_counter)
        
        return merge(left, right)
    
    @staticmethod
    def heapsort_optimized(arr: List[Any], operations_counter: List[int] = None) -> List[Any]:
        """Optimized heapsort with bottom-up heap construction"""
        if operations_counter is None:
            operations_counter = [0]
        
        def heapify(arr: List[Any], n: int, i: int):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n:
                operations_counter[0] += 1
                if arr[left] > arr[largest]:
                    largest = left
            
            if right < n:
                operations_counter[0] += 1
                if arr[right] > arr[largest]:
                    largest = right
            
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)
        
        n = len(arr)
        
        # Build max heap (bottom-up approach)
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
        
        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            heapify(arr, i, 0)
        
        return arr
    
    @staticmethod
    def insertion_sort(arr: List[Any], operations_counter: List[int] = None) -> List[Any]:
        """Insertion sort for small arrays"""
        if operations_counter is None:
            operations_counter = [0]
        
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0:
                operations_counter[0] += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    j -= 1
                else:
                    break
            arr[j + 1] = key
        
        return arr
    
    @staticmethod
    def timsort(arr: List[Any], operations_counter: List[int] = None) -> List[Any]:
        """Timsort implementation (Python's built-in sort algorithm)"""
        if operations_counter is None:
            operations_counter = [0]
        
        # This is a simplified version - Python's actual timsort is more complex
        return AdvancedSortingAlgorithms.mergesort_optimized(arr, operations_counter)

class AdvancedSearchingAlgorithms:
    """Advanced searching algorithms"""
    
    @staticmethod
    def binary_search_optimized(arr: List[Any], target: Any, operations_counter: List[int] = None) -> Optional[int]:
        """Optimized binary search with early termination"""
        if operations_counter is None:
            operations_counter = [0]
        
        left, right = 0, len(arr) - 1
        
        while left <= right:
            operations_counter[0] += 1
            mid = left + (right - left) // 2  # Avoid overflow
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return None
    
    @staticmethod
    def interpolation_search(arr: List[Any], target: Any, operations_counter: List[int] = None) -> Optional[int]:
        """Interpolation search for uniformly distributed data"""
        if operations_counter is None:
            operations_counter = [0]
        
        left, right = 0, len(arr) - 1
        
        while left <= right and target >= arr[left] and target <= arr[right]:
            operations_counter[0] += 1
            
            if left == right:
                if arr[left] == target:
                    return left
                return None
            
            # Interpolation formula
            pos = left + int(((right - left) * (target - arr[left])) / (arr[right] - arr[left]))
            
            if arr[pos] == target:
                return pos
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        return None
    
    @staticmethod
    def exponential_search(arr: List[Any], target: Any, operations_counter: List[int] = None) -> Optional[int]:
        """Exponential search for unbounded arrays"""
        if operations_counter is None:
            operations_counter = [0]
        
        if arr[0] == target:
            return 0
        
        i = 1
        while i < len(arr) and arr[i] <= target:
            operations_counter[0] += 1
            i = i * 2
        
        # Binary search in the range [i/2, min(i, len(arr)-1)]
        return AdvancedSearchingAlgorithms.binary_search_optimized(
            arr[i//2:min(i, len(arr))], target, operations_counter
        )

class GraphAlgorithms:
    """Advanced graph algorithms"""
    
    def __init__(self):
        self.graph = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, u: Any, v: Any, weight: float = 1.0):
        """Add a weighted edge to the graph"""
        self.graph[u].append(v)
        self.weights[(u, v)] = weight
    
    def dijkstra_shortest_path(self, start: Any, end: Any) -> Tuple[List[Any], float]:
        """Dijkstra's shortest path algorithm with priority queue"""
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        previous = {}
        
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == end:
                break
            
            for neighbor in self.graph[current_node]:
                weight = self.weights.get((current_node, neighbor), 1.0)
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        return path, distances[end]
    
    def bellman_ford(self, start: Any) -> Dict[Any, float]:
        """Bellman-Ford algorithm for negative weight detection"""
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        
        # Relax edges V-1 times
        for _ in range(len(self.graph) - 1):
            for u in self.graph:
                for v in self.graph[u]:
                    weight = self.weights.get((u, v), 1.0)
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
        
        # Check for negative cycles
        for u in self.graph:
            for v in self.graph[u]:
                weight = self.weights.get((u, v), 1.0)
                if distances[u] + weight < distances[v]:
                    raise ValueError("Negative cycle detected")
        
        return distances
    
    def floyd_warshall(self) -> Dict[Tuple[Any, Any], float]:
        """Floyd-Warshall algorithm for all-pairs shortest paths"""
        nodes = list(self.graph.keys())
        distances = {}
        
        # Initialize distances
        for u in nodes:
            for v in nodes:
                if u == v:
                    distances[(u, v)] = 0
                elif v in self.graph[u]:
                    distances[(u, v)] = self.weights.get((u, v), 1.0)
                else:
                    distances[(u, v)] = float('infinity')
        
        # Floyd-Warshall algorithm
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if distances[(i, k)] + distances[(k, j)] < distances[(i, j)]:
                        distances[(i, j)] = distances[(i, k)] + distances[(k, j)]
        
        return distances

class PerformanceAnalyzer:
    """Performance analysis and benchmarking tools"""
    
    def __init__(self):
        self.results = []
    
    def benchmark_algorithm(self, algorithm: Callable, data: List[Any], 
                          algorithm_name: str = None) -> AlgorithmResult:
        """Benchmark a single algorithm"""
        if algorithm_name is None:
            algorithm_name = algorithm.__name__
        
        # Create a copy of data to avoid modifying original
        test_data = data.copy()
        operations_counter = [0]
        
        # Measure execution time
        start_time = time.time()
        result = algorithm(test_data, operations_counter)
        execution_time = time.time() - start_time
        
        # Estimate memory usage (simplified)
        memory_usage = len(test_data) * 8  # Assume 8 bytes per element
        
        return AlgorithmResult(
            algorithm_name=algorithm_name,
            execution_time=execution_time,
            memory_usage=memory_usage,
            input_size=len(data),
            operations_count=operations_counter[0],
            result=result,
            complexity=self._estimate_complexity(algorithm_name, len(data), operations_counter[0])
        )
    
    def _estimate_complexity(self, algorithm_name: str, input_size: int, operations: int) -> str:
        """Estimate time complexity based on operations count"""
        if operations <= input_size:
            return "O(n)"
        elif operations <= input_size * np.log2(input_size):
            return "O(n log n)"
        elif operations <= input_size ** 2:
            return "O(n²)"
        elif operations <= input_size ** 3:
            return "O(n³)"
        else:
            return "O(2ⁿ)"
    
    def compare_algorithms(self, algorithms: Dict[str, Callable], 
                         data_sizes: List[int], data_generator: Callable = None) -> Dict[str, List[AlgorithmResult]]:
        """Compare multiple algorithms across different data sizes"""
        if data_generator is None:
            data_generator = lambda size: [random.randint(1, 1000) for _ in range(size)]
        
        results = {name: [] for name in algorithms.keys()}
        
        for size in data_sizes:
            data = data_generator(size)
            
            for name, algorithm in algorithms.items():
                try:
                    result = self.benchmark_algorithm(algorithm, data, name)
                    results[name].append(result)
                except Exception as e:
                    print(f"Error benchmarking {name} with size {size}: {e}")
        
        return results
    
    def generate_performance_report(self, results: Dict[str, List[AlgorithmResult]]) -> str:
        """Generate a comprehensive performance report"""
        report = "# Algorithm Performance Report\n\n"
        
        for algorithm_name, algorithm_results in results.items():
            report += f"## {algorithm_name}\n\n"
            report += "| Input Size | Time (s) | Operations | Complexity |\n"
            report += "|------------|----------|------------|------------|\n"
            
            for result in algorithm_results:
                report += f"| {result.input_size} | {result.execution_time:.6f} | {result.operations_count} | {result.complexity} |\n"
            
            report += "\n"
        
        return report
    
    def plot_performance(self, results: Dict[str, List[AlgorithmResult]], 
                        metric: str = 'execution_time') -> None:
        """Plot performance comparison"""
        plt.figure(figsize=(12, 8))
        
        for algorithm_name, algorithm_results in results.items():
            sizes = [r.input_size for r in algorithm_results]
            values = [getattr(r, metric) for r in algorithm_results]
            
            plt.plot(sizes, values, marker='o', label=algorithm_name)
        
        plt.xlabel('Input Size')
        plt.ylabel(metric.replace('_', ' ').title())
        plt.title(f'Algorithm Performance Comparison - {metric.replace("_", " ").title()}')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')
        plt.xscale('log')
        plt.show()

class AlgorithmComparator:
    """Advanced algorithm comparison and selection tools"""
    
    def __init__(self):
        self.analyzer = PerformanceAnalyzer()
        self.algorithm_registry = {}
    
    def register_algorithm(self, name: str, algorithm: Callable, 
                          best_case: str = "O(1)", worst_case: str = "O(n²)"):
        """Register an algorithm for comparison"""
        self.algorithm_registry[name] = {
            'algorithm': algorithm,
            'best_case': best_case,
            'worst_case': worst_case
        }
    
    def compare_algorithms(self, algorithm_names: List[str], data: List[Any]) -> Dict[str, AlgorithmResult]:
        """Compare registered algorithms on given data"""
        results = {}
        
        for name in algorithm_names:
            if name in self.algorithm_registry:
                algorithm = self.algorithm_registry[name]['algorithm']
                result = self.analyzer.benchmark_algorithm(algorithm, data, name)
                results[name] = result
        
        return results
    
    def recommend_algorithm(self, data: List[Any], criteria: str = 'speed') -> str:
        """Recommend the best algorithm based on data characteristics"""
        if not self.algorithm_registry:
            return "No algorithms registered"
        
        # Analyze data characteristics
        data_size = len(data)
        data_type = type(data[0]) if data else None
        data_range = max(data) - min(data) if data else 0
        
        # Simple recommendation logic
        if data_size < 50:
            return "insertion_sort" if "insertion_sort" in self.algorithm_registry else list(self.algorithm_registry.keys())[0]
        elif data_size < 1000:
            return "quicksort_optimized" if "quicksort_optimized" in self.algorithm_registry else list(self.algorithm_registry.keys())[0]
        else:
            return "mergesort_optimized" if "mergesort_optimized" in self.algorithm_registry else list(self.algorithm_registry.keys())[0]

# Example usage and testing
def test_enhanced_algorithms():
    """Test all enhanced algorithms"""
    print("Testing Enhanced Algorithms")
    print("=" * 40)
    
    # Test sorting algorithms
    print("\n1. Testing Sorting Algorithms:")
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original data: {test_data}")
    
    sorting_algorithms = {
        'quicksort': AdvancedSortingAlgorithms.quicksort_optimized,
        'mergesort': AdvancedSortingAlgorithms.mergesort_optimized,
        'heapsort': AdvancedSortingAlgorithms.heapsort_optimized,
        'insertion_sort': AdvancedSortingAlgorithms.insertion_sort
    }
    
    for name, algorithm in sorting_algorithms.items():
        data_copy = test_data.copy()
        result = algorithm(data_copy)
        print(f"{name}: {result}")
    
    # Test searching algorithms
    print("\n2. Testing Searching Algorithms:")
    sorted_data = sorted(test_data)
    print(f"Sorted data: {sorted_data}")
    
    search_algorithms = {
        'binary_search': AdvancedSearchingAlgorithms.binary_search_optimized,
        'interpolation_search': AdvancedSearchingAlgorithms.interpolation_search,
        'exponential_search': AdvancedSearchingAlgorithms.exponential_search
    }
    
    target = 22
    for name, algorithm in search_algorithms.items():
        result = algorithm(sorted_data, target)
        print(f"{name} for {target}: {result}")
    
    # Test graph algorithms
    print("\n3. Testing Graph Algorithms:")
    graph = GraphAlgorithms()
    graph.add_edge('A', 'B', 4)
    graph.add_edge('A', 'C', 2)
    graph.add_edge('B', 'C', 1)
    graph.add_edge('B', 'D', 5)
    graph.add_edge('C', 'D', 8)
    graph.add_edge('C', 'E', 10)
    graph.add_edge('D', 'E', 2)
    
    path, distance = graph.dijkstra_shortest_path('A', 'E')
    print(f"Shortest path from A to E: {path} (distance: {distance})")
    
    # Test performance analysis
    print("\n4. Testing Performance Analysis:")
    analyzer = PerformanceAnalyzer()
    comparator = AlgorithmComparator()
    
    # Register algorithms
    for name, algorithm in sorting_algorithms.items():
        comparator.register_algorithm(name, algorithm)
    
    # Compare algorithms
    test_sizes = [100, 1000, 10000]
    results = analyzer.compare_algorithms(sorting_algorithms, test_sizes)
    
    # Generate report
    report = analyzer.generate_performance_report(results)
    print("Performance Report:")
    print(report)

if __name__ == "__main__":
    test_enhanced_algorithms()
