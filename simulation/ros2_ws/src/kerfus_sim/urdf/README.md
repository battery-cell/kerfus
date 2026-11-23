# urdf/

`kerfus.urdf` describes the robot: its links, joints, sensors and the Gazebo plugins.

## What is in it

| Link | Joint to the base | Notes |
|---|---|---|
| `base_link` | (root) | 280 x 280 x 80 mm box, origin at the centre of the underside |
| `wheel_left`, `wheel_right` | `continuous`, axis +Y, at y = +/-149.6 mm, z = 19.9 mm | 22 mm radius, 20 mm wide |
| `caster_front`, `caster_rear` | `fixed` | Simulation-only frictionless balls, x = +/-115 mm |
| `lidar_link` | `fixed`, at z = 127 mm | Carries the `gpu_lidar` sensor (360 samples, 0.15 to 12 m, 10 Hz) |

It also contains the Gazebo plugins: **DiffDrive** (listens to `/cmd_vel`, publishes odometry and
`odom -> base_link`) and **JointStatePublisher** (so the wheels turn in RViz).

## Get these, then edit the file

| Value | Currently | How to get the real one | Where in the file |
|---|---|---|---|
| Whole-robot mass | 3.0 kg (placeholder) | Weigh it, with battery, Raspberry Pi and motors | `base_link` `<mass>`, then the inertia |
| Wheel mass | 0.08 kg (placeholder) | Weigh one wheel | `wheel_left` / `wheel_right` |
| Lidar mass | 0.17 kg (placeholder) | Datasheet or a scale | `lidar_link` |
| Lidar scan height | 0.127 m (mid-head guess) | Datasheet: height of the laser plane above the base | `lidar_joint` `<origin>` z |
| Caster positions | +/-0.115 m | Where your real support wheels or skids are | `caster_*_joint` |
| Front of the robot | +X (assumed) | Decide which side is the front | Rotate the joints, or the whole robot, if it differs |

**Inertia** values were worked out from the shapes: a solid box for the body, a solid cylinder for the
wheels and lidar. If you change a mass, scale that link's `ixx iyy izz` by the same factor, or
recompute: for a box of mass `m` and sides `a,b,c`, `ixx = m/12 * (b^2 + c^2)`, and so on.

## Check it before simulating

```bash
sudo apt install liburdfdom-tools
check_urdf urdf/kerfus.urdf                       # prints the link tree, or the error

sudo apt install ros-humble-urdf-tutorial ros-humble-joint-state-publisher-gui
source /opt/ros/humble/setup.bash
ros2 launch urdf_tutorial display.launch.py model:=$PWD/urdf/kerfus.urdf
```

The second command opens RViz with sliders for the wheel joints, so you can see the axes and positions.
