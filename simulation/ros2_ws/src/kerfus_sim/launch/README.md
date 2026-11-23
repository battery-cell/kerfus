# launch/

Start-up scripts. Each one is run with `ros2 launch kerfus_sim <name>`. You need to get nothing for this folder.

## What is in here

| File | What it starts | Run |
|---|---|---|
| `bringup.launch.py` | Everything for the SLAM demo: sim + slam + RViz + teleop | `./run_sim.sh` or `ros2 launch kerfus_sim bringup.launch.py` |
| `sim.launch.py` | Gazebo with the room, the robot, `robot_state_publisher`, and the bridge | First, always |
| `slam.launch.py` | slam_toolbox, to build a map | While driving, to make a map |
| `navigation.launch.py` | Nav2 with a saved map | Instead of SLAM, once a map exists |

Run **`slam` or `navigation`, not both**. They both want to publish the `map -> odom` transform.

## Options

```bash
ros2 launch kerfus_sim bringup.launch.py                 # full demo
ros2 launch kerfus_sim bringup.launch.py teleop:=false   # no teleop window
ros2 launch kerfus_sim bringup.launch.py slam:=false     # Gazebo + RViz only
ros2 launch kerfus_sim bringup.launch.py world:=/path/to/other.sdf
ros2 launch kerfus_sim sim.launch.py world:=/path/to/other.sdf
ros2 launch kerfus_sim navigation.launch.py map:=/full/path/room.yaml params_file:=/full/path/my_params.yaml
```

`bringup.launch.py` uses `rviz/slam.rviz`: fixed frame `map`, with RobotModel, LaserScan, Map and
TF displays. The map is empty until the robot moves and slam_toolbox publishes it.

## Topics the bridge connects (in `sim.launch.py`)

| ROS 2 topic | Direction | Type |
|---|---|---|
| `/clock` | Gazebo to ROS | `rosgraph_msgs/Clock` |
| `/scan` | Gazebo to ROS | `sensor_msgs/LaserScan` |
| `/odom` | Gazebo to ROS | `nav_msgs/Odometry` |
| `/tf` | Gazebo to ROS | `tf2_msgs/TFMessage` (`odom -> base_link`) |
| `/joint_states` | Gazebo to ROS | `sensor_msgs/JointState` |
| `/cmd_vel` | ROS to Gazebo | `geometry_msgs/Twist` |

The Gazebo-side type names say `ignition.msgs.*` because Humble pairs with Gazebo Fortress. If you
ever move to a newer ROS and Gazebo, they become `gz.msgs.*`.

## The simulation does not start

Gazebo is launched with `ign gazebo -r <world>`. If `ign` is not found, check that
`ros-humble-ros-gz` is installed, or run `ign gazebo -r worlds/room.sdf` in a separate terminal
and launch everything else by hand. `docs/troubleshooting.md` has more.
