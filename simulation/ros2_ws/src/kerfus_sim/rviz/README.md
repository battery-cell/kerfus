# rviz/

RViz configurations for the simulation.

## What is in here

`slam.rviz` is the view used by `launch/bringup.launch.py`:

- **Fixed Frame**: `map`
- **RobotModel** from `/robot_description`
- **LaserScan** from `/scan` (red points)
- **Map** from `/map` (the occupancy grid slam_toolbox builds)
- **Grid** and **TF**

Open it by starting the demo:

```bash
./run_sim.sh
```

or load it in your own RViz:

```bash
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix kerfus_sim)/share/kerfus_sim/rviz/slam.rviz
```

The map starts empty (all grey/unknown). Drive the robot with teleop and it fills in.
