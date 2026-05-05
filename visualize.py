#!/usr/bin/env python3
"""
Path Visualization Script

This script visualizes the Bees Algorithm path planning results
without requiring ROS/Gazebo.

Usage:
    python3 visualize.py

Author: Research Portfolio
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from typing import List, Tuple

from src.algorithms.bees_algorithm import ModernizedBeesAlgorithm, PlanningConfig


def visualize_scenario(scenario_name: str, config: dict, ax: plt.Axes):
    """Visualize a single scenario"""
    
    start = np.array(config['start'])
    goal = np.array(config['goal'])
    obstacles = [np.array(o) for o in config['obstacles']]
    
    # Run planner
    algo_config = PlanningConfig(n_scout_bees=50, max_iterations=200)
    algo = ModernizedBeesAlgorithm(algo_config)
    path, stats = algo.run(start, goal, obstacles)
    
    # Draw obstacles
    for obs in obstacles:
        circle = patches.Circle(obs, radius=0.4, linewidth=1, 
                                edgecolor='r', facecolor='lightcoral', alpha=0.7)
        ax.add_patch(circle)
    
    # Draw path
    if len(path) > 1:
        path_arr = np.array(path)
        ax.plot(path_arr[:, 0], path_arr[:, 1], 'b-', linewidth=2, 
                label='Planned Path', zorder=5)
        ax.plot(path_arr[:, 0], path_arr[:, 1], 'bo', markersize=8, zorder=6)
    
    # Draw start and goal
    ax.plot(start[0], start[1], 'go', markersize=12, label='Start', zorder=7)
    ax.plot(goal[0], goal[1], 'ro', markersize=12, label='Goal', zorder=7)
    
    # Labels
    ax.set_title(f"{scenario_name}\nPath Length: {stats['final_fitness']:.2f}")
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-1, 12)
    ax.set_ylim(-1, 12)
    ax.set_aspect('equal')


def main():
    """Main visualization function"""
    
    # Define scenarios
    scenarios = {
        'Empty Environment': {
            'start': [0.0, 0.0],
            'goal': [10.0, 10.0],
            'obstacles': []
        },
        'Single Obstacle': {
            'start': [0.0, 0.0],
            'goal': [10.0, 10.0],
            'obstacles': [[5.0, 5.0]]
        },
        'Multiple Obstacles': {
            'start': [0.0, 0.0],
            'goal': [10.0, 10.0],
            'obstacles': [[5.0, 5.0], [3.0, 7.0], [7.0, 3.0], [2.0, 2.0], [8.0, 8.0]]
        },
        'Narrow Passage': {
            'start': [0.0, 5.0],
            'goal': [10.0, 5.0],
            'obstacles': [[5.0, 3.0], [5.0, 4.0], [5.0, 6.0], [5.0, 7.0]]
        },
        'Maze': {
            'start': [0.0, 5.0],
            'goal': [20.0, 5.0],
            'obstacles': [[5.0, 0.0], [5.0, 3.0], [10.0, 7.0], [10.0, 10.0],
                         [15.0, 0.0], [15.0, 3.0]]
        },
        'Dynamic Obstacles': {
            'start': [0.0, 0.0],
            'goal': [10.0, 10.0],
            'obstacles': [[5.0, 5.0], [7.0, 2.0]]
        }
    }
    
    # Create figure
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # Plot each scenario
    for idx, (name, config) in enumerate(scenarios.items()):
        visualize_scenario(name, config, axes[idx])
    
    plt.suptitle('Bees Algorithm Path Planning - Benchmark Scenarios', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('benchmarks/visualization.png', dpi=150, bbox_inches='tight')
    print("Visualization saved to benchmarks/visualization.png")
    
    plt.show()


if __name__ == "__main__":
    main()