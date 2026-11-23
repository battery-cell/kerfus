"""Navigate on a saved map (Nav2). Run sim.launch.py first, then:

    ros2 launch kerfus_sim navigation.launch.py
    ros2 launch kerfus_sim navigation.launch.py map:=/full/path/to/room.yaml

The default map is maps/room.yaml in this package: create it first with slam.launch.py
and map_saver_cli (see maps/README.md). Do not run slam.launch.py at the same time.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_share = get_package_share_directory('kerfus_sim')
    nav2_share = get_package_share_directory('nav2_bringup')

    map_yaml = LaunchConfiguration('map')
    params = LaunchConfiguration('params_file')

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_yaml,
            'params_file': params,
            'use_sim_time': 'true',
            'autostart': 'true',
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('map',
                              default_value=os.path.join(pkg_share, 'maps', 'room.yaml'),
                              description='Full path to the map .yaml file'),
        DeclareLaunchArgument('params_file',
                              default_value=os.path.join(pkg_share, 'config', 'nav2_params.yaml'),
                              description='Full path to the Nav2 parameters file'),
        nav2,
    ])
