# Measured dimensions

Where every number in `urdf/kerfus.urdf` comes from, and how far to trust it.

**Method.** The STEP files are plain text, so they were read directly: part sizes come from vertex
positions and circle radii. No CAD program was used, so full circles and arcs are bounded rather than
measured exactly, and nothing here is a mass or inertia from the CAD. Positions of parts relative to
each other come from the joint chain in your Onshape URDF (`assembly_1.urdf`). All STEP units are mm.

## Frame used in the URDF

`base_link` origin: centre of the body, on its underside. +X forward (assumed), +Y left, +Z up.
This is the same frame as the `Body` part in `main_corpus.step`, which spans z = 0 to 80 mm.

## Numbers

| What | Value | Source | Confidence |
|---|---|---|---|
| Body outline | 280 x 280 mm | Vertices of `Body`: x and y both -140 to +140 | Medium: the edges are large arcs (radius 313 mm), so the real outline may bulge a few mm further |
| Body height | 80 mm (z = 0 to 80) | Vertices of `Body` | High |
| Connector plate | 105 x 76 x 5 mm, on top of the body (z = 80 to 85) | `connector_plate` | High |
| Wheel radius | 22 mm | Circle radius in `Wheel.step` | High |
| Wheel width | 20 mm | Wheel spans y = -20 to 0 | High |
| Wheel axle height | 19.9 mm above the body underside | Axle line at z = 19.9 in `Wheel.step`; agrees with the Onshape joint (z = 0.0199 m) | High |
| Wheel centres | y = +/-149.6 mm, x = 0 | Onshape joint chain: the wheel's inner face is at |y| = 139.6 mm and it is 20 mm wide | Medium-high |
| Track (centre to centre) | 299.2 mm | 2 x 149.6 | Medium-high |
| Wheels vs. ground | Bottoms are 2.1 mm below the body underside | 19.9 - 22 | High |
| Gear motors | At y = +/-111.1 mm, x = -14 mm, z = 49 mm | Onshape joints | Medium |
| Lidar axis | x = 0, y = 0 (vertical line through the body centre) | Onshape chain, head centre within 1 mm | Medium-high |
| Lidar head | z = 115.3 to 138.8 mm, about 72 mm across | `RPLidar_SCTL` | Medium |
| Lidar base | z = 85 to 116 mm | `RPLidar_SCTL001`, thickness 31 mm only (its other sizes are not reliable) | Medium |
| Lidar top height | about 139 mm | Compare: you measured 139.59 mm with FreeCAD's Measure tool | Agrees |

## Still guesses (placeholders)

| What | Value used | Replace with |
|---|---|---|
| Robot mass | 3.0 kg | The weighed robot |
| Wheel mass | 0.08 kg each | Weighed |
| Lidar mass | 0.17 kg | Datasheet |
| Lidar scan plane height | 0.127 m (middle of the head) | Datasheet |
| Casters | Two frictionless balls at x = +/-115 mm | Your real supports |
| Which end is the front | +X | Your decision |

## Why the Onshape URDF was not used directly

- **Masses are about 1000 times too small** (body 0.0018 kg, each motor 0.0001 kg), which would make
  the physics wrong. Probably a density or unit setting in Onshape.
- **The two wheel joints disagree.** `revolute_1` has its axis pointing straight up once converted to the
  body frame, while `revolute_2` points along Y. One wheel would not turn about its axle.
- **It splits the robot into 8 links** joined by fixed joints, which Gazebo merges anyway.
- **No collision shapes**, and the meshes are referenced as `package://assembly_1/...`, which
  doesn't exist here.

Its positions were still useful: that is where the wheel and lidar locations above come from.
