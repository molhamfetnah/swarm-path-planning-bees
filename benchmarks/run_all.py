"""
Comprehensive Benchmark Runner for Swarm Path Planning

This script runs benchmarks across multiple scenarios and generates
comparison tables against classical algorithms.

Author: Research Portfolio
"""

import numpy as np
import json
import time
from datetime import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
import os

from src.algorithms.bees_algorithm import ModernizedBeesAlgorithm, PlanningConfig


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run"""
    algorithm: str
    scenario: str
    path_length: float
    planning_time: float
    success: bool
    iterations: int
    fitness: float


class BenchmarkRunner:
    """Run comprehensive benchmarks for path planning algorithms"""
    
    def __init__(self, n_runs: int = 30):
        self.n_runs = n_runs
        self.results: List[BenchmarkResult] = []
        self.scenarios = self._load_scenarios()
    
    def _load_scenarios(self) -> Dict[str, dict]:
        """Define test scenarios"""
        return {
            'S1_empty': {
                'start': [0.0, 0.0],
                'goal': [10.0, 10.0],
                'obstacles': [],
                'description': 'Empty environment'
            },
            'S2_single_obstacle': {
                'start': [0.0, 0.0],
                'goal': [10.0, 10.0],
                'obstacles': [[5.0, 5.0]],
                'description': 'Single rectangular obstacle'
            },
            'S3_multiple_obstacles': {
                'start': [0.0, 0.0],
                'goal': [10.0, 10.0],
                'obstacles': [[5.0, 5.0], [3.0, 7.0], [7.0, 3.0], [2.0, 2.0], [8.0, 8.0]],
                'description': 'Multiple static obstacles'
            },
            'S4_maze': {
                'start': [0.0, 5.0],
                'goal': [20.0, 5.0],
                'obstacles': [[5.0, 0.0], [5.0, 3.0], [10.0, 7.0], [10.0, 10.0],
                             [15.0, 0.0], [15.0, 3.0]],
                'description': 'Maze-like structure'
            },
            'S5_narrow': {
                'start': [0.0, 5.0],
                'goal': [10.0, 5.0],
                'obstacles': [[5.0, 3.0], [5.0, 4.0], [5.0, 6.0], [5.0, 7.0]],
                'description': 'Narrow passage'
            },
            'D1_dynamic': {
                'start': [0.0, 0.0],
                'goal': [10.0, 10.0],
                'obstacles': [[5.0, 5.0], [7.0, 2.0]],
                'description': 'Slowly moving obstacle'
            }
        }
    
    def _calculate_path_length(self, path: List[np.ndarray]) -> float:
        """Calculate total path length"""
        if len(path) < 2:
            return 0.0
        
        total = 0.0
        for i in range(len(path) - 1):
            total += np.linalg.norm(path[i+1] - path[i])
        return total
    
    def run_bees_benchmark(self, scenario_name: str, config: dict) -> BenchmarkResult:
        """Run Bees Algorithm on a scenario"""
        np.random.seed(42)  # For reproducibility
        
        start = np.array(config['start'])
        goal = np.array(config['goal'])
        obstacles = [np.array(o) for o in config['obstacles']]
        
        algo_config = PlanningConfig(
            n_scout_bees=50,
            n_elite_sites=5,
            n_best_sites=20,
            max_iterations=500
        )
        
        algo = ModernizedBeesAlgorithm(algo_config)
        
        start_time = time.time()
        
        try:
            path, stats = algo.run(start, goal, obstacles)
            planning_time = time.time() - start_time
            path_length = self._calculate_path_length(path)
            
            return BenchmarkResult(
                algorithm='Bees',
                scenario=scenario_name,
                path_length=path_length,
                planning_time=planning_time,
                success=True,
                iterations=stats['iterations'],
                fitness=stats['final_fitness']
            )
        except Exception as e:
            planning_time = time.time() - start_time
            return BenchmarkResult(
                algorithm='Bees',
                scenario=scenario_name,
                path_length=float('inf'),
                planning_time=planning_time,
                success=False,
                iterations=0,
                fitness=float('inf')
            )
    
    def run_all_benchmarks(self) -> List[BenchmarkResult]:
        """Run all benchmarks"""
        print("=" * 60)
        print("RUNNING COMPREHENSIVE BENCHMARKS")
        print("=" * 60)
        
        results = []
        
        for scenario_name, config in self.scenarios.items():
            print(f"\n--- Scenario: {scenario_name} ---")
            print(f"Description: {config['description']}")
            
            # Run multiple times for statistics
            for run in range(self.n_runs):
                np.random.seed(run)
                result = self.run_bees_benchmark(scenario_name, config)
                results.append(result)
                
                if run == 0:
                    print(f"  Run {run+1}: path_length={result.path_length:.2f}, "
                          f"time={result.planning_time:.3f}s, "
                          f"success={result.success}")
            
            # Compute statistics
            scenario_results = [r for r in results if r.scenario == scenario_name]
            success_rate = sum(1 for r in scenario_results if r.success) / len(scenario_results)
            avg_path = np.mean([r.path_length for r in scenario_results if r.success])
            avg_time = np.mean([r.planning_time for r in scenario_results if r.success])
            
            print(f"  Statistics: success_rate={success_rate*100:.1f}%, "
                  f"avg_path={avg_path:.2f}m, avg_time={avg_time:.3f}s")
        
        self.results = results
        return results
    
    def generate_comparison_table(self) -> str:
        """Generate benchmark comparison table"""
        table = "\n" + "=" * 80
        table += "\nBENCHMARK RESULTS - Bees Algorithm"
        table += "\n" + "=" * 80 + "\n\n"
        
        table += "| Scenario | Path Length (m) | Time (s) | Success Rate | Iterations |\n"
        table += "|-----------|----------------|----------|--------------|------------|\n"
        
        scenarios = set(r.scenario for r in self.results)
        for scenario in sorted(scenarios):
            scenario_results = [r for r in self.results if r.scenario == scenario]
            
            success_rate = sum(1 for r in scenario_results if r.success) / len(scenario_results)
            path_lengths = [r.path_length for r in scenario_results if r.success]
            times = [r.planning_time for r in scenario_results if r.success]
            iterations = [r.iterations for r in scenario_results if r.success]
            
            if path_lengths:
                avg_path = np.mean(path_lengths)
                std_path = np.std(path_lengths)
                avg_time = np.mean(times)
                std_time = np.std(times)
                avg_iter = np.mean(iterations)
                
                table += f"| {scenario} | {avg_path:.2f} ± {std_path:.2f} | "
                table += f"{avg_time:.3f} ± {std_time:.3f} | "
                table += f"{success_rate*100:.0f}% | {avg_iter:.0f} |\n"
            else:
                table += f"| {scenario} | N/A | N/A | 0% | N/A |\n"
        
        return table
    
    def save_results(self, output_dir: str = "benchmarks"):
        """Save results to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON
        results_json = [asdict(r) for r in self.results]
        with open(f'{output_dir}/results.json', 'w') as f:
            json.dump(results_json, f, indent=2)
        
        # Save CSV
        import csv
        with open(f'{output_dir}/results.csv', 'w', newline='') as f:
            if self.results:
                writer = csv.DictWriter(f, fieldnames=asdict(self.results[0]).keys())
                writer.writeheader()
                for r in self.results:
                    writer.writerow(asdict(r))
        
        # Save summary
        summary = self.generate_comparison_table()
        with open(f'{output_dir}/summary.txt', 'w') as f:
            f.write(summary)
        
        print(f"\nResults saved to {output_dir}/")
        print(summary)
        
        return output_dir


def run_stress_tests():
    """Run stress tests"""
    print("\n" + "=" * 60)
    print("RUNNING STRESS TESTS")
    print("=" * 60 + "\n")
    
    from tests.stress.test_stress import StressTestRunner
    
    config = PlanningConfig(n_scout_bees=30, max_iterations=100)
    algo = ModernizedBeesAlgorithm(config)
    
    runner = StressTestRunner(algo)
    results = runner.run_all_tests()
    
    report = runner.generate_report()
    print(report)
    
    # Save stress test report
    os.makedirs('benchmarks', exist_ok=True)
    with open('benchmarks/stress_report.md', 'w') as f:
        f.write(report)
    
    return results


def main():
    """Main benchmark execution"""
    print("SWARM PATH PLANNING - BENCHMARK SUITE")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run benchmarks
    runner = BenchmarkRunner(n_runs=30)
    results = runner.run_all_benchmarks()
    
    # Save results
    runner.save_results('benchmarks')
    
    # Run stress tests
    stress_results = run_stress_tests()
    
    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)
    print(f"Total runs: {len(results)}")
    print(f"Results saved to: benchmarks/")


if __name__ == "__main__":
    main()