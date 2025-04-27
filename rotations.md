Okay, let's create a tabular overview of the rotations you've described. We'll break it down into the two sets of rotations you've specified, keeping in mind the Z-Y-X order.

**Set 1: "Flat Options"**

These involve rotations around the Z-axis (yaw) and rotations of 0° and 180° around the X-axis. There is no rotation around the Y-axis in this set.

| Combination ID | Yaw (Z)      | Pitch (Y)    | Roll (X)       | Description                                      |
| :------------- | :----------- | :----------- | :------------- | :----------------------------------------------- |
| 1              | 0°           | 0°           | 0°             | Base flat orientation                            |
| 2              | 90°          | 0°           | 0°             | Flat, rotated 90° clockwise around Z             |
| 3              | 180°         | 0°           | 0°             | Flat, rotated 180° around Z                      |
| 4              | 270°         | 0°           | 0°             | Flat, rotated 270° clockwise (or 90° counter) around Z |
| 5              | 0°           | 0°           | 180°           | Flat, flipped 180° around X                      |
| 6              | 90°          | 0°           | 180°           | Flat, rotated 90° around Z, then flipped 180° around X |
| 7              | 180°         | 0°           | 180°           | Flat, rotated 180° around Z, then flipped 180° around X |
| 8              | 270°         | 0°           | 180°           | Flat, rotated 270° around Z, then flipped 180° around X |

**Set 2: More Complex Rotations**

These involve 4 rotations around the Z-axis (starting at 45° with 90° increments), combined with two angles around the Y-axis (+/- 45°) and two angles around the X-axis (+/- 90°).

| Combination ID | Yaw (Z)      | Pitch (Y)    | Roll (X)       | Description                                                                 |
| :------------- | :----------- | :----------- | :------------- | :-------------------------------------------------------------------------- |
| 9              | 45°          | 45°          | 90°            | Rotated 45° around Z, then 45° around Y, then 90° around X                 |
| 10             | 45°          | 45°          | -90° (270°)    | Rotated 45° around Z, then 45° around Y, then -90° around X                |
| 11             | 45°          | -45° (315°) | 90°            | Rotated 45° around Z, then -45° around Y, then 90° around X                |
| 12             | 45°          | -45° (315°) | -90° (270°)    | Rotated 45° around Z, then -45° around Y, then -90° around X               |
| 13             | 135°         | 45°          | 90°            | Rotated 135° around Z, then 45° around Y, then 90° around X                |
| 14             | 135°         | 45°          | -90° (270°)    | Rotated 135° around Z, then 45° around Y, then -90° around X               |
| 15             | 135°         | -45° (315°) | 90°            | Rotated 135° around Z, then -45° around Y, then 90° around X               |
| 16             | 135°         | -45° (315°) | -90° (270°)    | Rotated 135° around Z, then -45° around Y, then -90° around X              |
| 17             | 225°         | 45°          | 90°            | Rotated 225° around Z, then 45° around Y, then 90° around X                |
| 18             | 225°         | 45°          | -90° (270°)    | Rotated 225° around Z, then 45° around Y, then -90° around X               |
| 19             | 225°         | -45° (315°) | 90°            | Rotated 225° around Z, then -45° around Y, then 90° around X               |
| 20             | 225°         | -45° (315°) | -90° (270°)    | Rotated 225° around Z, then -45° around Y, then -90° around X              |
| 21             | 315°         | 45°          | 90°            | Rotated 315° around Z, then 45° around Y, then 90° around X                |
| 22             | 315°         | 45°          | -90° (270°)    | Rotated 315° around Z, then 45° around Y, then -90° around X               |
| 23             | 315°         | -45° (315°) | 90°            | Rotated 315° around Z, then -45° around Y, then 90° around X               |
| 24             | 315°         | -45° (315°) | -90° (270°)    | Rotated 315° around Z, then -45° around Y, then -90° around X              |

**Total Number of Rotations:**

You have defined $8$ "flat options" and $4 \times 2 \times 2 = 16$ more complex rotations. This gives you a total of $8 + 16 = 24$ distinct rotation combinations to consider for your solver.

Remember that these rotations will be applied in the order of Yaw (Z), then Pitch (Y), then Roll (X) to the piece's local coordinate system.
