# Swarm Path Planning - Modernized Bees Algorithm

A reproducible implementation of the Bees Algorithm for mobile robot and UAV path planning in dynamic environments with constraint handling.

## Research Context

This implementation extends the foundational work on the Bees Algorithm for robot path planning, building upon the seminal contributions by Prof. A.K.M. Joukhadar and collaborators.

### Related Publications
- Joukhadar et al., "Eine neue Methode zur Erzeugung der Anfangspopulation des Bienenalgorithmus für die Roboterpfadplanung in einer statischen Umgebung" (2024)
- Joukhadar, "Sensorless Drives, state-of-the-Art", PCIM'2001-Nuremberg

## Project Scope

### Primary Objectives
1. **Modernize the Bees Algorithm** for dynamic constrained environments
2. **Real-time planning capabilities** for mobile robots and UAVs
3. **Comprehensive benchmarking** against classical baselines (A*, RRT*, PRM, PSO)
4. **Stress testing** under realistic failure modes and edge cases

### Implementation Focus
- Enhanced neighborhood search with adaptive parameters
- Dynamic obstacle handling and collision avoidance
- Multi-objective optimization (path length, safety, energy)
- Integration with ROS/Gazebo and MATLAB/Simulink

## Repository Structure

```
swarm-path-planning-bees/
├── src/
│   ├── algorithms/          # Core algorithm implementations
│   │   ├── bees_algorithm.py
│   │   ├── baseline_comparators.py
│   │   └── optimization_utils.py
│   └── wrappers/            # ROS and simulation wrappers
│       ├── ros_bridge.py
│       └── matlab_bridge.py
├── tests/
│   ├── unit/               # Unit tests for core algorithms
│   ├── integration/        # Integration with simulation pipelines
│   └── stress/             # Stress tests and edge cases
├── simulations/
│   ├── scenarios/          # Scenario definitions
│   ├── configs/            # Configuration files
│   └── launch/             # ROS launch files
├── docs/
│   ├── literature/         # Literature synthesis
│   ├── method/             # Method documentation
│   └── evaluation/         # Evaluation protocol
├── data/                   # Dataset and sample scenarios
├── benchmarks/             # Benchmark results and comparison tables
└── notebooks/              # Analysis notebooks
```

## Installation

```bash
# Clone and setup
git clone https://github.com/molhamfetnah/swarm-path-planning-bees.git
cd swarm-path-planning-bees

# Python dependencies
pip install -r requirements.txt

# ROS integration (if using ROS)
# This workspace is designed for ROS Jazzy
```

## Quick Start

### Basic Usage

```python
from src.algorithms.bees_algorithm import ModernizedBeesAlgorithm

# Define planning problem
config = {
    'n_scout_bees': 50,
    'n_elite_sites': 5,
    'n_best_sites': 20,
    'neighborhood_size': 0.1,
    'max_iterations': 500
}

planner = ModernizedBeesAlgorithm(config)
path = planner.plan(start, goal, obstacles)
```

### ROS Integration

```bash
# Launch simulation
ros2 launch simulations launch_planning.launch.py
```

## Benchmarking

Run comprehensive benchmarks:

```bash
python benchmarks/run_all.py --scenarios static dynamic --compare-baselines
```

### Metrics
- Path length (meters)
- Planning time (seconds)
- Success rate (%)
- Smoothness (path curvature variance)
- Obstacle clearance (minimum distance)

## Stress Testing

The framework includes extensive stress tests:

```bash
# Run stress tests
python -m pytest tests/stress/ -v
```

### Test Categories
1. **Noise escalation**: Sensor noise at various levels
2. **Obstacle density**: High-density obstacle scenarios
3. **Dynamic obstacles**: Moving obstacle avoidance
4. **Partial failures**: Sensor dropout simulation
5. **Edge cases**: Narrow passages, dead-ends

## Evaluation Protocol

See `docs/evaluation/evaluation_protocol.md` for the complete evaluation framework.

## Paper and Publication

This repository supports reproducible research with:
- Complete algorithm implementation
- Raw benchmark data
- Statistical analysis notebooks
- Stress test results
- Comparison tables

## Contributing

Contributions are welcome. Please follow the contribution guidelines in `CONTRIBUTING.md`.

## License

Apache 2.0 - See `LICENSE` for details.

## Contact

For research collaboration and discussion, please contact the maintainer.

---

**Note**: This implementation is part of a broader research portfolio focusing on path planning, swarm intelligence, and autonomous robot navigation. Related projects include:
- `localization-tracking` - UKF/EKF state estimation
- `uav-mpc-geometric-control` - UAV control systems
- `benchmark-core` - Reproducible evaluation framework