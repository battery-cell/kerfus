"""One-command demo: Gazebo room + robot + SLAM + RViz + teleop.

    ros2 launch kerfus_sim bringup.launch.py

This is a convenience wrapper around sim.launch.py and slam.launch.py. It
starts everything needed to watch a map being built while you drive:

  * Gazebo Fortress with worlds/room.sdf
  * the Kerfus robot and the ros_gz_bridge (via sim.launch.py)
  * slam_toolbox in online-async mapping mode (via slam.launch.py)
  * RViz with the Map, LaserScan, TF and RobotModel displays (rviz/slam.rviz)
  * teleop_twist_keyboard in a new terminal window

Launch arguments:
    world:=/path/to/world.sdf   Gazebo world to load (default room.sdf)
    slam:=false                 do not start slam_toolbox
    rviz:=false                 do not start RViz
    teleop:=false               do not open the teleop terminal

If no terminal emulator is found, teleop is skipped: run
`ros2 run teleop_twist_keyboard teleop_twist_keyboard` in another terminal.
"""
import os
import shutil

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    LogInfo,
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
    """Return the prefix tokens for a terminal emulator, or None."""
    for executable, option in TERMINALS:
        if shutil.which(executable):
            return [executable, *option]
    return None


def generate_launch_description():
    pkg_share = get_package_share_directory('kerfus_sim')

    sim_launch = os.path.join(pkg_share, 'launch', 'sim.launch.py')
    slam_launch = os.path.join(pkg_share, 'launch', 'slam.launch.py')
    rviz_config = os.path.join(pkg_share, 'rviz', 'slam.rviz')

    world = LaunchConfiguration('world')
    do_slam = LaunchConfiguration('slam')
    do_rviz = LaunchConfiguration('rviz')
    do_teleop = LaunchConfiguration('teleop')

    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(sim_launch),
        launch_arguments={'world': world}.items(),
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_launch),
        condition=IfCondition(do_slam),
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(do_rviz),
        output='screen',
    )

    actions = [
        DeclareLaunchArgument(
            'world',
            default_value=os.path.join(pkg_share, 'worlds', 'room.sdf'),
            description='Path to the Gazebo world (.sdf) to load'),
        DeclareLaunchArgument(
            'slam', default_value='true',
            description='Start slam_toolbox and build a map while driving'),
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Start RViz with the SLAM view'),
        DeclareLaunchArgument(
            'teleop', default_value='true',
            description='Open teleop_twist_keyboard in a new terminal'),
        sim,
        slam,
        rviz,
    ]

    prefix = _terminal_prefix()
    if prefix is None:
        actions.append(LogInfo(
            condition=IfCondition(do_teleop),
            msg='No terminal emulator found: run "ros2 run '
                'teleop_twist_keyboard teleop_twist_keyboard" in another '
                'terminal to drive the robot.'))
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
