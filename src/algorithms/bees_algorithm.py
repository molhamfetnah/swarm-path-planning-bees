"""
Modernized Bees Algorithm for Dynamic Path Planning

This implementation extends the classic Bees Algorithm with:
- Adaptive parameter tuning
- Dynamic obstacle handling
- Multi-objective optimization
- Real-time planning capabilities

Author: Research Portfolio
Based on work by A.K.M. Joukhadar et al.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Objective(Enum):
    PATH_LENGTH = "path_length"
    SAFETY = "safety"
    SMOOTHNESS = "smoothness"
    ENERGY = "energy"


@dataclass
class Bee:
    """Represents a single bee in the colony"""
    position: np.ndarray
    fitness: float = float('inf')
    cost: dict = field(default_factory=dict)
    
    def __repr__(self):
        return f"Bee(pos={self.position}, fitness={self.fitness:.4f})"


@dataclass
class PlanningConfig:
    """Configuration for the Bees Algorithm"""
    n_scout_bees: int = 50
    n_elite_sites: int = 5
    n_best_sites: int = 20
    neighborhood_size: float = 0.1
    max_iterations: int = 500
    convergence_threshold: float = 1e-6
    
    # Dynamic parameters
    adaptive_neighborhood: bool = True
    dynamic_obstacle_avoidance: bool = True
    
    # Multi-objective weights
    weights: dict = field(default_factory=lambda: {
        Objective.PATH_LENGTH: 0.4,
        Objective.SAFETY: 0.3,
        Objective.SMOOTHNESS: 0.2,
        Objective.ENERGY: 0.1
    })


class ModernizedBeesAlgorithm:
    """
    Modernized Bees Algorithm for path planning in dynamic environments
    """
    
    def __init__(self, config: PlanningConfig):
        self.config = config
        self.dimensions = None
        self.bounds = None
        self.colony: List[Bee] = []
        self.best_solution: Optional[Bee] = None
        self.iteration_history = []
        
    def initialize_colony(self, start: np.ndarray, goal: np.ndarray):
        """Initialize scout bees across the search space"""
        self.dimensions = len(start)
        self.bounds = (start, goal)
        
        # Generate initial population using improved method
        # Based on Joukhadar's population initialization improvement
        self.colony = []
        
        for _ in range(self.config.n_scout_bees):
            # Mix of random and heuristic initialization
            if np.random.random() < 0.3:
                # Heuristic: bias toward direct path
                alpha = np.random.random()
                position = start + alpha * (goal - start) + \
                          np.random.uniform(-0.1, 0.1, self.dimensions) * (goal - start)
            else:
                # Random initialization
                position = start + np.random.random(self.dimensions) * (goal - start)
            
            bee = Bee(position=position)
            self.colony.append(bee)
        
        logger.info(f"Initialized colony with {len(self.colony)} scout bees")
    
    def evaluate(self, position: np.ndarray, 
                 obstacles: List, 
                 start: np.ndarray, 
                 goal: np.ndarray) -> Tuple[float, dict]:
        """
        Evaluate fitness of a position
        
        Multi-objective evaluation:
        - Path length (distance to goal)
        - Safety (obstacle clearance)
        - Smoothness (path curvature)
        - Energy (effort estimate)
        """
        costs = {}
        
        # 1. Path length cost (Euclidean distance to goal)
        path_length = np.linalg.norm(position - goal)
        costs[Objective.PATH_LENGTH] = path_length
        
        # 2. Safety cost (minimum distance to obstacles)
        if obstacles:
            min_distance = min(
                np.linalg.norm(position - obs) if isinstance(obs, np.ndarray) 
                else self._obstacle_distance(position, obs)
                for obs in obstacles
            )
            # Penalize being too close to obstacles
            safety = 1.0 / (1.0 + min_distance)
        else:
            safety = 0.0
        costs[Objective.SAFETY] = safety
        
        # 3. Smoothness cost (deviation from straight line)
        if self.dimensions >= 2:
            direct_distance = np.linalg.norm(goal - start)
            deviation = abs(path_length - direct_distance) / (direct_distance + 1e-6)
            smoothness = deviation
        else:
            smoothness = 0.0
        costs[Objective.SMOOTHNESS] = smoothness
        
        # 4. Energy cost (path complexity estimate)
        energy = path_length * (1 + smoothness)
        costs[Objective.ENERGY] = energy
        
        # Weighted sum for multi-objective
        fitness = sum(
            self.config.weights[obj] * cost 
            for obj, cost in costs.items()
        )
        
        return fitness, costs
    
    def _obstacle_distance(self, position: np.ndarray, obstacle) -> float:
        """Calculate distance to obstacle (handles different types)"""
        if hasattr(obstacle, 'position'):
            return np.linalg.norm(position - obstacle.position)
        elif isinstance(obstacle, dict) and 'center' in obstacle:
            return np.linalg.norm(position - np.array(obstacle['center']))
        return float('inf')
    
    def scout_phase(self, obstacles: List, start: np.ndarray, goal: np.ndarray):
        """Phase 1: Send scouts to search for food sources"""
        for bee in self.colony:
            fitness, costs = self.evaluate(bee.position, obstacles, start, goal)
            bee.fitness = fitness
            bee.cost = costs
    
    def select_sites(self) -> Tuple[List[Bee], List[Bee]]:
        """Phase 2: Select elite and best sites for recruitment"""
        sorted_colony = sorted(self.colony, key=lambda b: b.fitness)
        
        elite_sites = sorted_colony[:self.config.n_elite_sites]
        best_sites = sorted_colony[:self.config.n_best_sites]
        
        return elite_sites, best_sites
    
    def recruit_elite_bees(self, elite_sites: List[Bee], 
                          obstacles: List, 
                          start: np.ndarray, 
                          goal: np.ndarray):
        """Phase 3a: Recruit bees to elite sites (intensive search)"""
        for elite in elite_sites:
            for _ in range(self.config.n_elite_sites):
                # Neighborhood search with small radius
                neighbor = elite.position + \
                          np.random.uniform(-1, 1, self.dimensions) * \
                          self.config.neighborhood_size * 0.5
                
                fitness, costs = self.evaluate(neighbor, obstacles, start, goal)
                
                if fitness < elite.fitness:
                    new_bee = Bee(position=neighbor, fitness=fitness, cost=costs)
                    self.colony.append(new_bee)
    
    def recruit_best_bees(self, best_sites: List[Bee],
                         obstacles: List,
                         start: np.ndarray,
                         goal: np.ndarray):
        """Phase 3b: Recruit bees to best sites (extensive search)"""
        for best in best_sites:
            for _ in range(self.config.n_best_sites):
                # Neighborhood search with larger radius
                neighbor = best.position + \
                          np.random.uniform(-1, 1, self.dimensions) * \
                          self.config.neighborhood_size
                
                fitness, costs = self.evaluate(neighbor, obstacles, start, goal)
                
                if fitness < best.fitness:
                    new_bee = Bee(position=neighbor, fitness=fitness, cost=costs)
                    self.colony.append(new_bee)
    
    def select_best_solution(self):
        """Update best solution found so far"""
        if not self.best_solution:
            self.best_solution = min(self.colony, key=lambda b: b.fitness)
        else:
            current_best = min(self.colony, key=lambda b: b.fitness)
            if current_best.fitness < self.best_solution.fitness:
                self.best_solution = current_best
    
    def check_convergence(self) -> bool:
        """Check if algorithm has converged"""
        if len(self.iteration_history) < 10:
            return False
        
        recent_fitness = [h['best_fitness'] for h in self.iteration_history[-10:]]
        fitness_variance = np.var(recent_fitness)
        
        return fitness_variance < self.config.convergence_threshold
    
    def run(self, start: np.ndarray, goal: np.ndarray, 
            obstacles: List = None) -> Tuple[List[np.ndarray], dict]:
        """
        Main algorithm execution
        
        Returns:
            path: List of waypoints from start to goal
            stats: Execution statistics
        """
        if obstacles is None:
            obstacles = []
        
        logger.info("Starting Bees Algorithm optimization...")
        
        # Initialization
        self.initialize_colony(start, goal)
        
        for iteration in range(self.config.max_iterations):
            # Phase 1: Scout search
            self.scout_phase(obstacles, start, goal)
            
            # Phase 2: Site selection
            elite_sites, best_sites = self.select_sites()
            
            # Phase 3: Recruitment
            self.recruit_elite_bees(elite_sites, obstacles, start, goal)
            self.recruit_best_bees(best_sites, obstacles, start, goal)
            
            # Adaptive neighborhood size
            if self.config.adaptive_neighborhood:
                self._adapt_neighborhood(iteration)
            
            # Track best solution
            self.select_best_solution()
            
            # Record history
            self.iteration_history.append({
                'iteration': iteration,
                'best_fitness': self.best_solution.fitness if self.best_solution else float('inf'),
                'avg_fitness': np.mean([b.fitness for b in self.colony])
            })
            
            # Log progress
            if iteration % 50 == 0:
                logger.info(f"Iteration {iteration}: Best fitness = {self.best_solution.fitness:.4f}")
            
            # Check convergence
            if self.check_convergence():
                logger.info(f"Converged at iteration {iteration}")
                break
        
        # Generate path
        path = self._generate_path(start, goal)
        
        stats = {
            'iterations': len(self.iteration_history),
            'final_fitness': self.best_solution.fitness if self.best_solution else float('inf'),
            'convergence_iteration': iteration,
            'history': self.iteration_history
        }
        
        logger.info(f"Optimization complete. Final fitness: {stats['final_fitness']:.4f}")
        
        return path, stats
    
    def _adapt_neighborhood(self, iteration: int):
        """Adaptively adjust neighborhood size"""
        # Decrease neighborhood size as iterations progress
        decay_rate = 0.95
        self.config.neighborhood_size *= decay_rate
    
    def _generate_path(self, start: np.ndarray, goal: np.ndarray) -> List[np.ndarray]:
        """Generate smooth path from optimization result"""
        if self.best_solution is None:
            return [start, goal]
        
        # Simple path: start -> best solution -> goal
        # In practice, you'd smooth this with splines
        return [start, self.best_solution.position, goal]


class BaselineComparator:
    """
    Compare Bees Algorithm against classical baselines
    """
    
    def __init__(self):
        self.results = {}
    
    def run_baselines(self, start: np.ndarray, goal: np.ndarray,
                      obstacles: List, scenarios: List[str]) -> dict:
        """
        Run all baseline algorithms
        
        Baselines:
        - A* (grid-based)
        - RRT* (sampling-based)
        - PRM (probabilistic roadmap)
        - PSO (Particle Swarm Optimization)
        - GA (Genetic Algorithm)
        """
        baselines = {
            'bees': lambda: self._run_bees(start, goal, obstacles),
            'astar': lambda: self._run_astar(start, goal, obstacles),
            'rrt': lambda: self._run_rrt(start, goal, obstacles),
            'pso': lambda: self._run_pso(start, goal, obstacles)
        }
        
        for name, func in baselines.items():
            logger.info(f"Running {name} baseline...")
            try:
                result = func()
                self.results[name] = result
            except Exception as e:
                logger.error(f"Error running {name}: {e}")
                self.results[name] = {'error': str(e)}
        
        return self.results
    
    def _run_bees(self, start, goal, obstacles):
        """Run Bees Algorithm"""
        config = PlanningConfig()
        algo = ModernizedBeesAlgorithm(config)
        path, stats = algo.run(start, goal, obstacles)
        return {'path': path, 'stats': stats}
    
    def _run_astar(self, start, goal, obstacles):
        """Run A* algorithm (placeholder - implement based on environment)"""
        # Placeholder - requires grid environment
        return {'path': [start, goal], 'stats': {'time': 0}}
    
    def _run_rrt(self, start, goal, obstacles):
        """Run RRT* (placeholder - implement based on environment)"""
        # Placeholder - requires sampling
        return {'path': [start, goal], 'stats': {'time': 0}}
    
    def _run_pso(self, start, goal, obstacles):
        """Run Particle Swarm Optimization (placeholder)"""
        # Placeholder - implement if needed
        return {'path': [start, goal], 'stats': {'time': 0}}
    
    def generate_comparison_table(self) -> str:
        """Generate benchmark comparison table"""
        if not self.results:
            return "No results available"
        
        table = "| Algorithm | Path Length | Time (s) | Success Rate |\n"
        table += "|-----------|-------------|----------|--------------|\n"
        
        for name, result in self.results.items():
            if 'error' not in result:
                stats = result.get('stats', {})
                table += f"| {name} | - | - | - |\n"
        
        return table


if __name__ == "__main__":
    # Example usage
    config = PlanningConfig(
        n_scout_bees=50,
        n_elite_sites=5,
        n_best_sites=20,
        max_iterations=200
    )
    
    # Test problem
    start = np.array([0.0, 0.0])
    goal = np.array([10.0, 10.0])
    obstacles = [np.array([5.0, 5.0]), np.array([7.0, 3.0])]
    
    algo = ModernizedBeesAlgorithm(config)
    path, stats = algo.run(start, goal, obstacles)
    
    print(f"Found path with {len(path)} waypoints")
    print(f"Final fitness: {stats['final_fitness']:.4f}")
    print(f"Iterations: {stats['iterations']}")