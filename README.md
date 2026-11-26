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
# Kerfus — ROS 2 Operating Guide

**Platform:** Zorin OS / Ubuntu 22.04  
**ROS distribution:** ROS 2 Humble  
**Simulator:** Gazebo Fortress  
**Workspace:** `~/freecadprojects/kerfus/simulation/ros2_ws`

---

## 1. Project structure

The relevant project files are organized like this:

```text
kerfus/
└── simulation/
    └── ros2_ws/
        ├── src/
        │   └── kerfus_sim/
        │       ├── urdf/
        │       ├── worlds/
        │       ├── launch/
        │       └── config/
        ├── build/
        ├── install/
        └── log/
```

The workspace contains the Kerfus simulation package, its URDF robot description, Gazebo world, launch files and configuration.

## 2. Preparing the ROS 2 environment

Every new terminal needs to load the ROS 2 environment.

Run:

```bash
source /opt/ros/humble/setup.bash
```

Then load the Kerfus workspace:

```bash
source ~/freecadprojects/kerfus/simulation/ros2_ws/install/setup.bash
```

You can combine these into one command:

```bash
source /opt/ros/humble/setup.bash && \
source ~/freecadprojects/kerfus/simulation/ros2_ws/install/setup.bash
```

**Important:** You need to source both environments in every new terminal that will use Kerfus packages.

## 3. Building the workspace

You only need to rebuild when you change package source code, URDF files, launch files or other installed configuration.

```bash
cd ~/freecadprojects/kerfus/simulation/ros2_ws

source /opt/ros/humble/setup.bash

colcon build --symlink-install
```

After building, load the workspace:

```bash
source install/setup.bash
```

The `--symlink-install` option makes development easier because many changes to package files do not require reinstalling the package.

## 4. Starting the Gazebo simulation

Open **Terminal 1**.

Load ROS 2 and the workspace:

```bash
source /opt/ros/humble/setup.bash

source ~/freecadprojects/kerfus/simulation/ros2_ws/install/setup.bash
```

Start Kerfus:

```bash
ros2 launch kerfus_sim sim.launch.py
```

This launches:
- Gazebo Fortress.
- The Kerfus robot.
- The simulated differential-drive system.
- The simulated RPLIDAR.
- Robot state and odometry publishing.

Wait until the simulation has finished loading.

## 5. Starting the simulated LIDAR bridge

Gazebo Fortress uses Ignition Transport messages, while ROS 2 uses ROS messages.

The bridge converts the simulated laser scan into a ROS 2 `LaserScan` message.

Open **Terminal 2**:

```bash
source /opt/ros/humble/setup.bash

ros2 run ros_gz_bridge parameter_bridge \
/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan
```

This makes the simulated LIDAR available through:

```text
/scan
```

Check whether scans are being published:

```bash
ros2 topic hz /scan
```

Expected frequency: approximately 10 Hz.

Inspect a scan:

```bash
ros2 topic echo /scan --once
```

The simulated scanner is configured for:
- 360 samples.
- 10 Hz update rate.
- 0.15 m minimum range.
- 12 m maximum range.

## 6. Starting RViz2

Open **Terminal 3**:

```bash
source /opt/ros/humble/setup.bash

source ~/freecadprojects/kerfus/simulation/ros2_ws/install/setup.bash

rviz2
```

Configure RViz2:

**Fixed Frame:**

```text
odom
```

Add the following displays:

| Display | Configuration |
|---|---|
| RobotModel | Default |
| TF | Default |
| LaserScan | Topic: `/scan` |
| Odometry | Topic: `/odom` |

You should now see the robot model, coordinate frames and LIDAR measurements.

The LIDAR frame in the URDF is `lidar_link`.

## 7. Manually controlling Kerfus

Kerfus receives movement commands through:

```text
/cmd_vel
```

The message type is:

```text
geometry_msgs/msg/Twist
```

For a differential-drive robot, the relevant values are:

| Field | Meaning | Unit |
|---|---|---|
| `linear.x` | Forward/backward velocity | m/s |
| `angular.z` | Rotation velocity | rad/s |

### Drive forward

Open **Terminal 4**:

```bash
source /opt/ros/humble/setup.bash

ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.2}, angular: {z: 0.0}}"
```

This commands the robot to move forward at 0.2 m/s.

### Drive backward

```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: -0.2}, angular: {z: 0.0}}"
```

### Turn left

```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0}, angular: {z: 0.5}}"
```

### Turn right

```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0}, angular: {z: -0.5}}"
```

### Drive and turn simultaneously

```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.2}, angular: {z: 0.5}}"
```

### Stop

Send a zero velocity command:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0}, angular: {z: 0.0}}"
```

Press `Ctrl+C` to stop a continuously running publisher.

## 8. Understanding differential-drive movement

Kerfus uses two powered wheels.

The robot turns by changing the speed of its left and right wheels.

Its current dimensions:

| Parameter | Value |
|---|---:|
| Wheel radius | 0.022 m |
| Wheel separation | 0.2992 m |

The wheel velocity equations are:

```text
Left wheel:
vL = v - (angular_velocity × wheel_separation / 2)

Right wheel:
vR = v + (angular_velocity × wheel_separation / 2)
```

Where:
- `v` is the requested forward velocity.
- `angular_velocity` is the requested turning velocity.
- `vL` and `vR` are the left and right wheel linear velocities.

Wheel RPM is calculated using:

```text
RPM = (wheel_velocity / wheel_radius) × 60 / (2 × PI)
```

The Gazebo differential-drive plugin performs this conversion automatically in simulation.

For the real robot, we'll implement the equivalent calculation in the Raspberry Pi's ROS 2 control node.

## 9. Useful ROS 2 debugging commands

### List all topics

```bash
ros2 topic list
```

### Inspect a topic's message type

```bash
ros2 topic type /scan
```

### Monitor LIDAR

```bash
ros2 topic echo /scan
```

### Monitor odometry

```bash
ros2 topic echo /odom
```

### Monitor wheel joint states

```bash
ros2 topic echo /joint_states
```

### Monitor movement commands

```bash
ros2 topic echo /cmd_vel
```

### Check LIDAR publishing frequency

```bash
ros2 topic hz /scan
```

### Check odometry frequency

```bash
ros2 topic hz /odom
```

### Inspect the robot's TF transform

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

### Display the ROS 2 node graph

```bash
rqt_graph
```

This displays the nodes and their connections.

## 10. SLAM and navigation

Kerfus has separate launch files prepared for SLAM and navigation:

```text
launch/
├── sim.launch.py
├── slam.launch.py
└── navigation.launch.py
```

The intended sequence is:

1. Start Gazebo.
2. Start the simulated LIDAR bridge.
3. Start SLAM Toolbox.
4. Open RViz2.
5. Drive Kerfus around to build a map.
6. Save the map.
7. Start navigation using the saved map.

Start SLAM:

```bash
ros2 launch kerfus_sim slam.launch.py
```

Start navigation when a suitable map and navigation configuration are ready:

```bash
ros2 launch kerfus_sim navigation.launch.py
```

These launch files may have their own dependencies and launch arguments, so check their configuration if they fail.

## 11. Physical RPLIDAR A1M8-R6

When using the actual RPLIDAR instead of the Gazebo scanner, you will use the Slamtec ROS 2 driver.

Repository:

https://github.com/Slamtec/sllidar_ros2

Download:

```bash
cd ~/freecadprojects/kerfus/simulation/ros2_ws/src

git clone https://github.com/Slamtec/sllidar_ros2.git
```

Install dependencies and build:

```bash
cd ~/freecadprojects/kerfus/simulation/ros2_ws

source /opt/ros/humble/setup.bash

rosdep install --from-paths src --ignore-src -r -y

colcon build --symlink-install --packages-select sllidar_ros2
```

Give your user serial-port permissions:

```bash
sudo usermod -aG dialout $USER
```

Log out and back in, or reboot.

Check the scanner's serial port:

```bash
ls /dev/ttyUSB*
```

Start the physical A1 scanner:

```bash
source /opt/ros/humble/setup.bash

source ~/freecadprojects/kerfus/simulation/ros2_ws/install/setup.bash

ros2 launch sllidar_ros2 sllidar_a1_launch.py \
serial_port:=/dev/ttyUSB0 \
serial_baudrate:=115200 \
frame_id:=lidar_link \
inverted:=false \
angle_compensate:=true
```

**Important:** Do not run the Gazebo LIDAR bridge and physical LIDAR driver simultaneously while both publish to `/scan`. Use one scan source at a time.

## 12. Future real-robot architecture

The planned physical robot will use the Raspberry Pi 4 and ESP32 together.

```text
             Raspberry Pi 4
             Ubuntu 22.04
             ROS 2 Humble
                   |
          +--------+--------+
          |                 |
       SLAM Toolbox       Nav2
          |                 |
          +--------+--------+
                   |
                /cmd_vel
                   |
            Python ROS 2 node
                   |
               UART serial
                   |
                 ESP32
              C++ firmware
                   |
          +--------+--------+
          |                 |
       Left motor       Right motor
          |                 |
       Encoder           Encoder
          +--------+--------+
                   |
             ESP32 feedback
                   |
              Raspberry Pi
                   |
             /odom and TF
```

### Raspberry Pi responsibilities

- ROS 2.
- SLAM Toolbox.
- Nav2.
- LIDAR processing.
- High-level movement commands.
- UART communication.
- Odometry integration.

### ESP32 responsibilities

- Reading wheel encoders.
- Left and right motor PID control.
- PWM generation.
- Motor direction control.
- Sending wheel feedback.
- Emergency motor stop on communication timeout.

The ESP32 will use a watchdog timeout so that loss of communication causes the motors to stop.

---

## 13. Quick-start cheat sheet

For normal simulation sessions, these are the only commands you need.

**Terminal 1 — Gazebo:**

```bash
source /opt/ros/humble/setup.bash
source ~/freecadprojects/kerfus/simulation/ros2_ws/install/setup.bash
ros2 launch kerfus_sim sim.launch.py
```

**Terminal 2 — LIDAR bridge:**

```bash
source /opt/ros/humble/setup.bash
ros2 run ros_gz_bridge parameter_bridge \
/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan
```

**Terminal 3 — RViz2:**

```bash
source /opt/ros/humble/setup.bash
source ~/freecadprojects/kerfus/simulation/ros2_ws/install/setup.bash
rviz2
```

**Terminal 4 — Drive forward:**

```bash
source /opt/ros/humble/setup.bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.2}, angular: {z: 0.0}}"
```

**Stop:**

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0}, angular: {z: 0.0}}"
```

---

**Remember:** Gazebo simulates the robot and its sensors. The ROS 2 nodes communicate with the simulation through topics. When we move to the physical Kerfus, the simulated differential-drive system will be replaced by the Raspberry Pi and ESP32 motor-control interface, while keeping the same `/cmd_vel`, `/scan`, `/odom` and TF interfaces wherever possible.
