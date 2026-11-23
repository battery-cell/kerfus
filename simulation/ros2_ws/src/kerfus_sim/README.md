# Kerfus simulation

ROS 2 **Humble** + Gazebo **Fortress** (`ign gazebo`) package for the Kerfus robot: a two-wheel
differential-drive base with a 2D lidar (RPLIDAR A1M8 class) that maps rooms and navigates with
slam_toolbox and Nav2.

> **Status: written but not run.** The files were checked for syntax and for internal consistency
> (valid XML and YAML, a proper link tree, sane inertia values), but nothing here has been started in
> ROS or Gazebo yet. Expect to fix a few small things on the first launch. `docs/troubleshooting.md`
> lists the likely ones.

## Folder map

| Folder | What it is | What you still need to get for it |
|---|---|---|
| `cad/` | Your STEP / FreeCAD source files | Put your exports here, plus the lidar datasheet |
| `meshes/` | STL models for how the robot looks | Export 3 STL files from FreeCAD (optional: the simulation works with plain shapes) |
| `urdf/` | `kerfus.urdf`, the robot description | Real masses and the lidar scan height |
| `worlds/` | `room.sdf`, a 6 x 5 m test room | Your real room's dimensions (optional) |
| `config/` | slam_toolbox and Nav2 settings | Nothing now; tune after the first runs |
| `launch/` | Start-up scripts | Nothing |
| `maps/` | Where saved maps go | Make a map by driving the robot (see `maps/README.md`) |
| `docs/` | Measurements, assumptions, troubleshooting | Nothing |

Every folder has its own `README.md` saying what belongs in it.

## Install and build

```bash
sudo apt install ros-humble-ros-gz ros-humble-slam-toolbox ros-humble-navigation2 \
                 ros-humble-nav2-bringup ros-humble-teleop-twist-keyboard ros-humble-rviz2

mkdir -p ~/ros2_ws/src
cp -r simulation ~/ros2_ws/src/            # this folder, as it is
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select kerfus_sim --symlink-install
source install/setup.bash
```

`--symlink-install` matters: edits to the URDF, configs and saved maps then take effect without
rebuilding. The package name is `kerfus_sim`, whatever the folder is called.

## Run it

Use a new terminal for each step, and run `source ~/ros2_ws/install/setup.bash` in every one.

```bash
# 1. Gazebo + robot + bridge
ros2 launch kerfus_sim sim.launch.py

# 2. Drive it (keys shown in the terminal)
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 3. Look at it
ros2 run rviz2 rviz2        # Fixed Frame = odom (or map); add RobotModel, LaserScan /scan, TF
```

**Make a map**

```bash
ros2 launch kerfus_sim slam.launch.py                  # then drive around the whole room
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/simulation/maps/room
```

**Navigate on it** (stop the SLAM launch first)

```bash
ros2 launch kerfus_sim navigation.launch.py
```

In RViz, add a **Map** display (`/map`), click **2D Pose Estimate** if the robot isn't where AMCL thinks,
then **Nav2 Goal** to send it somewhere.

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
