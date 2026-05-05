#!/usr/bin/env python3
"""
ROS2 Node for Bees Algorithm Path Planning

This node provides a ROS2 interface for the Modernized Bees Algorithm
for real-time path planning in robotics applications.

Author: Research Portfolio
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Pose, Point
from nav_msgs.msg import Path
from std_msgs.msg import Header
import numpy as np

from src.algorithms.bees_algorithm import ModernizedBeesAlgorithm, PlanningConfig


class BeesPlannerNode(Node):
    """
    ROS2 Node for Bees Algorithm Path Planning
    
    Subscriptions:
        - /goal_pose: Goal position for path planning
        
    Publications:
        - /planned_path: Generated path
        - /robot_pose: Current robot position (simulated)
        
    Parameters:
        - n_scout_bees: Number of scout bees (default: 50)
        - n_elite_sites: Number of elite sites (default: 5)
        - max_iterations: Maximum iterations (default: 500)
    """
    
    def __init__(self):
        super().__init__('bees_planner')
        
        # Declare parameters
        self.declare_parameter('n_scout_bees', 50)
        self.declare_parameter('n_elite_sites', 5)
        self.declare_parameter('n_best_sites', 20)
        self.declare_parameter('max_iterations', 500)
        self.declare_parameter('adaptive_neighborhood', True)
        
        # Get parameters
        n_scout = self.get_parameter('n_scout_bees').value
        n_elite = self.get_parameter('n_elite_sites').value
        n_best = self.get_parameter('n_best_sites').value
        max_iter = self.get_parameter('max_iterations').value
        adaptive = self.get_parameter('adaptive_neighborhood').value
        
        # Initialize algorithm
        config = PlanningConfig(
            n_scout_bees=n_scout,
            n_elite_sites=n_elite,
            n_best_sites=n_best,
            max_iterations=max_iter,
            adaptive_neighborhood=adaptive
        )
        self.planner = ModernizedBeesAlgorithm(config)
        
        # State
        self.start_pos = np.array([0.0, 0.0])
        self.goal_pos = np.array([10.0, 10.0])
        self.obstacles = []
        
        # Publishers
        self.path_pub = self.create_publisher(Path, '/planned_path', 10)
        
        # Subscribers
        self.goal_sub = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )
        
        # Timer for planning (1 Hz)
        self.timer = self.create_timer(1.0, self.plan_callback)
        
        self.get_logger().info('Bees Planner Node initialized')
    
    def goal_callback(self, msg: PoseStamped):
        """Handle incoming goal pose"""
        self.goal_pos = np.array([msg.pose.position.x, msg.pose.position.y])
        self.get_logger().info(f'Received goal: {self.goal_pos}')
        
        # Trigger immediate replan
        self.publish_path()
    
    def plan_callback(self):
        """Periodic planning callback"""
        # In a real system, this would check if replanning is needed
        pass
    
    def publish_path(self):
        """Run planner and publish path"""
        try:
            path, stats = self.planner.run(self.start_pos, self.goal_pos, self.obstacles)
            
            # Convert to ROS message
            path_msg = Path()
            path_msg.header.stamp = self.get_clock().now().to_msg()
            path_msg.header.frame_id = 'map'
            
            for point in path:
                pose = PoseStamped()
                pose.header = path_msg.header
                pose.pose.position.x = float(point[0])
                pose.pose.position.y = float(point[1])
                pose.pose.position.z = 0.0
                path_msg.poses.append(pose)
            
            self.path_pub.publish(path_msg)
            self.get_logger().info(f'Published path with {len(path)} waypoints')
            
        except Exception as e:
            self.get_logger().error(f'Planning failed: {e}')
    
    def set_obstacles(self, obstacles: list):
        """Update obstacle list"""
        self.obstacles = [np.array(o) for o in obstacles]
    
    def set_start(self, x: float, y: float):
        """Set start position"""
        self.start_pos = np.array([x, y])


def main(args=None):
    rclpy.init(args=args)
    node = BeesPlannerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()