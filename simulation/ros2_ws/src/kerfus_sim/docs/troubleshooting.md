# Troubleshooting

The Gazebo + SLAM + teleop demo has been run. The Nav2 demo additionally needs the full Nav2
stack installed. Run `source ~/ros2_ws/install/setup.bash` in every terminal first (or use the
workspace inside `simulation/ros2_ws`).

| Symptom | Likely cause | What to do |
|---|---|---|
| `run_sim.sh` prints `missing packages` | ROS 2 Humble / Gazebo / slam_toolbox / RViz not installed | Run the `sudo apt install ...` line it prints, then start it again |
| `run_sim.sh --nav` prints `missing packages: ros-humble-nav2-bringup` | The full Nav2 stack is not installed | `sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup` |
| `ros2 launch ... nav_demo` says `nav2_bringup` not found | Only `nav2_map_server` / parts of Nav2 are installed | Install `ros-humble-navigation2` and `ros-humble-nav2-bringup` |
| No map in RViz in `--nav` mode | RViz map display durability is Volatile, or map_server failed | `ros2 topic info /map -v`; the map is latched (Transient Local), reload `nav.rviz` |
| Nav2 Goal does nothing | No `map -> odom` transform, or Nav2 is still starting | Wait 10 s after launch, check `/cmd_vel` and `ros2 run tf2_tools view_frames` |
| rqt_graph window is empty | Nodes have not started, or the graph filter hides them | Wait for Nav2, press the refresh button, or untick "Hide dead sinks" |
| `libEGL warning: egl: failed to create dri2 screen` | Harmless graphics warning | Ignore it if the window opens |
| Segmentation fault when closing Gazebo | Known Fortress GUI exit bug | Ignore it |
| Gazebo window is black or the lidar sensor errors | The `ogre2` renderer does not suit your graphics driver | In `worlds/room.sdf` change `ogre2` to `ogre`; or try `LIBGL_ALWAYS_SOFTWARE=1 ros2 launch kerfus_sim sim.launch.py` |
| Room appears but the robot doesn't | Gazebo was not ready when the spawn ran | Run it by hand: `ros2 run ros_gz_sim create -world kerfus_room -file ~/ros2_ws/src/simulation/urdf/kerfus.urdf -name kerfus -z 0.02` |
| Robot appears, then falls through the floor or tips over | Wrong inertia, or a missing caster | Check `urdf/kerfus.urdf`: casters are present, masses are not 0 |
| `/scan` is missing | The `Sensors` plugin is missing, or the sensor failed | `ign topic -l \| grep scan`; `ign topic -e -t /scan` shows raw Gazebo data; check the world still has the `Sensors` plugin |
| `/scan` exists but is all `inf` | Nothing within 12 m is **drawn** (the lidar sees visuals), or the robot is inside a wall | Check the obstacle has a `<visual>`; check the spawn point |
| `ros2 topic echo /scan --once --field header.frame_id` prints something other than `lidar_link` (for example `kerfus/lidar_link/rplidar_a1`) | The sensor frame name was not applied | Add a bridge: `ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 lidar_link kerfus/lidar_link/rplidar_a1` (use the exact name printed) |
| Robot ignores `/cmd_vel` | Bridge not running, or the plugin did not load | `ign topic -l \| grep cmd_vel`; `ros2 topic info /cmd_vel`; read the Gazebo terminal for plugin errors |
| Robot drives backwards or turns the wrong way | A wheel axis is inverted | Both wheel joints use axis `0 1 0`; if you changed the CAD frames, check the sign |
| RViz: `Frame [odom] does not exist` | `/tf` is not arriving | `ros2 topic echo /tf --once`; check the `/tf` line in the bridge |
| RViz: no `wheel_left` / `wheel_right` frames | `/joint_states` is not bridged | `ros2 topic echo /joint_states --once`; the joint-state topic name contains the world and model names, so they must be `kerfus_room` and `kerfus` |
| slam_toolbox: `Message Filter dropping message` | Scan frame is not in the TF tree | Check the frame_id line above, and `ros2 run tf2_tools view_frames` |
| slam_toolbox: the map doesn't grow | Robot hasn't moved far enough, or no clock | Drive at least 0.2 m; check `ros2 topic hz /clock` |
| Nav2: `map_server` fails | `maps/room.yaml` doesn't exist | Make and save a map (`maps/README.md`), or pass `map:=/full/path/room.yaml` |
| Nav2: `Failed to transform initial pose` or AMCL silent | No map-to-odom yet | Wait a few seconds, then use RViz **2D Pose Estimate** |
| Nav2: robot won't enter a gap it should fit | Inflation too large | Lower `robot_radius` or `inflation_radius` in `config/nav2_params.yaml` |
| Package or parameter errors from a launch file | A name differs in your Humble install | Run the command with `--show-args`, and compare with the file in `/opt/ros/humble/share/<package>/launch` |

## Useful commands

```bash
ros2 node list ; ros2 topic list                  # what is running
ros2 run tf2_tools view_frames                    # writes frames.pdf: want map -> odom -> base_link -> lidar_link
ign topic -l                                      # Gazebo-side topics
ign gazebo --versions                             # confirms Fortress
```
