<?xml version="1.0"?>
<launch>
    <!-- 
    Swarm Path Planning - ROS Launch File
    
    This launch file starts the path planning simulation with the 
    Modernized Bees Algorithm.
    
    Usage:
        ros2 launch simulations launch_planning.launch.py
    -->
    
    <!-- Path Planning Node -->
    <node name="bees_planner" pkg="swarm_path_planning" exec="bees_planner_node">
        <param name="n_scout_bees" value="50"/>
        <param name="n_elite_sites" value="5"/>
        <param name="max_iterations" value="500"/>
        <param name="adaptive_neighborhood" value="true"/>
    </node>
    
    <!-- RViz for visualization -->
    <node name="rviz" pkg="rviz2" exec="rviz2" args="-d $(find-pkg-share swarm_path_planning)/config/planning.rviz"/>
    
    <!-- Static Transform Publisher -->
    <node name="static_transform_publisher" pkg="tf2_ros" exec="static_transform_publisher" 
          args="0 0 0 0 0 0 map odom"/>
    
</launch>