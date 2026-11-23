# worlds/

Gazebo worlds: the environment the robot drives around in.

## What is in here

`room.sdf`: a 6 m x 5 m room centred on the origin, with four walls (1 m high) and three obstacles
(a crate, a pillar and a table). The robot spawns at (0, 0) facing +X.

## Rules when you edit or add a world

- **Keep the world name `kerfus_room`**, or change `WORLD_NAME` in `launch/sim.launch.py` to match.
  The robot-spawn and joint-state bridge use that name.
- **Keep the four plugins** at the top (`Physics`, `UserCommands`, `SceneBroadcaster`, `Sensors`).
  Without `Sensors` there is no lidar scan.
- **Obstacles must be taller than the lidar's scan plane** (about 0.127 m), or the lidar looks over them.
  The simulated lidar sees what is *drawn* (visuals), so every wall and obstacle needs a `<visual>` as
  well as a `<collision>`.
- If the Gazebo window will not open on your graphics card, change `ogre2` to `ogre` in the `Sensors`
  plugin.

## Get these (optional)

| What | How |
|---|---|
| A layout matching a real room | Measure the room (walls, doors, furniture) and edit the `<pose>` and `<size>` values in `room.sdf` |
| Ready-made furniture and rooms | Browse Gazebo Fuel, `app.gazebosim.org/fuel`, download a model, and add an `<include>` to the world |
| A world with a narrow doorway | Copy a wall in `room.sdf`, leave a gap of at least 0.6 m (the robot is about 0.32 m wide, and Nav2 inflates obstacles) |

Run a different world with:

```bash
ros2 launch kerfus_sim sim.launch.py world:=/full/path/to/my_world.sdf
```
