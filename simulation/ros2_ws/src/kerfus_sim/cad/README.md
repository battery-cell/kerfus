# cad/

Source files for the robot's design. Nothing here is installed into the ROS package: it is your
reference material, kept next to the simulation so the numbers can be traced back.

## Put these here

| File | Where to get it | Why |
|---|---|---|
| `Kerfus_corpus-main_corpus.step` | FreeCAD: select `main_corpus`, File > Export > STEP | The body shell, plates, Raspberry Pi and motors |
| `Kerfus_corpus-Wheel.step` | You already have it | Wheel size: 44 mm diameter, 20 mm wide |
| `Kerfus_corpus-Motor_plate.step` | You already have it | Motor mount |
| `Kerfus_corpus-LidarAssembly.step` | You already have it | Lidar position and head size |
| `Kerfus_corpus.FCStd` | Your FreeCAD project | The editable original. Keep the copy saved by your newest FreeCAD |
| `assembly_1.urdf` | The Onshape export you made | Reference only: it is **not** used (see `docs/measured_dimensions.md`) |
| `rplidar_a1m8_datasheet.pdf` | Slamtec's site: search "RPLIDAR A1M8 datasheet" | See below |

## From the lidar datasheet, write down

These go into `urdf/kerfus.urdf` (the `lidar_joint` and the `lidar_link` inertia):

1. **Scan plane height** above the mounting face, in mm. The current 0.127 m is a guess.
2. **Mass**, in grams. The current 0.17 kg is a guess.
3. **Direction of 0 degrees** relative to the cable or connector. It decides which way the scan points.
4. **Head diameter** and the **blind zone** (minimum range, about 0.15 m is already assumed).

## Tip

When you change the CAD (move the lidar, widen the body), re-export the STEP files and re-run the
measurements described in `docs/measured_dimensions.md`, then update the URDF by hand.
