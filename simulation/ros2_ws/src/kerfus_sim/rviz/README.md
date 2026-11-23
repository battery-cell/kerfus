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

## Navigation view

`nav.rviz` is the view used by `launch/nav_demo.launch.py`:

- **Map** from `/map` (the reference map in `maps/room.yaml`)
- **Global Costmap** from `/global_costmap/costmap`
- **Local Costmap** from `/local_costmap/costmap`
- **Path** from `/plan`
- **LaserScan**, **RobotModel**, **Grid** and **TF**
- Nav2's **Navigation 2** panel and **Nav2 Goal** tool

Start it with:

```bash
./run_sim.sh --nav
```
