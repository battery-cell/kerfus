# meshes/

STL files that make the robot look like your real model in RViz and Gazebo.

**This is optional.** The simulation works without any files here: `urdf/kerfus.urdf` draws the body
as a box, the wheels as cylinders and the lidar as two cylinders, using the measured sizes. Add meshes
only when you want it to look right.

## Put these here

| File | What it is | Origin of the model (very important) |
|---|---|---|
| `base_link.stl` | Body shell, plates, motors, Raspberry Pi, simplified | Centre of the underside of the body, Z up, X forward |
| `wheel.stl` | One wheel | Centre of the wheel, axle along the **Y** axis |
| `lidar.stl` | Lidar head and base | Centre of the scan plane on the rotation axis, Z up |

## How to export them from FreeCAD

1. Open `Kerfus_corpus` and show only the parts for one file.
2. Move the object so its origin matches the table above. Your `Body` already has its origin at the
   underside centre (it spans z = 0 to 80 mm). The wheel's origin is **not** at its centre: in
   `Wheel.step` the axle runs along Y at x = 0, z = 19.9 mm between y = -20 and y = 0, so the centre
   is at (0, -10, 19.9) mm. Move it to (0, 0, 0) first. The lidar's up direction is its Y axis in your
   export, so rotate it 90 degrees about X so that it points along Z.
3. Select the object, then **File > Export**, type **STL Mesh (*.stl)**, and save it in this folder.
4. Undo the move in FreeCAD afterwards.

Things that help:
- **Leave out the Raspberry Pi's tiny parts** (connectors, SD slot). Your `main_corpus` file has 75
  separate Raspberry Pi parts, which makes a huge, slow mesh. Export the body and plates, and keep the Pi as
  a simple block if you want it visible.
- Keep each STL under about 50,000 triangles. Coarser tessellation at export time is fine.
- FreeCAD exports in millimetres, so the URDF uses `scale="0.001 0.001 0.001"`.

## Switch the URDF to the meshes

In `urdf/kerfus.urdf`, replace the `<geometry>` of each **visual** (not the collision) with, for example:

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <mesh filename="package://kerfus_sim/meshes/base_link.stl" scale="0.001 0.001 0.001"/>
  </geometry>
</visual>
```

Use the same pattern for `wheel_left` and `wheel_right` (`wheel.stl`, no `rpy` rotation needed if the
axle was exported along Y) and for `lidar_link` (`lidar.stl`).

Leave the **collision** shapes as boxes and cylinders. They make the physics faster and steadier.

If Gazebo says it cannot find `package://kerfus_sim/...`, check that you built with
`colcon build --symlink-install` and started Gazebo through `sim.launch.py`, which sets the
resource path for it.
