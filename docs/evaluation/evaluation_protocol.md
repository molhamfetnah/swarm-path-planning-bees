# Evaluation Protocol - Swarm Path Planning

This document defines the standardized evaluation framework for comparing path planning algorithms.

## Metrics Definition

### Primary Metrics

1. **Path Length**
   - Definition: Total Euclidean distance of the planned path
   - Unit: meters (m)
   - Target: Minimize

2. **Planning Time**
   - Definition: Time from problem specification to path solution
   - Unit: seconds (s)
   - Target: Minimize

3. **Success Rate**
   - Definition: Percentage of trials where valid path is found
   - Unit: percentage (%)
   - Target: Maximize (100%)

### Secondary Metrics

4. **Path Smoothness**
   - Definition: Variance in path curvature
   - Computation: σ²(κ) where κ is curvature at each waypoint
   - Unit: dimensionless
   - Target: Minimize

5. **Obstacle Clearance**
   - Definition: Minimum distance to any obstacle
   - Unit: meters (m)
   - Target: Maximize (with safety margin)

6. **Path Complexity**
   - Definition: Number of waypoints / direct distance
   - Unit: dimensionless
   - Target: Minimize (closer to 1 is simpler)

## Test Scenarios

### Static Scenarios

| Scenario | Description | Difficulty |
|----------|-------------|------------|
| S1 | Empty environment | Easy |
| S2 | Single rectangular obstacle | Easy |
| S3 | Multiple static obstacles | Medium |
| S4 | Maze-like structure | Hard |
| S5 | Narrow passage | Hard |

### Dynamic Scenarios

| Scenario | Description | Difficulty |
|----------|-------------|------------|
| D1 | Slowly moving obstacle | Medium |
| D2 | Fast moving obstacle | Hard |
| D3 | Multiple dynamic obstacles | Hard |
| D4 | Partially observable | Hard |

### Stress Scenarios

| Scenario | Description | Purpose |
|----------|-------------|---------|
| T1 | High obstacle density (>50%) | Robustness |
| T2 | Sensor noise injection | Reliability |
| T3 | Goal unreachable (boundary) | Graceful failure |
| T4 | Narrow corridor (< robot width) | Edge case |
| T5 | Time-constrained replanning | Real-time performance |

## Evaluation Procedure

### Standard Benchmark Run

1. **Setup**
   - Initialize algorithm with default parameters
   - Set random seed for reproducibility
   - Load scenario configuration

2. **Execution**
   - Run algorithm for each scenario
   - Record all metrics
   - Save raw path data

3. **Analysis**
   - Compute statistics (mean, std, min, max)
   - Generate comparison tables
   - Create visualization plots

### Statistical Significance

- Run each scenario 30 times
- Use paired t-test for comparison
- Report p-values for significance (α = 0.05)
- Confidence intervals: 95%

## Baseline Algorithms

For comparison, the following baselines are included:

1. **A*** - Grid-based optimal pathfinder
2. **RRT*** - Rapidly-exploring Random Tree Star
3. **PRM** - Probabilistic Roadmap Method
4. **PSO** - Particle Swarm Optimization
5. **GA** - Genetic Algorithm

## Environment Specification

### Simulation Parameters
- Environment size: 20m x 20m
- Robot radius: 0.3m
- Velocity: 1.0 m/s (for dynamic scenarios)
- Time step: 0.1s

### Hardware Configuration
- CPU: Standard laptop processor
- Memory: 8GB RAM
- No GPU acceleration required

## Output Formats

### Benchmark Results
```json
{
  "scenario": "S3",
  "algorithm": "bees",
  "metrics": {
    "path_length": 15.4,
    "planning_time": 0.32,
    "success_rate": 1.0,
    "smoothness": 0.15,
    "clearance": 0.5
  },
  "statistics": {
    "runs": 30,
    "mean": {...},
    "std": {...}
  }
}
```

### Comparison Table Format

| Algorithm | Path Length (m) | Time (s) | Success (%) | Clearance (m) |
|-----------|----------------|----------|-------------|---------------|
| Bees      | 15.4 ± 0.3     | 0.32±0.05| 100         | 0.50 ± 0.10   |
| A*        | 14.8 ± 0.2     | 0.15±0.02| 100         | 0.45 ± 0.08   |
| RRT*      | 16.2 ± 0.8     | 0.45±0.10| 95          | 0.55 ± 0.12   |

## Reproducibility

All benchmarks are reproducible using:
- Fixed random seeds (configurable)
- Pinned dependency versions
- Deterministic execution where possible
- Complete logging of all parameters

## References

- Joukhadar et al., "Eine neue Methode zur Erzeugung der Anfangspopulation des Bienenalgorithmus" (2024)
- Standard evaluation frameworks for path planning algorithms