#!/usr/bin/env python3
"""
Path Visualization Script (Non-interactive)

Author: Research Portfolio
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src.algorithms.bees_algorithm import ModernizedBeesAlgorithm, PlanningConfig


def run_visualization():
    """Run and save visualization"""
    
    scenarios = {
        'S1: Empty': {'start': [0.0, 0.0], 'goal': [10.0, 10.0], 'obstacles': []},
        'S2: Single': {'start': [0.0, 0.0], 'goal': [10.0, 10.0], 'obstacles': [[5.0, 5.0]]},
        'S3: Multiple': {'start': [0.0, 0.0], 'goal': [10.0, 10.0], 'obstacles': [[5.0, 5.0], [3.0, 7.0], [7.0, 3.0]]},
    }
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, (name, config) in enumerate(scenarios.items()):
        ax = axes[idx]
        start = np.array(config['start'])
        goal = np.array(config['goal'])
        obstacles = [np.array(o) for o in config['obstacles']]
        
        algo = ModernizedBeesAlgorithm(PlanningConfig(n_scout_bees=30, max_iterations=100))
        path, stats = algo.run(start, goal, obstacles)
        
        # Draw obstacles
        for obs in obstacles:
            ax.add_patch(patches.Circle(obs, radius=0.4, facecolor='lightcoral', alpha=0.7))
        
        # Draw path
        if len(path) > 1:
            path_arr = np.array(path)
            ax.plot(path_arr[:, 0], path_arr[:, 1], 'b-', linewidth=2)
            ax.plot(path_arr[:, 0], path_arr[:, 1], 'bo', markersize=6)
        
        ax.plot(start[0], start[1], 'go', markersize=10)
        ax.plot(goal[0], goal[1], 'ro', markersize=10)
        ax.set_title(f"{name}")
        ax.set_xlim(-1, 12)
        ax.set_ylim(-1, 12)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmarks/visualization.png', dpi=100)
    print("Saved: benchmarks/visualization.png")


if __name__ == "__main__":
    run_visualization()