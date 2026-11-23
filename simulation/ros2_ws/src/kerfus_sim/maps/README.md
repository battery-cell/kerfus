# maps/

Saved maps of rooms. **This folder is empty on purpose**: you make the map by driving the robot.
Nav2 needs a map before `navigation.launch.py` will work.

## Get a map

1. Start the simulation, SLAM and teleop in one command (from the repository's `simulation/`
   folder):

```bash
./run_sim.sh
```

Or start the pieces by hand:

```bash
ros2 launch kerfus_sim sim.launch.py
ros2 launch kerfus_sim slam.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix kerfus_sim)/share/kerfus_sim/rviz/slam.rviz
```

RViz opens with **Fixed Frame = map** and a **Map** display on `/map`. The map starts empty (grey)
and fills in as the robot drives.

2. Drive slowly around the room, along every wall, and past each obstacle, until the map in RViz is
   complete. Drive a loop back to the start so slam_toolbox can correct drift.

3. Save it:

```bash
# from the repository's simulation/ folder
ros2 run nav2_map_server map_saver_cli -f ros2_ws/src/kerfus_sim/maps/room
```

## Files you should end up with

| File | What it is |
|---|---|
| `room.yaml` | Map settings: image name, resolution (0.05 m per pixel), origin |
| `room.pgm` | The map image: white free space, black walls, grey unknown |

`navigation.launch.py` loads `maps/room.yaml` by default. Use another name with
`map:=/full/path/other.yaml`.

## Notes

- **Start mapping from the spawn point.** The map's origin is where the robot was when SLAM started. The Nav2
  config assumes the robot is at (0, 0) on the map at start-up. If you mapped from somewhere else, set
  `set_initial_pose: false` in `config/nav2_params.yaml` and use **2D Pose Estimate** in RViz.
- Build with `colcon build --symlink-install`, or the saved map will land in `src/` but Nav2 will look in
  `install/`. Alternatively pass the full `map:=...` path.
- You can clean up `room.pgm` in any image editor (paint over noise with black or white) and keep the
  same `room.yaml`.
- A map made in the simulated room is for testing. For the real robot, make a new one in the real room.
