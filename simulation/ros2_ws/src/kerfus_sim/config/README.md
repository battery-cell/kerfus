# config/

Settings for the two programs that turn the lidar into maps and movement.

## What is in here

| File | Used by | What it does |
|---|---|---|
| `slam_toolbox.yaml` | `launch/slam.launch.py` | Builds the map while you drive |
| `nav2_params.yaml` | `launch/navigation.launch.py` | Localisation (AMCL), path planning, obstacle avoidance, speed limits |

You don't need to get anything for these now. Run the defaults first, then tune.

## What to tune, and when

**`nav2_params.yaml`**

| Setting | Now | Change it when |
|---|---|---|
| `robot_radius` (local and global costmap) | 0.22 m | The robot clips walls (raise it) or refuses doorways it should fit (lower it) |
| `max_vel_x`, `max_speed_xy`, `max_velocity` | 0.3 m/s | The robot is too slow, or spills drinks (lower it) |
| `max_vel_theta` | 1.0 rad/s | Turns are too jerky or too slow |
| `inflation_radius` | 0.55 m | The robot hugs obstacles (raise) or won't pass gaps (lower) |
| `xy_goal_tolerance` | 0.25 m | It should stop closer to the goal |
| `set_initial_pose` / `initial_pose` | true, (0,0,0) | The map was not made from the spawn point |

**`slam_toolbox.yaml`**

| Setting | Now | Change it when |
|---|---|---|
| `resolution` | 0.05 m | You want a finer or smaller map |
| `max_laser_range` | 12.0 m | You use a lidar with a different range |
| `minimum_travel_distance` | 0.2 m | The map updates too often or too rarely |

## Frames that must agree everywhere

`base_link`, `odom` and `map` are used in both files, in the URDF, and in the bridge. If you rename
the robot's root link, change it in **every** place.

## If Nav2 complains about a missing parameter

Compare with Nav2's own reference file, which ships with ROS:

```bash
diff /opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml config/nav2_params.yaml
```
