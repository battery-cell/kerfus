"""Build a map while you drive the robot (slam_toolbox, online asynchronous mode).

Run sim.launch.py first, then:

    ros2 launch kerfus_sim slam.launch.py

Drive with:  ros2 run teleop_twist_keyboard teleop_twist_keyboard
Save with:   ros2 run nav2_map_server map_saver_cli -f <path>/maps/room
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg_share = get_package_share_directory('kerfus_sim')
    slam_toolbox_share = get_package_share_directory('slam_toolbox')

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_share, 'launch', 'online_async_launch.py')),
        launch_arguments={
            'slam_params_file': os.path.join(pkg_share, 'config', 'slam_toolbox.yaml'),
            'use_sim_time': 'true',
        }.items(),
    )

    return LaunchDescription([slam])
