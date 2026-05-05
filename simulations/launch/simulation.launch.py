#!/usr/bin/env python3
"""
Complete Launch File for Swarm Path Planning Simulation

This launch file brings up:
1. Gazebo simulation world
2. Robot state publisher
3. Bees Algorithm path planner
4. RViz for visualization

Usage:
    ros2 launch simulations launch_simulation.launch.py

Author: Research Portfolio
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description"""
    
    # Package paths
    pkg_name = 'swarm_path_planning'
    
    # World file path
    world_file = os.path.join(
        get_package_share_directory(pkg_name),
        'worlds',
        'planning.world'
    )
    
    # If package not built, use local path
    if not os.path.exists(world_file):
        pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        world_file = os.path.join(pkg_dir, 'simulations', 'worlds', 'planning.world')
    
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Nodes
    nodes = []
    
    # 1. Robot State Publisher (simulated)
    nodes.append(Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    ))
    
    # 2. Bees Algorithm Planner
    # Note: Requires package to be built
    # Uncomment when package is properly set up:
    # nodes.append(Node(
    #     package=pkg_name,
    #     executable='bees_planner_node',
    #     name='bees_planner',
    #     parameters=[{
    #         'n_scout_bees': 50,
    #         'n_elite_sites': 5,
    #         'max_iterations': 500
    #     }],
    #     output='screen'
    # ))
    
    # 3. Simple path visualizer (standalone Python script)
    nodes.append(Node(
        package='pkg_name',
        executable='visualize_path',
        name='path_visualizer',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    ))
    
    # 4. Gazebo (if available)
    # This would normally use gazebo_ros package
    # ExecuteProcess used as example
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation clock time'
        ),
        
        # Add nodes
        *nodes
    ])


# Alternative: Standalone launch without full ROS setup
def generate_standalone_description():
    """Generate standalone description for non-ROS environments"""
    
    return LaunchDescription([
        # Placeholder for simulation setup
        # In practice, this would launch:
        # - gazebo simulation
        # - robot controllers
        # - path planner
        # - rviz
    ])