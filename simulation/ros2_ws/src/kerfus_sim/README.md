# Kerfus simulation

ROS 2 **Humble** + Gazebo **Fortress** (`ign gazebo`) package for the Kerfus robot: a two-wheel
differential-drive base with a 2D lidar (RPLIDAR A1M8 class) that maps rooms and navigates with
slam_toolbox and Nav2.

> **Status:** the Gazebo + SLAM + teleop demo has been run. The Nav2 teaching demo is prepared
> against a reference map and needs the full Nav2 stack installed (`ros-humble-navigation2`,
> `ros-humble-nav2-bringup`). `docs/troubleshooting.md` lists the likely first-launch problems.

## Folder map

| Folder | What it is | What you still need to get for it |
|---|---|---|
| `cad/` | Your STEP / FreeCAD source files | Put your exports here, plus the lidar datasheet |
| `meshes/` | STL models for how the robot looks | Export 3 STL files from FreeCAD (optional: the simulation works with plain shapes) |
| `urdf/` | `kerfus.urdf`, the robot description | Real masses and the lidar scan height |
| `worlds/` | `room.sdf`, a 6 x 5 m test room | Your real room's dimensions (optional) |
| `config/` | slam_toolbox and Nav2 settings | Nothing now; tune after the first runs |
| `launch/` | Start-up scripts | Nothing |
| `rviz/` | `slam.rviz` and `nav.rviz` views | Nothing |
| `maps/` | Reference map plus maps saved from SLAM | `maps/room.yaml` is generated from the world; replace it with a real mapping run for the real robot |
| `docs/` | Measurements, assumptions, troubleshooting | Nothing |

Every folder has its own `README.md` saying what belongs in it.

## Install

```bash
sudo apt install ros-humble-ros-gz ros-humble-slam-toolbox ros-humble-navigation2 \
                 ros-humble-nav2-bringup ros-humble-teleop-twist-keyboard ros-humble-rviz2 \
                 ros-humble-rqt-graph
```

The repository already contains a ROS 2 workspace at `simulation/ros2_ws`, so the quickest way is
to build and run it in place from the repository's `simulation/` folder:

```bash
cd simulation
./run_sim.sh
```

`run_sim.sh` sources ROS 2 Humble, builds `kerfus_sim` with `colcon build --symlink-install` and
starts the demo. `--symlink-install` matters: edits to the URDF, configs and saved maps then take
effect without rebuilding. The package name is `kerfus_sim`, whatever the folder is called.

To use the package in a different workspace instead:

```bash
mkdir -p ~/ros2_ws/src
cp -r simulation/ros2_ws/src/kerfus_sim ~/ros2_ws/src/
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select kerfus_sim --symlink-install
source install/setup.bash
```

## Run it

From the repository's `simulation/` folder:

```bash
./run_sim.sh
```

This is the whole demo in one command: Gazebo with the test room, the robot and the bridge,
slam_toolbox, RViz with the SLAM view, and teleop in a new terminal window. Drive the robot around
with the keys printed in the teleop window; the occupancy grid in RViz grows as the lidar sees the
walls and obstacles. Ctrl-C in the script terminal stops everything.

Useful variants:

```bash
./run_sim.sh --nav                         # Nav2 + RViz + rqt_graph demo
./run_sim.sh --no-build                    # skip the build after the first run
./run_sim.sh world:=/path/to/other.sdf     # use a different Gazebo world
./run_sim.sh teleop:=false                 # do not open the teleop window
./run_sim.sh rviz:=false slam:=false       # Gazebo only
```

If no terminal emulator is available (for example over SSH), run teleop in another terminal:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Manual start

Use a new terminal for each step. From the repository root, run
`source simulation/ros2_ws/install/setup.bash` in every one (or source the workspace you built in).

```bash
# 1. Gazebo + robot + bridge
ros2 launch kerfus_sim sim.launch.py

# 2. SLAM (builds the map while you drive)
ros2 launch kerfus_sim slam.launch.py

# 3. Drive it (keys shown in the terminal)
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 4. Look at it
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix kerfus_sim)/share/kerfus_sim/rviz/slam.rviz
```

You can also start all of it through the launch file without the wrapper script:

```bash
ros2 launch kerfus_sim bringup.launch.py
```

**Make a map**

`slam.launch.py` is already running when you use `bringup.launch.py` or `run_sim.sh`, so just
drive around the whole room, then save:

```bash
# from the repository's simulation/ folder
ros2 run nav2_map_server map_saver_cli -f ros2_ws/src/kerfus_sim/maps/room
```

**Navigation + rqt_graph demo** (for teaching how ROS works)

```bash
./run_sim.sh --nav
```

This starts the same Gazebo room and robot, but instead of SLAM it runs the full Nav2 stack on the
reference map `maps/room.yaml`, opens `rviz/nav.rviz` (map, global/local costmaps, planned path,
scan, robot) and starts `rqt_graph`. Use the **Nav2 Goal** tool in RViz to send the robot somewhere.
In rqt_graph follow the chain:

```
Gazebo -> ros_gz_bridge -> /scan, /odom, /tf -> AMCL + Nav2 -> /cmd_vel -> ros_gz_bridge -> Gazebo
```

You can also open the graph next to any other demo:

```bash
ros2 launch kerfus_sim rqt_graph.launch.py
```

The reference map is generated from the world by `maps/generate_room_map.py` (see `maps/README.md`).
To navigate on a map you built with SLAM, pass it explicitly:

```bash
./run_sim.sh --nav map:=/full/path/to/room.yaml
```

**Navigate on it** (stop the SLAM launch first)

`nav_demo.launch.py` runs the simulation and Nav2 together. If you prefer separate terminals:

```bash
ros2 launch kerfus_sim sim.launch.py
ros2 launch kerfus_sim navigation.launch.py \
  map:=$(pwd)/simulation/ros2_ws/src/kerfus_sim/maps/room.yaml
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix kerfus_sim)/share/kerfus_sim/rviz/nav.rviz
ros2 run rqt_graph rqt_graph
```

In RViz, click **2D Pose Estimate** if the robot isn't where AMCL thinks, then **Nav2 Goal** to
send it somewhere.

## Quick checks

```bash
ros2 topic hz /scan                                   # about 10 Hz
ros2 topic echo /scan --once --field header.frame_id  # should print lidar_link
ros2 run tf2_tools view_frames                        # want: map -> odom -> base_link -> lidar_link
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}}"   # robot moves forward
```

## Numbers you should replace

These were not measurable from your CAD, so they are placeholders:

- **Masses**: body 3.0 kg, wheels 0.08 kg each, lidar 0.17 kg. Weigh the robot and edit `urdf/kerfus.urdf`.
- **Lidar scan height**: the frame is put at 0.127 m, mid-head. Check the RPLIDAR A1 datasheet.
- **Casters**: your CAD shows two wheels only, so two ball casters were added for the simulation.
- **"Forward"**: +X is assumed to be the front of the robot.

What was measured, and how, is in `docs/measured_dimensions.md`.
