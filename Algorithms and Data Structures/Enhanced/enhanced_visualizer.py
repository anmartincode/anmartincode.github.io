#!/usr/bin/env python3
"""
Enhanced Algorithm Visualizer with ML Integration and Performance Analytics
"""

import time
import psutil
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

from enhanced_structures import RedBlackTree, BTree, SkipList, Trie, DisjointSet
from enhanced_algorithms import AlgorithmComparator, PerformanceAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Data class for storing algorithm performance metrics"""
    algorithm_name: str
    execution_time: float
    memory_usage: float
    time_complexity: str
    space_complexity: str
    input_size: int
    cpu_usage: float
    operations_count: int

class MLAlgorithmOptimizer:
    """Machine Learning-based algorithm optimization"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.performance_history = []
    
    def extract_features(self, data: List[Any]) -> np.ndarray:
        """Extract features from input data for ML model"""
        features = []
        for item in data:
            if isinstance(item, (int, float)):
                features.extend([item, abs(item), item ** 2])
            elif isinstance(item, str):
                features.extend([len(item), sum(ord(c) for c in item), len(set(item))])
            else:
                features.extend([0, 0, 0])  # Default for unknown types
        
        # Pad or truncate to fixed length
        feature_vector = features[:30] + [0] * max(0, 30 - len(features))
        return np.array(feature_vector).reshape(1, -1)
    
    def train(self, training_data: List[Dict]):
        """Train the ML model on historical performance data"""
        if not training_data:
            logger.warning("No training data provided")
            return
        
        X = []
        y = []
        
        for record in training_data:
            features = self.extract_features(record['data'])
            X.append(features.flatten())
            y.append(record['execution_time'])
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        logger.info("ML model trained successfully")
    
    def predict_performance(self, data: List[Any], algorithm: str) -> float:
        """Predict execution time for given data and algorithm"""
        if not self.is_trained:
            return 0.0
        
        features = self.extract_features(data)
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        return max(0.0, prediction)

class DistributedAlgorithmExecutor:
    """Distributed computing support for algorithms"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def parallel_sort(self, data: List[Any], algorithm: str = 'quicksort') -> List[Any]:
        """Parallel sorting implementation"""
        if len(data) < 1000:  # Use sequential for small datasets
            return sorted(data)
        
        # Split data into chunks
        chunk_size = len(data) // self.max_workers
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Sort chunks in parallel
        futures = []
        for chunk in chunks:
            future = self.executor.submit(sorted, chunk)
            futures.append(future)
        
        # Collect results
        sorted_chunks = [future.result() for future in as_completed(futures)]
        
        # Merge sorted chunks
        return self._merge_sorted_chunks(sorted_chunks)
    
    def _merge_sorted_chunks(self, chunks: List[List[Any]]) -> List[Any]:
        """Merge multiple sorted chunks into a single sorted list"""
        if not chunks:
            return []
        if len(chunks) == 1:
            return chunks[0]
        
        # Use heap-based merge for efficiency
        import heapq
        merged = []
        heap = []
        
        # Initialize heap with first element from each chunk
        for i, chunk in enumerate(chunks):
            if chunk:
                heapq.heappush(heap, (chunk[0], i, 0))
        
        # Merge elements
        while heap:
            value, chunk_idx, elem_idx = heapq.heappop(heap)
            merged.append(value)
            
            # Add next element from the same chunk if available
            if elem_idx + 1 < len(chunks[chunk_idx]):
                next_elem = chunks[chunk_idx][elem_idx + 1]
                heapq.heappush(heap, (next_elem, chunk_idx, elem_idx + 1))
        
        return merged

class EnhancedVisualizer:
    """Enhanced algorithm visualizer with advanced features"""
    
    def __init__(self):
        self.ml_optimizer = MLAlgorithmOptimizer()
        self.distributed_executor = DistributedAlgorithmExecutor()
        self.performance_analyzer = PerformanceAnalyzer()
        self.comparator = AlgorithmComparator()
        self.metrics_history = []
        
        # Initialize data structures
        self.red_black_tree = RedBlackTree()
        self.b_tree = BTree(degree=3)
        self.skip_list = SkipList()
        self.trie = Trie()
        self.disjoint_set = DisjointSet()
    
    def measure_performance(self, func, *args, **kwargs) -> PerformanceMetrics:
        """Measure performance metrics for a function execution"""
        process = psutil.Process()
        
        # Record initial state
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        initial_cpu = process.cpu_percent()
        
        # Execute function and measure time
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        # Record final state
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        final_cpu = process.cpu_percent()
        
        # Calculate metrics
        memory_usage = final_memory - initial_memory
        cpu_usage = (initial_cpu + final_cpu) / 2
        
        return PerformanceMetrics(
            algorithm_name=func.__name__,
            execution_time=execution_time,
            memory_usage=memory_usage,
            time_complexity="O(n log n)",  # Default, should be calculated based on algorithm
            space_complexity="O(n)",
            input_size=len(args[0]) if args else 0,
            cpu_usage=cpu_usage,
            operations_count=0  # Would need to be tracked within algorithm
        )
    
    def benchmark_algorithms(self, data: List[Any]) -> Dict[str, PerformanceMetrics]:
        """Benchmark multiple algorithms on the same dataset"""
        algorithms = {
            'sorted': sorted,
            'parallel_sort': lambda x: self.distributed_executor.parallel_sort(x),
            'red_black_tree': lambda x: self._test_red_black_tree(x),
            'b_tree': lambda x: self._test_b_tree(x),
            'skip_list': lambda x: self._test_skip_list(x)
        }
        
        results = {}
        for name, algorithm in algorithms.items():
            try:
                metrics = self.measure_performance(algorithm, data.copy())
                results[name] = metrics
                self.metrics_history.append(metrics)
            except Exception as e:
                logger.error(f"Error benchmarking {name}: {e}")
        
        return results
    
    def _test_red_black_tree(self, data: List[Any]) -> List[Any]:
        """Test Red-Black Tree operations"""
        tree = RedBlackTree()
        for item in data:
            tree.insert(item)
        return tree.inorder_traversal()
    
    def _test_b_tree(self, data: List[Any]) -> List[Any]:
        """Test B-Tree operations"""
        tree = BTree(degree=3)
        for item in data:
            tree.insert(item)
        return tree.traverse()
    
    def _test_skip_list(self, data: List[Any]) -> List[Any]:
        """Test Skip List operations"""
        skip_list = SkipList()
        for item in data:
            skip_list.insert(item)
        return skip_list.to_list()
    
    def generate_performance_report(self, metrics: Dict[str, PerformanceMetrics]) -> str:
        """Generate a comprehensive performance report"""
        report = "# Algorithm Performance Report\n\n"
        
        # Summary table
        report += "## Performance Summary\n\n"
        report += "| Algorithm | Time (s) | Memory (MB) | CPU (%) | Input Size |\n"
        report += "|-----------|----------|-------------|---------|------------|\n"
        
        for name, metric in metrics.items():
            report += f"| {name} | {metric.execution_time:.4f} | {metric.memory_usage:.2f} | {metric.cpu_usage:.1f} | {metric.input_size} |\n"
        
        # Find fastest algorithm
        fastest = min(metrics.values(), key=lambda x: x.execution_time)
        report += f"\n**Fastest Algorithm**: {fastest.algorithm_name} ({fastest.execution_time:.4f}s)\n\n"
        
        # ML predictions
        if self.ml_optimizer.is_trained:
            report += "## ML Performance Predictions\n\n"
            for name, metric in metrics.items():
                prediction = self.ml_optimizer.predict_performance([metric.input_size], name)
                report += f"- **{name}**: Predicted {prediction:.4f}s (Actual: {metric.execution_time:.4f}s)\n"
        
        return report
    
    def create_interactive_dashboard(self):
        """Create an interactive Dash dashboard"""
        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        
        app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Enhanced Algorithm Visualizer", className="text-center mb-4"),
                    html.Hr()
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Input Data"),
                        dbc.CardBody([
                            dcc.Textarea(
                                id='input-data',
                                placeholder='Enter comma-separated numbers...',
                                style={'width': '100%', 'height': 100}
                            ),
                            dbc.Button("Run Benchmark", id="run-benchmark", color="primary", className="mt-2")
                        ])
                    ])
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Performance Metrics"),
                        dbc.CardBody(id="metrics-output")
                    ])
                ], width=6)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="performance-chart")
                ])
            ], className="mt-4")
        ])
        
        @app.callback(
            [Output("metrics-output", "children"),
             Output("performance-chart", "figure")],
            [Input("run-benchmark", "n_clicks")],
            [State("input-data", "value")]
        )
        def update_metrics(n_clicks, input_data):
            if not n_clicks or not input_data:
                return "Enter data and click Run Benchmark", {}
            
            try:
                # Parse input data
                data = [int(x.strip()) for x in input_data.split(',') if x.strip()]
                
                # Run benchmark
                metrics = self.benchmark_algorithms(data)
                
                # Create metrics display
                metrics_display = []
                for name, metric in metrics.items():
                    metrics_display.append(
                        dbc.Alert([
                            html.H5(name),
                            html.P(f"Time: {metric.execution_time:.4f}s | Memory: {metric.memory_usage:.2f}MB")
                        ], color="info", className="mb-2")
                    )
                
                # Create performance chart
                fig = go.Figure()
                algorithms = list(metrics.keys())
                times = [metrics[alg].execution_time for alg in algorithms]
                
                fig.add_trace(go.Bar(
                    x=algorithms,
                    y=times,
                    text=[f"{t:.4f}s" for t in times],
                    textposition='auto',
                ))
                
                fig.update_layout(
                    title="Algorithm Performance Comparison",
                    xaxis_title="Algorithm",
                    yaxis_title="Execution Time (seconds)",
                    showlegend=False
                )
                
                return metrics_display, fig
                
            except Exception as e:
                return f"Error: {str(e)}", {}
        
        return app

def main():
    """Main function to run the enhanced visualizer"""
    visualizer = EnhancedVisualizer()
    
    # Example usage
    print("Enhanced Algorithm Visualizer")
    print("=" * 40)
    
    # Generate sample data
    sample_data = list(range(1000, 0, -1))  # Reverse sorted data
    
    print(f"Benchmarking algorithms on {len(sample_data)} elements...")
    
    # Run benchmark
    metrics = visualizer.benchmark_algorithms(sample_data)
    
    # Generate report
    report = visualizer.generate_performance_report(metrics)
    print(report)
    
    # Save report
    with open("performance_report.md", "w") as f:
        f.write(report)
    
    print("Report saved to performance_report.md")
    
    # Start interactive dashboard
    print("Starting interactive dashboard...")
    app = visualizer.create_interactive_dashboard()
    app.run_server(debug=True, port=8050)

if __name__ == "__main__":
    main()
