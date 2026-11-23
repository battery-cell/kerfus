# Kerfus

Kerfus is a small two-wheel differential-drive drink-delivery robot. The repository
contains the ESP32 firmware, the mechanical design, and a ROS 2 + Gazebo simulation
used to develop and demonstrate mapping and navigation.

## Layout

| Path | Contents |
|---|---|
| `src/`, `include/`, `lib/` | PlatformIO ESP32 firmware |
| `platformio.ini` | PlatformIO build configuration |
| `*.step`, `*.FCStd` | FreeCAD / STEP mechanical design |
| `simulation/` | ROS 2 workspace, Gazebo world, robot model, maps and launch files |

## Simulation quick start

Needs ROS 2 Humble, Gazebo Fortress and the Nav2 / SLAM / RViz packages:

```bash
sudo apt install ros-humble-ros-gz ros-humble-slam-toolbox \
                 ros-humble-navigation2 ros-humble-nav2-bringup \
                 ros-humble-teleop-twist-keyboard ros-humble-rviz2 \
                 ros-humble-rqt-graph

cd simulation
./run_sim.sh          # Gazebo + robot + SLAM + RViz + teleop
./run_sim.sh --nav    # Gazebo + robot + Nav2 + RViz + rqt_graph
```

The script builds the workspace and checks for missing packages. Use the first mode
to drive with teleop and watch the SLAM map grow; `--nav` runs Nav2 on the reference
map in `maps/room.yaml` and opens `rqt_graph` for explaining the ROS 2 graph.

Full documentation: [`simulation/ros2_ws/src/kerfus_sim/README.md`](simulation/ros2_ws/src/kerfus_sim/README.md)  
Troubleshooting: [`simulation/ros2_ws/src/kerfus_sim/docs/troubleshooting.md`](simulation/ros2_ws/src/kerfus_sim/docs/troubleshooting.md)

## Firmware

The ESP32 firmware is a PlatformIO project:

```bash
pio run
pio run --target upload
```

## Notes

The simulation still uses placeholder masses and lidar height. Replace them with
measured values in `simulation/ros2_ws/src/kerfus_sim/urdf/kerfus.urdf` before using
the model for hardware decisions.
