"""Start rqt_graph, the live ROS 2 node/topic graph.

    ros2 launch kerfus_sim rqt_graph.launch.py

Useful on its own while another demo is running, for example:

    ./run_sim.sh --no-teleop          # in one terminal
    ros2 launch kerfus_sim rqt_graph.launch.py

`nav_demo.launch.py` includes this file automatically (rqt:=true).
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rqt_graph',
            executable='rqt_graph',
            output='screen',
        ),
    ])
