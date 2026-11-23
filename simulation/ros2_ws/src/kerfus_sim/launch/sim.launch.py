"""Start Gazebo with the test room, spawn the robot and connect it to ROS 2.

    ros2 launch kerfus_sim sim.launch.py
    ros2 launch kerfus_sim sim.launch.py world:=/path/to/other_world.sdf

Starts: Gazebo (ign gazebo), robot_state_publisher, the robot spawn, and the
ros_gz_bridge for /clock, /scan, /odom, /tf, /cmd_vel and /joint_states.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

WORLD_NAME = 'kerfus_room'   # must match <world name="..."> in worlds/room.sdf
MODEL_NAME = 'kerfus'        # must match <robot name="..."> in urdf/kerfus.urdf


def generate_launch_description():
    pkg_share = get_package_share_directory('kerfus_sim')
    urdf_path = os.path.join(pkg_share, 'urdf', 'kerfus.urdf')
    default_world = os.path.join(pkg_share, 'worlds', 'room.sdf')

    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    # Lets Gazebo resolve package://kerfus_sim/meshes/... (only needed once you use real meshes).
    resource_path = os.pathsep.join(
        p for p in (os.path.dirname(pkg_share),
                    os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')) if p)

    world = LaunchConfiguration('world')

    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', world],
        additional_env={'IGN_GAZEBO_RESOURCE_PATH': resource_path},
        output='screen',
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
        output='screen',
    )

    # Wait a few seconds so Gazebo has finished loading the world before spawning.
    spawn = TimerAction(
        period=6.0,
        actions=[Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-world', WORLD_NAME, '-file', urdf_path,
                       '-name', MODEL_NAME, '-x', '0', '-y', '0', '-z', '0.02'],
            output='screen',
        )],
    )

    joint_state_topic = f'/world/{WORLD_NAME}/model/{MODEL_NAME}/joint_state'
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Humble + Gazebo Fortress use the "ignition.msgs" type names.
            # '[' = Gazebo -> ROS, ']' = ROS -> Gazebo.
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            f'{joint_state_topic}@sensor_msgs/msg/JointState[ignition.msgs.Model',
        ],
        remappings=[(joint_state_topic, '/joint_states')],
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument('world', default_value=default_world,
                              description='Path to the Gazebo world (.sdf) to load'),
        gazebo,
        robot_state_publisher,
        spawn,
        bridge,
    ])
