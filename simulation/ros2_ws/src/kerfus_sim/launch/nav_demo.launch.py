"""Navigation teaching demo: Gazebo room + robot + Nav2 + RViz + rqt_graph.

    ros2 launch kerfus_sim nav_demo.launch.py

Starts everything needed to explain the ROS 2 graph to a student:

  * Gazebo Fortress with worlds/room.sdf, the robot and the ros_gz_bridge
    (via sim.launch.py)
  * the full Nav2 stack on the reference map maps/room.yaml (map_server, AMCL,
    planner, controller, behaviors, BT navigator, ...)
  * RViz with map, costmaps, planned path, laser scan and robot model
    (rviz/nav.rviz)
  * rqt_graph, which draws the live node/topic graph
  * optional teleop in a new terminal (off by default; Nav2 drives)

Launch arguments:
    world:=/path/to/world.sdf   Gazebo world to load (default room.sdf)
    map:=/path/to/map.yaml      map for Nav2 (default maps/room.yaml)
    params_file:=/path/nav2_params.yaml
    rviz:=false                 do not start RViz
    rqt:=false                  do not start rqt_graph
    teleop:=true                open teleop_twist_keyboard in a new terminal

In RViz, use "2D Goal Pose" or "Nav2 Goal" to send the robot somewhere.
"""
import os
import shutil

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    LogInfo,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

# Command used to open a new terminal window, most common first.
TERMINALS = (
    ('gnome-terminal', ['--']),
    ('konsole', ['-e']),
    ('xfce4-terminal', ['-e']),
    ('mate-terminal', ['-e']),
    ('xterm', ['-e']),
    ('x-terminal-emulator', ['-e']),
)


def _terminal_prefix():
    """Return a terminal-emulator launch prefix string, or None."""
    for executable, option in TERMINALS:
        if shutil.which(executable):
            return ' '.join([executable, *option])
    return None


def generate_launch_description():
    pkg_share = get_package_share_directory('kerfus_sim')

    sim_launch = os.path.join(pkg_share, 'launch', 'sim.launch.py')
    navigation_launch = os.path.join(pkg_share, 'launch', 'navigation.launch.py')
    rqt_graph_launch = os.path.join(pkg_share, 'launch', 'rqt_graph.launch.py')
    rviz_config = os.path.join(pkg_share, 'rviz', 'nav.rviz')

    world = LaunchConfiguration('world')
    map_yaml = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    do_rviz = LaunchConfiguration('rviz')
    do_rqt = LaunchConfiguration('rqt')
    do_teleop = LaunchConfiguration('teleop')

    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(sim_launch),
        launch_arguments={'world': world}.items(),
    )

    nav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(navigation_launch),
        launch_arguments={
            'map': map_yaml,
            'params_file': params_file,
        }.items(),
    )

    # Give Gazebo time to load the world and spawn the robot before Nav2 starts
    # asking for TF and laser data.
    nav_after_spawn = TimerAction(period=10.0, actions=[nav])

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(do_rviz),
        output='screen',
    )

    rqt_graph = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rqt_graph_launch),
        condition=IfCondition(do_rqt),
    )

    actions = [
        DeclareLaunchArgument(
            'world',
            default_value=os.path.join(pkg_share, 'worlds', 'room.sdf'),
            description='Path to the Gazebo world (.sdf) to load'),
        DeclareLaunchArgument(
            'map',
            default_value=os.path.join(pkg_share, 'maps', 'room.yaml'),
            description='Full path to the Nav2 map .yaml file'),
        DeclareLaunchArgument(
            'params_file',
            default_value=os.path.join(pkg_share, 'config', 'nav2_params.yaml'),
            description='Full path to the Nav2 parameters file'),
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Start RViz with the navigation view'),
        DeclareLaunchArgument(
            'rqt', default_value='true',
            description='Start rqt_graph to show the ROS 2 node/topic graph'),
        DeclareLaunchArgument(
            'teleop', default_value='false',
            description='Also open teleop_twist_keyboard in a new terminal'),
        sim,
        nav_after_spawn,
        rviz,
        rqt_graph,
    ]

    prefix = _terminal_prefix()
    if prefix is None:
        actions.append(LogInfo(
            condition=IfCondition(do_teleop),
            msg='No terminal emulator found: run "ros2 run '
                'teleop_twist_keyboard teleop_twist_keyboard" in another '
                'terminal to drive the robot manually.'))
    else:
        actions.append(Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop_twist_keyboard',
            prefix=prefix,
            condition=IfCondition(do_teleop),
            output='screen',
        ))

    return LaunchDescription(actions)
